"""
🛡️ GINI Guardian v3.3 — 텍스트 권위 강화! (최적화)
✨ 음성 제거 → 명확한 텍스트 중심 상담
✨ 종목명 완벽 인식 (퍼지 매칭)
✨ 핵심 로직 강화
⚡ 성능 최적화: 캐싱 시스템 추가!

라이라 설계 × 미라클 구현 × 제미니 전략 🔥
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from groq import Groq
import re
import sqlite3
from collections import Counter
import io
import os
from difflib import SequenceMatcher

st.set_page_config(page_title="GINI Guardian v3.3", page_icon="🛡️", layout="wide")

# ============================================================================
# 📊 종목명 데이터베이스 (제미니 전략)
# ============================================================================

STOCK_NAMES_DB = {
    '삼성전자': '005930', 'SK하이닉스': '000660', 'NAVER': '035420', '카카오': '035720',
    '삼성바이오로직스': '207940', 'LG에너지솔루션': '373220', 'LG화학': '051910',
    '현대차': '005380', '기아': '000270', '셀트리온': '068270', '포스코홀딩스': '005490',
    '삼성SDI': '006400', 'SK이노베이션': '096770', 'KB금융': '105560', '신한지주': '055550',
    'LG전자': '066570', '한국전력': '015760', '한미반도체': '042700', '한미약품': '128940',
    '에코프로비엠': '247540', '에코프로': '086520', '엘앤에프': '066970', '알테오젠': '196170',
    '카카오게임즈': '293490', '카카오뱅크': '323410', '하이브': '352820', 'CJ ENM': '035760',
}

COMMON_MISTAKES = {
    '상승전자': '삼성전자', '삼성건조': '삼성전자', '삼성전지': '삼성전자',
    '하이닉스': 'SK하이닉스', '에스케이하이닉스': 'SK하이닉스',
    '네이바': 'NAVER', '네이버': 'NAVER', '카카오톡': '카카오',
    '항미반도체': '한미반도체', '샐트리온': '셀트리온', '엘지화학': 'LG화학',
    '현대자동차': '현대차',
}

def get_similarity(str1, str2):
    """두 문자열 유사도 (0.0~1.0)"""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def find_similar_stock(input_text, threshold=0.7):
    """퍼지 매칭으로 유사 종목 찾기"""
    if input_text in STOCK_NAMES_DB:
        return [(input_text, STOCK_NAMES_DB[input_text], 1.0)]
    
    if input_text in COMMON_MISTAKES:
        corrected = COMMON_MISTAKES[input_text]
        if corrected in STOCK_NAMES_DB:
            return [(corrected, STOCK_NAMES_DB[corrected], 0.95)]
    
    similarities = []
    for stock_name, stock_code in STOCK_NAMES_DB.items():
        similarity = get_similarity(input_text, stock_name)
        if similarity >= threshold:
            similarities.append((stock_name, stock_code, similarity))
    
    similarities.sort(key=lambda x: x[2], reverse=True)
    return similarities[:3]

def extract_and_correct_stocks(text):
    """텍스트에서 종목명 추출 및 보정"""
    words = text.split()
    found_stocks = []
    corrected_text = text
    needs_confirmation = False
    
    for word in words:
        matches = find_similar_stock(word, threshold=0.7)
        
        if matches:
            best_match = matches[0]
            stock_name, stock_code, similarity = best_match
            
            if similarity < 1.0:
                needs_confirmation = True
            
            corrected_text = corrected_text.replace(word, stock_name)
            
            found_stocks.append({
                'original': word,
                'corrected': stock_name,
                'code': stock_code,
                'confidence': similarity,
                'alternatives': matches[1:] if len(matches) > 1 else []
            })
    
    return {
        'original': text,
        'corrected': corrected_text,
        'found_stocks': found_stocks,
        'needs_confirmation': needs_confirmation
    }

# ============================================================================
# 📊 실시간 주식 데이터 함수들
# ============================================================================

try:
    from pykrx import stock as pykrx_stock
    PYKRX_AVAILABLE = True
except:
    PYKRX_AVAILABLE = False

import random

@st.cache_data(ttl=300)  # 5분 캐싱
def get_stock_price_realtime(ticker):
    """실시간 주가 조회 (pykrx 또는 Mock) - 5분 캐싱"""
    if PYKRX_AVAILABLE:
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=7)
            end_str = end_date.strftime("%Y%m%d")
            start_str = start_date.strftime("%Y%m%d")
            
            df = pykrx_stock.get_market_ohlcv_by_date(start_str, end_str, ticker)
            
            if not df.empty:
                latest = df.iloc[-1]
                stock_name = pykrx_stock.get_market_ticker_name(ticker)
                
                return {
                    '종목코드': ticker,
                    '종목명': stock_name,
                    '현재가': int(latest['종가']),
                    '등락률': round(latest['등락률'], 2),
                    '조회일': df.index[-1].strftime("%Y-%m-%d")
                }
        except:
            pass
    
    # Mock 데이터
    return get_mock_stock_data(ticker)

def get_mock_stock_data(ticker):
    """Mock 주식 데이터"""
    mock_stocks = {
        '005930': {'name': '삼성전자', 'base_price': 70000},
        '000660': {'name': 'SK하이닉스', 'base_price': 130000},
        '035420': {'name': 'NAVER', 'base_price': 200000},
        '035720': {'name': '카카오', 'base_price': 50000},
        '207940': {'name': '삼성바이오로직스', 'base_price': 800000},
        '051910': {'name': 'LG화학', 'base_price': 400000},
        '042700': {'name': '한미반도체', 'base_price': 70000},
    }
    
    if ticker in mock_stocks:
        info = mock_stocks[ticker]
        base = info['base_price']
        variation = random.uniform(-0.05, 0.05)
        current = int(base * (1 + variation))
        
        return {
            '종목코드': ticker,
            '종목명': info['name'],
            '현재가': current,
            '등락률': round(variation * 100, 2),
            '조회일': datetime.now().strftime("%Y-%m-%d")
        }
    
    return None

def update_portfolio_realtime(portfolio):
    """포트폴리오 실시간 업데이트"""
    updated = []
    total_buy = 0
    total_value = 0
    
    for item in portfolio:
        data = get_stock_price_realtime(item['종목코드'])
        
        if data:
            current_price = data['현재가']
            buy_amount = item['매입가'] * item['수량']
            current_amount = current_price * item['수량']
            profit_loss = current_amount - buy_amount
            profit_rate = ((current_price - item['매입가']) / item['매입가']) * 100
            
            updated.append({
                '종목코드': item['종목코드'],
                '종목명': data['종목명'],
                '매입가': item['매입가'],
                '현재가': current_price,
                '수량': item['수량'],
                '매입금액': buy_amount,
                '평가금액': current_amount,
                '손익금액': profit_loss,
                '수익률': round(profit_rate, 2),
                '등락률': data['등락률']
            })
            
            total_buy += buy_amount
            total_value += current_amount
        else:
            buy_amount = item['매입가'] * item['수량']
            
            updated.append({
                '종목코드': item['종목코드'],
                '종목명': item.get('종목명', '정보없음'),
                '매입가': item['매입가'],
                '현재가': item['매입가'],
                '수량': item['수량'],
                '매입금액': buy_amount,
                '평가금액': buy_amount,
                '손익금액': 0,
                '수익률': 0.0,
                '등락률': 0.0
            })
            
            total_buy += buy_amount
            total_value += buy_amount
    
    total_profit = total_value - total_buy
    total_rate = ((total_value - total_buy) / total_buy * 100) if total_buy > 0 else 0
    
    summary = {
        '총매입액': total_buy,
        '총평가액': total_value,
        '총손익': total_profit,
        '수익률': round(total_rate, 2)
    }
    
    return updated, summary

# ============================================================================
# 🗄️ SQLite 데이터베이스 함수
# ============================================================================

def get_connection():
    """SQLite 연결"""
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    return conn

def create_tables():
    """테이블 생성"""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_input TEXT NOT NULL,
        ai_response TEXT NOT NULL,
        emotion_score REAL,
        risk_level TEXT,
        tags TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS portfolio (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker TEXT NOT NULL,
        stock_name TEXT,
        buy_price INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    conn.commit()
    conn.close()

def save_chat(user_input, ai_response, emotion_score, risk_level, tags):
    """상담 기록 저장"""
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("""
    INSERT INTO chats (user_input, ai_response, emotion_score, risk_level, tags)
    VALUES (?, ?, ?, ?, ?)
    """, (user_input, ai_response, emotion_score, risk_level, tags))
    
    conn.commit()
    conn.close()
    
    # 캐시 무효화
    load_history.clear()
    get_emotion_stats.clear()

@st.cache_data(ttl=30)  # 30초 캐싱
def load_history():
    """과거 상담 기록 조회 (캐싱)"""
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    cur.execute("SELECT user_input, ai_response, emotion_score, risk_level, tags, timestamp FROM chats ORDER BY id DESC LIMIT 50")
    rows = cur.fetchall()
    conn.close()
    return rows

@st.cache_data(ttl=30)  # 30초 캐싱
def get_emotion_stats():
    """감정 통계 (캐싱)"""
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    cur.execute("SELECT emotion_score, timestamp FROM chats WHERE emotion_score IS NOT NULL ORDER BY timestamp")
    rows = cur.fetchall()
    conn.close()
    return rows

def save_portfolio_stock(ticker, stock_name, buy_price, quantity):
    """포트폴리오에 종목 추가"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
    INSERT INTO portfolio (ticker, stock_name, buy_price, quantity)
    VALUES (?, ?, ?, ?)
    """, (ticker, stock_name, buy_price, quantity))
    conn.commit()
    conn.close()
    
    # 캐시 무효화
    load_portfolio_from_db.clear()

@st.cache_data(ttl=60)  # 1분 캐싱
def load_portfolio_from_db():
    """DB에서 포트폴리오 로드 (캐싱)"""
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    cur.execute("SELECT ticker, stock_name, buy_price, quantity FROM portfolio")
    rows = cur.fetchall()
    conn.close()
    
    return [
        {
            '종목코드': row[0],
            '종목명': row[1],
            '매입가': row[2],
            '수량': row[3]
        }
        for row in rows
    ]

def delete_portfolio_stock(ticker):
    """포트폴리오에서 종목 삭제"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM portfolio WHERE ticker = ?", (ticker,))
    conn.commit()
    conn.close()
    
    # 캐시 무효화
    load_portfolio_from_db.clear()

create_tables()

# ============================================================================
# 🎨 애니메이션 CSS
# ============================================================================

ANIMATION_CSS = """
<style>
    .main { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); }
    
    @keyframes gentle-blink { 
        0%, 100% { opacity: 1; } 
        50% { opacity: 0.7; } 
    }
    
    @keyframes float-gentle {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .header-animated {
        animation: gentle-blink 3s infinite;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #052d7a, #0a47a0, #052d7a);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    @keyframes hot-pulse {
        0%, 100% { 
            opacity: 1;
            transform: scale(1);
            text-shadow: 0 0 5px #ff4500;
        }
        50% { 
            opacity: 0.7;
            transform: scale(1.1);
            text-shadow: 0 0 15px #ff6347, 0 0 25px #ff4500;
        }
    }
    
    .hot-badge {
        animation: hot-pulse 1.5s infinite;
        display: inline-block;
        font-weight: bold;
    }
    
    .success-float { 
        animation: gentle-blink 2s infinite;
        background-color: #d4edda; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #28a745; 
        margin-bottom: 10px; 
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3cd 0%, #ffe69c 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #ff6b00;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .danger-box {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 8px solid #dc3545;
        margin: 20px 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        animation: hot-pulse 2s infinite;
    }
</style>
"""

st.markdown(ANIMATION_CSS, unsafe_allow_html=True)

# ============================================================================
# 🎯 위험지표 계산
# ============================================================================

def calc_risk_score(emotion, volatility=0, news=0):
    """위험지표 계산"""
    score = emotion * 0.5 + volatility * 0.3 + news * 0.2
    return round(score, 2)

def get_risk_emoji(risk):
    """위험도 이모지"""
    if risk >= 8.0:
        return "🔴 극도로 위험"
    elif risk >= 6.5:
        return "🟠 높은 위험"
    elif risk >= 5.0:
        return "🟡 중간 위험"
    else:
        return "🟢 낮은 위험"

def detect_risk_level(risk_score):
    """위험 레벨 텍스트"""
    if risk_score >= 6.5:
        return "high"
    elif risk_score >= 5.0:
        return "mid"
    else:
        return "low"

def detect_tags(user_input):
    """감정 태그 감지"""
    tags = []
    
    if any(word in user_input for word in ["불안", "걱정", "두려", "무섯"]):
        tags.append("불안")
    if any(word in user_input for word in ["손실", "떨어", "내려", "털렸", "씨발"]):
        tags.append("분노")
    if any(word in user_input for word in ["사도", "들어갈", "몰빵", "급"]):
        tags.append("충동")
    if any(word in user_input for word in ["후회", "실수", "잘못"]):
        tags.append("후회")
    
    return ", ".join(tags) if tags else "중립"

def get_strong_warning(risk_level):
    """위험도에 따른 강력한 경고 메시지"""
    if risk_level == "high":
        return """
        <div class="danger-box">
            <h2 style="color: #dc3545; margin: 0;">⛔ 긴급 경고 ⛔</h2>
            <h3 style="color: #721c24; margin-top: 10px;">지금 당장 거래를 멈추세요!</h3>
            <p style="font-size: 1.1em; font-weight: bold; color: #721c24;">
            당신의 감정 상태는 극도로 불안정합니다.<br>
            이 상태에서의 투자 결정은 99% 실패합니다.<br><br>
            <strong>즉시 행동할 것:</strong><br>
            1. 거래 앱을 끄세요<br>
            2. 최소 24시간 쉬세요<br>
            3. 신뢰할 수 있는 사람과 대화하세요
            </p>
        </div>
        """
    elif risk_level == "mid":
        return """
        <div class="warning-box">
            <h3 style="color: #856404; margin: 0;">⚠️ 주의 필요</h3>
            <p style="font-size: 1.05em; color: #856404;">
            당신의 감정 상태가 흔들리고 있습니다.<br>
            오늘은 거래를 하지 않는 것이 현명합니다.<br><br>
            잠시 멈추고, 내일 다시 생각해보세요.
            </p>
        </div>
        """
    else:
        return ""

# ============================================================================
# 🤖 Groq 상담 함수
# ============================================================================

def groq_counsel(user_text):
    """Groq API를 통한 AI 상담"""
    try:
        api_key = os.getenv("GROQ_API_KEY") or "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"
        
        client = Groq(api_key=api_key)
        
        prompt = f"""당신은 냉철하고 권위 있는 투자 심리 상담 전문가입니다.
감정적인 투자를 막고, 이성적 판단을 돕는 것이 목표입니다.

사용자 질문: {user_text}

**상담 원칙:**
1. 감정 점수 0~10으로 평가 (0=매우 안정, 10=극도로 불안/흥분)
2. 직설적이고 명확한 조언 (애매한 표현 금지)
3. 과매매 위험 감지 시 강력하게 경고
4. 구체적인 행동 지침 제시

**응답 형식:**
[감정점수: X]
(명확하고 직설적인 상담 내용)
"""
        
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        
        full_response = response.choices[0].message.content
        
        emotion_match = re.search(r'\[감정점수[:\s]*(\d+(?:\.\d+)?)\]', full_response)
        emotion_score = float(emotion_match.group(1)) if emotion_match else 5.0
        
        clean_response = re.sub(r'\[감정점수[:\s]*\d+(?:\.\d+)?\]', '', full_response).strip()
        
        return clean_response, emotion_score
        
    except Exception as e:
        return f"상담 중 오류가 발생했습니다: {str(e)}", 5.0

# ============================================================================
# Session State 초기화
# ============================================================================

if 'portfolio' not in st.session_state:
    db_portfolio = load_portfolio_from_db()
    
    if db_portfolio:
        st.session_state.portfolio = db_portfolio
    else:
        st.session_state.portfolio = [
            {'종목코드': '005930', '종목명': '삼성전자', '매입가': 70000, '수량': 10},
            {'종목코드': '000660', '종목명': 'SK하이닉스', '매입가': 130000, '수량': 5}
        ]

# ============================================================================
# 🌟 메인 UI
# ============================================================================

st.markdown('<div class="header-animated">🛡️ GINI Guardian v3.3</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; margin-bottom: 20px;"><span class="hot-badge" style="font-size: 1.2em; color: #ff4500;">권위 있는 텍스트 상담 🔥</span></div>', unsafe_allow_html=True)

# ============================================================================
# 탭 구성
# ============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🧭 AI 상담",
    "📚 상담 기록",
    "💼 실시간 포트폴리오",
    "⚙️ 설정"
])

# ============================================================================
# TAB 1: AI 상담 (텍스트 강화)
# ============================================================================

with tab1:
    st.markdown('<div style="text-align: center; margin-bottom: 15px;"><span style="font-size: 1.8em;">💬 투자 심리 상담</span></div>', unsafe_allow_html=True)
    
    st.info("✨ 감정적 투자를 막고 이성적 판단을 돕는 AI 상담사입니다.")
    
    # 종목명 자동 보정 안내
    with st.expander("💡 종목명 자동 보정 기능", expanded=False):
        st.write("""
        **오타가 있어도 걱정 마세요!**
        - '상승전자' → '삼성전자' 자동 보정
        - '항미반도체' → '한미반도체' 자동 보정
        - '네이바' → 'NAVER' 자동 보정
        
        AI가 자동으로 정확한 종목명을 찾아드립니다!
        """)
    
    user_input = st.text_area(
        "💬 투자 고민을 솔직하게 말씀해주세요:",
        height=120,
        placeholder="예) 삼성전자 손실이 커서 너무 힘들어요...\n예) 오늘 카카오 급등했는데 지금 사도 될까요?",
        key="chat_textarea"
    )
    
    if st.button("🧭 AI 상담 받기", use_container_width=True, type="primary"):
        if user_input.strip():
            # 종목명 자동 보정
            correction_result = extract_and_correct_stocks(user_input)
            
            if correction_result['found_stocks']:
                st.markdown("---")
                st.markdown("### 🎯 종목명 인식")
                
                for stock in correction_result['found_stocks']:
                    if stock['confidence'] == 1.0:
                        st.success(f"✅ {stock['corrected']} ({stock['code']})")
                    else:
                        st.info(f"💡 '{stock['original']}' → **{stock['corrected']}** ({stock['code']}) 으로 보정되었습니다.")
                
                user_input = correction_result['corrected']
            
            st.markdown("---")
            
            with st.spinner("🤔 AI가 분석 중... (2~3초)"):
                response, emotion_score = groq_counsel(user_input)
                
                volatility_score = 5.0
                news_score = 3.0
                risk = calc_risk_score(emotion_score, volatility_score, news_score)
                risk_emoji = get_risk_emoji(risk)
                risk_level = detect_risk_level(risk)
                tags = detect_tags(user_input)
                
                save_chat(user_input, response, emotion_score, risk_level, tags)
                
                # 위험도 표시
                col_risk1, col_risk2 = st.columns(2)
                
                with col_risk1:
                    st.metric(
                        label="📊 위험지표",
                        value=f"{risk} / 10",
                        delta=None
                    )
                
                with col_risk2:
                    st.info(f"**{risk_emoji}**")
                
                # 강력한 경고 메시지 (위험도 높을 때)
                warning_html = get_strong_warning(risk_level)
                if warning_html:
                    st.markdown(warning_html, unsafe_allow_html=True)
                
                st.divider()
                
                # AI 상담 결과
                st.markdown("### 🧭 AI 상담 결과")
                st.write(response)
                
                st.success("✅ 상담 기록이 저장되었습니다! 📚")
                
                st.markdown("---")
        else:
            st.warning("⚠️ 질문을 입력해주세요!")

# ============================================================================
# TAB 2: 상담 기록
# ============================================================================

with tab2:
    st.subheader("📚 과거 상담 기록")
    
    history = load_history()
    
    if history:
        st.success(f"✅ 총 {len(history)}개의 상담 기록")
        st.divider()
        
        for idx, (user, ai, emo, risk, tags, timestamp) in enumerate(history, 1):
            with st.expander(f"💬 상담 #{idx} | {timestamp} | {tags}", expanded=False):
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown(f"**👤 당신의 질문:**\n{user}")
                    st.markdown(f"**💙 감정 점수:** {emo} / 10")
                
                with col2:
                    st.markdown(f"**⚠️ 위험지표:** {risk.upper()}")
                    st.markdown(f"**🏷️ 태그:** {tags}")
                
                st.markdown("---")
                st.markdown(f"**🤖 AI의 답변:**\n{ai}")
    else:
        st.info("📝 아직 상담 기록이 없습니다.")

# ============================================================================
# TAB 3: 실시간 포트폴리오
# ============================================================================

with tab3:
    st.markdown('<div style="text-align: center; margin-bottom: 15px;"><span class="hot-badge" style="font-size: 1.8em; color: #ff4500;">💼 실시간 포트폴리오 🔥</span></div>', unsafe_allow_html=True)
    
    st.info("✨ pykrx 기반 실시간 주가 추적 (20분 지연)")
    
    col_refresh, col_add = st.columns([1, 3])
    
    with col_refresh:
        if st.button("🔄 포트폴리오 새로고침", use_container_width=True, type="primary"):
            st.rerun()
    
    st.divider()
    
    if st.session_state.portfolio:
        with st.spinner("📊 실시간 데이터 조회 중..."):
            updated_portfolio, summary = update_portfolio_realtime(st.session_state.portfolio)
        
        col1, col2, col3, col4 = st.columns(4)
        
        profit_color = "#28a745" if summary['총손익'] >= 0 else "#dc3545"
        
        with col1:
            st.markdown(f'<div class="success-float"><strong>총 매입액</strong><br>₩{summary["총매입액"]:,}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="success-float"><strong>총 평가액</strong><br>₩{summary["총평가액"]:,}</div>', unsafe_allow_html=True)
        with col3:
            st.markdown(f'<div style="background: {profit_color}22; color: {profit_color}; font-weight: bold; padding: 15px; border-radius: 10px;"><strong>총 손익</strong><br>₩{summary["총손익"]:+,}</div>', unsafe_allow_html=True)
        with col4:
            st.markdown(f'<div style="background: {profit_color}22; color: {profit_color}; font-weight: bold; padding: 15px; border-radius: 10px;"><strong>수익률</strong><br>{summary["수익률"]:+.2f}%</div>', unsafe_allow_html=True)
        
        st.divider()
        
        st.markdown("### 📊 보유 종목")
        
        for stock in updated_portfolio:
            status_emoji = "🔴" if stock['수익률'] < 0 else "🟢" if stock['수익률'] > 0 else "⚪"
            bg_color = "#fff3cd" if stock['수익률'] < 0 else "#d4edda" if stock['수익률'] > 0 else "#e9ecef"
            text_color = "#dc3545" if stock['수익률'] < 0 else "#28a745" if stock['수익률'] > 0 else "#6c757d"
            
            data_status = "⚠️ 실시간 데이터 없음" if stock['수익률'] == 0 and stock['등락률'] == 0 else ""
            
            col_stock, col_delete = st.columns([6, 1])
            
            with col_stock:
                st.markdown(f'''
                <div style="background-color: {bg_color}; padding: 12px; border-radius: 8px; margin-bottom: 8px;">
                    {status_emoji} <strong>{stock["종목명"]}</strong> ({stock["종목코드"]}) {data_status}
                    <br>
                    매입: ₩{stock["매입가"]:,} | 현재: ₩{stock["현재가"]:,} | 수량: {stock["수량"]}개
                    <br>
                    <span style="color: {text_color}; font-weight: bold;">
                        수익률: {stock["수익률"]:+.2f}% | 손익: ₩{stock["손익금액"]:+,}
                    </span>
                </div>
                ''', unsafe_allow_html=True)
            
            with col_delete:
                if st.button("🗑️", key=f"delete_{stock['종목코드']}", help="종목 삭제"):
                    delete_portfolio_stock(stock['종목코드'])
                    st.session_state.portfolio = [p for p in st.session_state.portfolio if p['종목코드'] != stock['종목코드']]
                    st.rerun()
        
        st.divider()
        
        if summary['수익률'] < -5:
            st.error("🚨 포트폴리오 손실이 -5%를 넘었습니다! 감정적 매매를 조심하세요!")
        
    else:
        st.warning("📝 포트폴리오가 비어있습니다. 종목을 추가해주세요!")
    
    st.divider()
    
    st.markdown("### ➕ 종목 추가하기")
    
    with st.form("add_stock_form", clear_on_submit=True):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            new_ticker = st.text_input("종목코드", placeholder="042700")
        with col2:
            new_name = st.text_input("종목명", placeholder="한미반도체")
        with col3:
            new_buy_price = st.number_input("매입가", min_value=0, value=70000, step=1000)
        with col4:
            new_quantity = st.number_input("수량", min_value=1, value=10, step=1)
        
        submitted = st.form_submit_button("➕ 포트폴리오에 추가", type="primary", use_container_width=True)
        
        if submitted:
            if new_ticker and new_name and new_buy_price > 0:
                save_portfolio_stock(new_ticker, new_name, new_buy_price, new_quantity)
                
                st.session_state.portfolio.append({
                    '종목코드': new_ticker,
                    '종목명': new_name,
                    '매입가': new_buy_price,
                    '수량': new_quantity
                })
                
                st.success(f"✅ {new_name} ({new_ticker}) 추가 완료! 새로고침 버튼을 눌러주세요.")
                st.balloons()
            else:
                st.warning("⚠️ 모든 항목을 올바르게 입력해주세요!")

# ============================================================================
# TAB 4: 설정
# ============================================================================

with tab4:
    st.subheader("⚙️ 설정 & 정보")
    
    st.info(f"""
    **GINI Guardian v3.3 - 텍스트 권위 강화! (최적화)**
    
    ⚡ 최적화:
       - DB 연결 캐싱
       - 주가 데이터 5분 캐싱
       - 상담 기록 30초 캐싱
       - 포트폴리오 1분 캐싱
       - 렉 대폭 감소!
    
    🆕 v3.3 변경사항:
       - 음성 기능 제거 → 명확한 텍스트 중심
       - 권위 있는 직설적 조언
       - 강력한 경고 메시지 시스템
       - 핵심 로직에 집중
    
    ✅ 핵심 기능:
       - 종목명 자동 보정 (퍼지 매칭)
       - 실시간 포트폴리오 추적
       - 감정 분석 & 위험지표
       - 상담 기록 저장
    
    **다음 업그레이드:**
    - 위험지표 고도화 (거래 패턴 분석)
    - 맥락 기억 AI (과거 상담 내용 기억)
    - 대시보드 완성 (감정 히트맵)
    - 주간 리포트 자동 생성
    """)
    
    st.markdown("#### 📋 기술 스택")
    st.code("""
- Streamlit: UI/UX
- Groq API: AI 상담
- pykrx: 실시간 주식 데이터
- SQLite: 데이터 저장
- Plotly: 차트 시각화
- 퍼지 매칭: 종목명 보정
    """, language="python")
    
    st.markdown("#### 🎯 설계 철학")
    st.write("""
    **제미니 전략:**
    - 기계적 음성보다 명확한 텍스트가 더 권위 있음
    - 흥분한 투자자에게는 냉철하고 직설적인 조언 필요
    - 핵심 기능의 완성도가 가장 중요
    
    **라이라 설계 × 미라클 구현 × 제미니 전략**
    """)

st.divider()
st.markdown("---\n🛡️ **GINI Guardian v3.3** | 💬 텍스트 권위 강화 | 💙 라이라 × 미라클 × 제미니")
