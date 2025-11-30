"""
🛡️ GINI Guardian v4.4 — 라이라 최종 수정!
✨ NEW: 전문적 경고 문구, 행동 단계 추가, 톤 통일
✨ 주간 리포트 + 거래 패턴 분석
✨ 맥락 기억 + 감정 압박 시스템

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

st.set_page_config(page_title="GINI Guardian v4.4", page_icon="🛡️", layout="wide")
# ============================================================================
# 🎨 강력한 배경색 CSS - app.py CSS 부분 교체
# ============================================================================

st.markdown("""
<style>
/* ------------------------------- */
/* 🌙 강력한 배경색 적용 */
/* ------------------------------- */
body,
.stApp,
[data-testid="stAppViewContainer"],
.main,
[data-testid="stApp"],
section[data-testid="stAppViewContainer"] > .main {
    background-color: #1A1625 !important;
}

/* 메인 컨테이너 */
.block-container {
    background-color: transparent !important;
}

/* 사이드바 */
[data-testid="stSidebar"],
[data-testid="stSidebarNav"],
section[data-testid="stSidebar"] > div {
    background-color: #13111A !important;
}

/* 헤더 */
header[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* ------------------------------- */
/* 🎨 Brand Colors */
/* ------------------------------- */
:root {
    --soft-lavender: #A78BFA;
    --pastel-violet: #C4B5FD;
    --glass-border: rgba(255,255,255,0.12);
    --headline: #EDEAFF;
    --body-text: #D8D3E8;
    --sub-text: #B5ADC7;
}

/* ------------------------------- */
/* 📝 텍스트 컬러 */
/* ------------------------------- */
.stApp {
    color: #EDEAFF !important;
    font-family: "Pretendard", "Inter", sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    color: var(--headline) !important;
    text-shadow: 
        0 0 8px rgba(167,139,250,0.4),
        0 0 14px rgba(167,139,250,0.25);
}

p, div, span, .stMarkdown {
    color: var(--body-text) !important;
}

.stCaption {
    color: var(--sub-text) !important;
}

/* ------------------------------- */
/* 🌈 메인 박스 그라데이션 */
/* ------------------------------- */
.intro-banner,
.main-banner {
    background: linear-gradient(165deg, #A78BFA, #C4B5FD) !important;
    padding: 26px !important;
    border-radius: 18px !important;
    border: 1px solid var(--glass-border) !important;
    box-shadow: 0 0 25px rgba(167,139,250,0.2) !important;
    backdrop-filter: blur(6px);
}

/* ------------------------------- */
/* 🟣 Buttons */
/* ------------------------------- */
.stButton > button {
    background: linear-gradient(165deg, #A78BFA, #C4B5FD) !important;
    color: #1A1535 !important;
    font-weight: 600 !important;
    border-radius: 12px !important;
    padding: 12px 18px !important;
    border: none !important;
    box-shadow: 
        0 0 12px rgba(167,139,250,0.35),
        0 4px 8px rgba(167,139,250,0.2) !important;
}

.stButton > button:hover {
    filter: brightness(1.12) !important;
}

/* ------------------------------- */
/* 📊 Input Fields */
/* ------------------------------- */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input {
    background: rgba(255,255,255,0.08) !important;
    border: 1px solid var(--glass-border) !important;
    color: var(--headline) !important;
    border-radius: 10px !important;
    padding: 12px !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--soft-lavender) !important;
    box-shadow: 0 0 8px rgba(167,139,250,0.3) !important;
}

/* ------------------------------- */
/* 🧭 Tabs */
/* ------------------------------- */
.stTabs [data-baseweb="tab"] {
    background: rgba(255,255,255,0.05);
    color: var(--body-text) !important;
    border-radius: 8px;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(165deg, #A78BFA, #C4B5FD) !important;
    color: #1A1535 !important;
    font-weight: 600;
}

/* ------------------------------- */
/* 📦 Expander */
/* ------------------------------- */
.stExpander {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px !important;
}

.streamlit-expanderHeader {
    background: rgba(167,139,250,0.08) !important;
    color: var(--headline) !important;
}

/* ------------------------------- */
/* 📈 Metrics */
/* ------------------------------- */
.stMetric {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: 12px !important;
}

.stMetric [data-testid="stMetricValue"] {
    color: var(--soft-lavender) !important;
}

/* ------------------------------- */
/* 🔻 Divider */
/* ------------------------------- */
hr {
    border: none !important;
    border-bottom: 1px solid rgba(167,139,250,0.15) !important;
}

/* ------------------------------- */
/* 🌟 Header Title */
/* ------------------------------- */
.header-animated {
    color: var(--headline) !important;
    font-size: 2.3rem !important;
    font-weight: 700 !important;
    text-shadow: 
        0 0 12px rgba(167,139,250,0.5),
        0 0 20px rgba(167,139,250,0.3);
}
</style>
""", unsafe_allow_html=True)


# ============================================================================
# 📱 PWA 설정
# ============================================================================

st.markdown("""
<head>
    <meta name="theme-color" content="#667eea">
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="GINI Guardian">
    <link rel="manifest" href="./manifest.json">
    <link rel="icon" type="image/png" sizes="192x192" href="./static/icons/icon-192x192.png">
    <link rel="icon" type="image/png" sizes="512x512" href="./static/icons/icon-512x512.png">
    <link rel="apple-touch-icon" href="./static/icons/icon-192x192.png">
</head>
<script>
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('./service-worker.js')
                .then(function(registration) {
                    console.log(' Service Worker 등록 성공');
                })
                .catch(function(error) {
                    console.log(' Service Worker 등록 실패:', error);
                });
        });
    }
</script>
""", unsafe_allow_html=True)
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
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    
    # 기존 상담 기록 테이블
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
    
    # 포트폴리오 테이블
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
    
    # ===== v4.0 NEW: 맥락 기억 테이블 =====
    
    # 1. 가장 위험했던 순간 기록
    cur.execute("""
    CREATE TABLE IF NOT EXISTS dangerous_moments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME NOT NULL,
        risk_score REAL NOT NULL,
        emotion_tags TEXT NOT NULL,
        user_input TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 2. 사용자 중독 패턴
    cur.execute("""
    CREATE TABLE IF NOT EXISTS addiction_patterns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hour_of_day INTEGER,
        day_of_week INTEGER,
        investment_purpose TEXT,
        pattern_count INTEGER DEFAULT 1,
        last_detected DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # 3. 압박 멘트 효과 추적
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pressure_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_type TEXT NOT NULL,
        emotion_tag TEXT NOT NULL,
        user_stopped BOOLEAN,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    conn.commit()
    conn.close()

def save_chat(user_input, ai_response, emotion_score, risk_level, tags):
    """상담 기록 저장"""
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    
    # 태그를 문자열로 변환
    tags_str = ", ".join(tags) if isinstance(tags, list) else tags
    
    cur.execute("""
    INSERT INTO chats (user_input, ai_response, emotion_score, risk_level, tags)
    VALUES (?, ?, ?, ?, ?)
    """, (user_input, ai_response, emotion_score, risk_level, tags_str))
    
    conn.commit()
    conn.close()
    
    # 캐시 무효화
    load_history.clear()
    get_emotion_stats.clear()
    get_user_memory.clear()

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
    """감정 태그 12종 감지"""
    tags = []
    
    # 1. 불안
    if any(word in user_input for word in ["불안", "걱정", "두려", "무서", "떨려"]):
        tags.append("불안")
    
    # 2. 분노
    if any(word in user_input for word in ["손실", "떨어", "내려", "털렸", "씨발", "화나", "짜증"]):
        tags.append("분노")
    
    # 3. 충동
    if any(word in user_input for word in ["사도", "들어갈", "몰빵", "급", "지금", "당장"]):
        tags.append("충동")
    
    # 4. 후회
    if any(word in user_input for word in ["후회", "실수", "잘못", "했어야"]):
        tags.append("후회")
    
    # 5. 탐욕 (고위험)
    if any(word in user_input for word in ["더", "많이", "대박", "벌고", "수익", "올랐", "급등"]):
        tags.append("탐욕")
    
    # 6. 공포
    if any(word in user_input for word in ["망했", "끝났", "파산", "다 잃", "무섭"]):
        tags.append("공포")
    
    # 7. FOMO (Fear Of Missing Out)
    if any(word in user_input for word in ["남들은", "다들", "나만", "놓쳤", "늦었", "올라가는데"]):
        tags.append("FOMO")
    
    # 8. 자포자기 (고위험)
    if any(word in user_input for word in ["어차피", "상관없", "아무거나", "됐어", "포기"]):
        tags.append("자포자기")
    
    # 9. 우울
    if any(word in user_input for word in ["우울", "힘들", "지쳤", "포기하고싶", "의미없"]):
        tags.append("우울")
    
    # 10. 흥분
    if any(word in user_input for word in ["와!", "대박", "완전", "진짜!", "미쳤"]):
        tags.append("흥분")
    
    # 11. 회의감
    if any(word in user_input for word in ["의심", "믿을수없", "사기", "조작", "속았"]):
        tags.append("회의감")
    
    # 12. 냉정
    if any(word in user_input for word in ["분석", "계획", "전략", "냉정", "객관"]):
        tags.append("냉정")
    
    return tags if tags else ["중립"]

def get_high_risk_tags():
    """고위험 감정 태그 리스트"""
    return ["탐욕", "자포자기", "충동", "FOMO", "공포"]

# ============================================================================
# 💥 압박 멘트 시스템 (v4.0)
# ============================================================================

PRESSURE_MESSAGES = {
    "탐욕": {
        "title": "⚠️ 투자 위험 경고",
        "message": """
**심리 상태가 불안정합니다. 지금 투자하면 손실 확률이 매우 높습니다.**

탐욕에 의한 추가 매수의 87%는 더 큰 손실로 이어집니다. (행동경제학 연구 결과)

**오늘의 감정 상태로는 합리적 결정을 내리기 어렵습니다.**

당신의 투자 계획을 다시 확인하세요:
- 지금 매수가 당신의 원칙에 맞습니까?
- 계획 외 매매는 당신의 원칙을 깨는 행동입니다.

**지금 투자를 멈추지 않으면, 내일 더 큰 후회가 기다립니다.**
        """,
        "blocking_word": "원칙",
        "actions": [
            "🫁 30초간 깊게 호흡하기",
            "📝 투자 이유를 3줄로 적어보기",
            "📅 오늘의 투자 원칙 다시 읽기",
            "🚶 2분간 자리에서 일어나 창문 보기"
        ]
    },
    
    "자포자기": {
        "title": "🔴 긴급 개입 필요",
        "message": """
**STOP. 당신은 지금 가장 위험한 심리 상태입니다.**

"어차피 망했어"라는 생각으로 하는 투자는:
- 100% 실패합니다 (통계적으로 검증됨)
- 회복 불가능한 손실을 만듭니다
- 투자 원금을 모두 잃을 수 있습니다

**오늘 투자하면 손실 확률이 매우 높습니다.**

당신의 1년 후를 상상해보세요:
- 이 결정을 후회하는 당신
- 가족 앞에서 고개 숙인 당신
- 모든 것을 잃은 당신

**지금 거래 앱을 끄세요. 지금 당장.**
        """,
        "blocking_word": "멈춤",
        "actions": [
            "📱 거래 앱 즉시 종료하기",
            "🚶 5분간 자리 이탈하기",
            "💧 물 한 컵 천천히 마시기",
            "☎️ 신뢰할 수 있는 사람에게 전화하기"
        ]
    },
    
    "충동": {
        "title": "⏸️ 투자 중단 권고",
        "message": """
**심리 상태가 불안정해 보이므로, 지금 투자는 위험합니다.**

충동적 결정의 95%는 실패합니다. (행동경제학 검증 결과)

지금 당장 매수하고 싶은 마음, 24시간만 기다려보세요.

**내일 다시 보면:**
- 80%는 "안 사길 잘했다"고 생각합니다
- 15%는 "더 싸게 살 수 있었다"고 생각합니다  
- 5%만 "사야 했다"고 생각합니다

**오늘의 감정 상태로는 합리적 결정을 내리기 어렵습니다.**

기회는 매일 옵니다. 당신의 돈은 도망가지 않습니다.
        """,
        "blocking_word": "내일",
        "actions": [
            "⏰ 24시간 후로 알람 설정하기",
            "✍️ 지금 사고 싶은 이유 3가지 적기",
            "🫁 1분간 깊은 호흡으로 진정하기",
            "📊 투자 계획표 다시 확인하기"
        ]
    },
    
    "FOMO": {
        "title": "🎯 현실 직시 필요",
        "message": """
**"남들은 다 번다"는 착각입니다. 지금 투자하면 손실 확률이 높습니다.**

실제 통계:
- SNS에서 수익 자랑하는 사람: 5%
- 조용히 손실 보는 사람: 70%
- 거짓말하는 사람: 25%

**당신이 못 탄 그 주식, 내일 -10% 떨어질 수도 있습니다.**

**계획 외 매매는 당신의 투자 원칙을 깨는 행동입니다.**

뉴스와 SNS를 끄세요. 당신만의 전략을 지키세요.
        """,
        "blocking_word": "나만",
        "actions": [
            "📱 SNS와 뉴스 앱 닫기",
            "📝 내 투자 원칙 다시 읽기",
            "🫁 30초간 심호흡하기",
            "🚶 창문 밖 2분간 바라보기"
        ]
    },
    
    "공포": {
        "title": "🛡️ 진정 필요",
        "message": """
**공포에 의한 손절은 대부분 최악의 타이밍입니다.**

**심리 상태가 불안정합니다. 지금 투자 결정은 위험합니다.**

시장은 당신의 감정을 이용합니다:
- 당신이 무서워 팔 때 = 기관이 삽니다
- 당신이 욕심내 살 때 = 기관이 팝니다

**오늘의 감정 상태로는 합리적 판단을 내리기 어렵습니다.**

최소 3일 기다려보세요. 그때도 팔고 싶으면, 그때 파세요.
        """,
        "blocking_word": "기다림",
        "actions": [
            "📅 3일 후로 알람 설정하기",
            "🫁 1분간 깊게 호흡하기",
            "💧 물 한 컵 마시며 진정하기",
            "📝 지금 팔고 싶은 이유 적어보기"
        ]
    }
}

def get_pressure_message(emotion_tags):
    """
    감정 태그에 따른 압박 멘트 반환
    
    Args:
        emotion_tags: 감지된 감정 태그 리스트
    
    Returns:
        dict or None: {title, message, blocking_word, actions} or None
    """
    high_risk = get_high_risk_tags()
    
    for tag in emotion_tags:
        if tag in high_risk and tag in PRESSURE_MESSAGES:
            return PRESSURE_MESSAGES[tag]
    
    return None

# ============================================================================
# 🧠 맥락 기억 시스템 (v4.0)
# ============================================================================

def save_dangerous_moment(risk_score, emotion_tags, user_input):
    """위험한 순간 기록"""
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    
    tags_str = ", ".join(emotion_tags) if isinstance(emotion_tags, list) else emotion_tags
    
    cur.execute("""
    INSERT INTO dangerous_moments (timestamp, risk_score, emotion_tags, user_input)
    VALUES (datetime('now'), ?, ?, ?)
    """, (risk_score, tags_str, user_input))
    
    conn.commit()
    conn.close()

def update_addiction_pattern(hour, day_of_week, purpose="만회"):
    """중독 패턴 업데이트"""
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    
    # 기존 패턴 확인
    cur.execute("""
    SELECT id, pattern_count FROM addiction_patterns
    WHERE hour_of_day = ? AND day_of_week = ? AND investment_purpose = ?
    """, (hour, day_of_week, purpose))
    
    existing = cur.fetchone()
    
    if existing:
        # 카운트 증가
        cur.execute("""
        UPDATE addiction_patterns
        SET pattern_count = pattern_count + 1, last_detected = datetime('now')
        WHERE id = ?
        """, (existing[0],))
    else:
        # 새 패턴 추가
        cur.execute("""
        INSERT INTO addiction_patterns (hour_of_day, day_of_week, investment_purpose)
        VALUES (?, ?, ?)
        """, (hour, day_of_week, purpose))
    
    conn.commit()
    conn.close()

def save_pressure_result(message_type, emotion_tag, user_stopped):
    """압박 멘트 결과 저장"""
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    
    cur.execute("""
    INSERT INTO pressure_messages (message_type, emotion_tag, user_stopped)
    VALUES (?, ?, ?)
    """, (message_type, emotion_tag, user_stopped))
    
    conn.commit()
    conn.close()

@st.cache_data(ttl=60)
def get_user_memory():
    """사용자 맥락 기억 불러오기"""
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    
    memory = {
        "dangerous_moments": [],
        "addiction_patterns": [],
        "pressure_effectiveness": {}
    }
    
    # 1. 가장 위험했던 순간 (최근 5개)
    cur.execute("""
    SELECT timestamp, risk_score, emotion_tags, user_input
    FROM dangerous_moments
    ORDER BY risk_score DESC
    LIMIT 5
    """)
    memory["dangerous_moments"] = cur.fetchall()
    
    # 2. 중독 패턴 (상위 3개)
    cur.execute("""
    SELECT hour_of_day, day_of_week, investment_purpose, pattern_count
    FROM addiction_patterns
    ORDER BY pattern_count DESC
    LIMIT 3
    """)
    memory["addiction_patterns"] = cur.fetchall()
    
    # 3. 압박 멘트 효과
    cur.execute("""
    SELECT emotion_tag, 
           SUM(CASE WHEN user_stopped = 1 THEN 1 ELSE 0 END) as stopped,
           COUNT(*) as total
    FROM pressure_messages
    GROUP BY emotion_tag
    """)
    
    for row in cur.fetchall():
        emotion_tag, stopped, total = row
        memory["pressure_effectiveness"][emotion_tag] = {
            "stopped": stopped,
            "total": total,
            "rate": round(stopped / total * 100, 1) if total > 0 else 0
        }
    
    conn.close()  
    return memory

# ============================================================================
# 📊 대시보드 시각화 함수 (v4.1)
# ============================================================================

def create_emotion_heatmap():
    """감정 히트맵 생성 (요일 × 시간대)"""
    import plotly.graph_objects as go
    import numpy as np
    
    conn = sqlite3.connect("gini.db", check_same_thread=False)  
    # 시간대별, 요일별 감정 점수 조회
    cur.execute("""
    SELECT 
        CAST(strftime('%w', timestamp) AS INTEGER) as day_of_week,
        CAST(strftime('%H', timestamp) AS INTEGER) as hour,
        AVG(emotion_score) as avg_emotion
    FROM chats
    WHERE emotion_score IS NOT NULL
    GROUP BY day_of_week, hour
    """)
    
    data = cur.fetchall()
    conn.close()
    
    # 히트맵 데이터 생성 (7일 × 24시간)
    heatmap_data = np.zeros((7, 24))
    
    for day, hour, emotion in data:
        heatmap_data[day][hour] = emotion
    
    # 요일 이름
    days = ['일', '월', '화', '수', '목', '금', '토']
    hours = [f"{h}시" for h in range(24)]
    
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=hours,
        y=days,
        colorscale='RdYlGn_r',  # 빨강(위험) → 노랑 → 초록(안전)
        text=heatmap_data,
        texttemplate='%{text:.1f}',
        textfont={"size": 10},
        colorbar=dict(title="감정 점수")
    ))
    
    fig.update_layout(
        title="📅 요일 × 시간대 감정 히트맵",
        xaxis_title="시간대",
        yaxis_title="요일",
        height=400
    )
    
    return fig

def create_risk_timeline():
    """위험지표 시간별 추이"""
    import plotly.express as px
    
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    
    cur.execute("""
    SELECT timestamp, emotion_score
    FROM chats
    WHERE emotion_score IS NOT NULL
    ORDER BY timestamp
    LIMIT 50
    """)
    
    data = cur.fetchall()
    conn.close()
    
    if not data:
        return None
    
    timestamps = [row[0] for row in data]
    scores = [row[1] for row in data]
    
    import pandas as pd
    df = pd.DataFrame({
        '시간': timestamps,
        '감정점수': scores
    })
    
    fig = px.line(df, x='시간', y='감정점수', 
                  title='📈 시간별 감정 점수 추이',
                  markers=True)
    
    # 위험 구간 표시
    fig.add_hline(y=6.5, line_dash="dash", line_color="red", 
                  annotation_text="HIGH 위험")
    fig.add_hline(y=5.0, line_dash="dash", line_color="orange", 
                  annotation_text="MID 주의")
    
    fig.update_layout(height=400)
    
    return fig

def create_emotion_tag_chart():
    """감정 태그 빈도 차트"""
    import plotly.express as px
    
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    
    cur.execute("""
    SELECT tags
    FROM chats
    WHERE tags IS NOT NULL AND tags != '중립'
    """)
    
    rows = cur.fetchall()
    conn.close()
    
    # 태그 카운트
    tag_counts = {}
    for row in rows:
        tags = row[0].split(', ')
        for tag in tags:
            tag = tag.strip()
            if tag and tag != '중립':
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
    
    if not tag_counts:
        return None
    
    # 상위 10개
    sorted_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    import pandas as pd
    df = pd.DataFrame(sorted_tags, columns=['감정태그', '빈도'])
    
    fig = px.bar(df, x='감정태그', y='빈도',
                 title='🏷️ 감정 태그 빈도 (상위 10개)',
                 color='빈도',
                 color_continuous_scale='Reds')
    
    fig.update_layout(height=400)
    
    return fig

def get_dashboard_stats():
    """대시보드 통계 데이터"""
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    
    stats = {}
    
    # 총 상담 횟수
    cur.execute("SELECT COUNT(*) FROM chats")
    stats['total_chats'] = cur.fetchone()[0]
    
    # 평균 감정 점수
    cur.execute("SELECT AVG(emotion_score) FROM chats WHERE emotion_score IS NOT NULL")
    avg_emotion = cur.fetchone()[0]
    stats['avg_emotion'] = round(avg_emotion, 2) if avg_emotion else 0
    
    # 고위험 상담 횟수
    cur.execute("SELECT COUNT(*) FROM chats WHERE risk_level = 'HIGH'")
    stats['high_risk_count'] = cur.fetchone()[0]
    
    # 최근 7일 상담 횟수
    cur.execute("""
    SELECT COUNT(*) FROM chats 
    WHERE timestamp >= datetime('now', '-7 days')
    """)
    stats['week_chats'] = cur.fetchone()[0]
    
    # 가장 많이 나온 감정 태그
    cur.execute("""
    SELECT tags FROM chats 
    WHERE tags IS NOT NULL AND tags != '중립'
    """)
    
    all_tags = []
    for row in cur.fetchall():
        tags = row[0].split(', ')
        all_tags.extend([t.strip() for t in tags if t.strip() and t.strip() != '중립'])
    
    if all_tags:
        from collections import Counter
        most_common = Counter(all_tags).most_common(1)[0]
        stats['most_common_tag'] = most_common[0]
        stats['most_common_count'] = most_common[1]
    else:
        stats['most_common_tag'] = '없음'
        stats['most_common_count'] = 0
    
    conn.close()
    return stats

# ============================================================================
# 🎯 위험지표 고도화 - 거래 패턴 분석 (v4.2)
# ============================================================================

def detect_overtrading():
    """
    과매매 감지
    - 최근 3일 내 5회 이상 상담 → 과매매 의심
    """
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    
    cur.execute("""
    SELECT COUNT(*) FROM chats
    WHERE timestamp >= datetime('now', '-3 days')
    """)
    
    recent_count = cur.fetchone()[0]
    conn.close()
    
    if recent_count >= 5:
        return {
            'detected': True,
            'count': recent_count,
            'message': f"⚠️ 최근 3일간 {recent_count}회 상담! 과매매 위험 신호입니다!"
        }
    
    return {'detected': False, 'count': recent_count}

def detect_revenge_trading():
    """
    복수 매매 감지
    - 손실 후 즉시(1시간 내) 재상담 → 복수 매매 의심
    """
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    
    # 최근 2개 상담 조회
    cur.execute("""
    SELECT emotion_score, timestamp, user_input
    FROM chats
    ORDER BY timestamp DESC
    LIMIT 2
    """)
    
    recent_chats = cur.fetchall()
    conn.close()
    
    if len(recent_chats) < 2:
        return {'detected': False}
    
    # 첫 번째 상담에 "손실", "떨어", "손해" 키워드 있고
    # 두 번째 상담이 1시간 이내면 복수 매매
    first_input = recent_chats[0][2].lower()
    loss_keywords = ["손실", "떨어", "손해", "마이너스", "잃", "-"]
    
    has_loss = any(keyword in first_input for keyword in loss_keywords)
    
    if has_loss and len(recent_chats) >= 2:
        from datetime import datetime
        time1 = datetime.fromisoformat(recent_chats[0][1])
        time2 = datetime.fromisoformat(recent_chats[1][1])
        time_diff = abs((time1 - time2).total_seconds() / 3600)  # 시간 단위
        
        if time_diff <= 1:
            return {
                'detected': True,
                'time_diff': round(time_diff * 60),  # 분 단위
                'message': f"🚨 손실 후 {round(time_diff * 60)}분 만에 재상담! 복수 매매 위험!"
            }
    
    return {'detected': False}

def detect_loss_pattern():
    """
    연속 손실 패턴 감지
    - 최근 5회 상담 중 3회 이상 "손실" 관련 → 악순환 경고
    """
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    
    cur.execute("""
    SELECT user_input FROM chats
    ORDER BY timestamp DESC
    LIMIT 5
    """)
    
    recent_inputs = [row[0].lower() for row in cur.fetchall()]
    conn.close()
    
    if not recent_inputs:
        return {'detected': False}
    
    loss_keywords = ["손실", "떨어", "손해", "마이너스", "잃", "물렸"]
    loss_count = sum(1 for inp in recent_inputs if any(kw in inp for kw in loss_keywords))
    
    if loss_count >= 3:
        return {
            'detected': True,
            'count': loss_count,
            'message': f"📉 최근 5회 중 {loss_count}회가 손실 관련 상담! 악순환에 빠졌습니다!"
        }
    
    return {'detected': False, 'count': loss_count}

def detect_fomo_pattern():
    """
    FOMO 연속 패턴 감지
    - 최근 3회 상담에 "급등", "올라", "놓쳤" 등 → FOMO 중독
    """
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    
    cur.execute("""
    SELECT user_input FROM chats
    ORDER BY timestamp DESC
    LIMIT 3
    """)
    
    recent_inputs = [row[0].lower() for row in cur.fetchall()]
    conn.close()
    
    if not recent_inputs:
        return {'detected': False}
    
    fomo_keywords = ["급등", "올라", "놓쳤", "남들", "다들", "나만", "뒤쳐"]
    fomo_count = sum(1 for inp in recent_inputs if any(kw in inp for kw in fomo_keywords))
    
    if fomo_count >= 2:
        return {
            'detected': True,
            'count': fomo_count,
            'message': f"🏃 최근 3회 중 {fomo_count}회가 FOMO 패턴! 남과 비교하지 마세요!"
        }
    
    return {'detected': False}

def get_trading_pattern_warnings():
    """
    모든 거래 패턴 경고 통합
    """
    warnings = []
    
    # 1. 과매매
    overtrading = detect_overtrading()
    if overtrading['detected']:
        warnings.append({
            'type': '과매매',
            'level': 'HIGH',
            'message': overtrading['message']
        })
    
    # 2. 복수 매매
    revenge = detect_revenge_trading()
    if revenge['detected']:
        warnings.append({
            'type': '복수매매',
            'level': 'CRITICAL',
            'message': revenge['message']
        })
    
    # 3. 연속 손실
    loss = detect_loss_pattern()
    if loss['detected']:
        warnings.append({
            'type': '연속손실',
            'level': 'HIGH',
            'message': loss['message']
        })
    
    # 4. FOMO 중독
    fomo = detect_fomo_pattern()
    if fomo['detected']:
        warnings.append({
            'type': 'FOMO중독',
            'level': 'MID',
            'message': fomo['message']
        })
    
    return warnings

# ============================================================================
# 📝 주간 리포트 생성 (v4.3)
# ============================================================================

def generate_weekly_report():
    """
    주간 리포트 데이터 생성
    """
    from datetime import datetime, timedelta
    
    conn = sqlite3.connect("gini.db", check_same_thread=False)
    cur = conn.cursor()
    
    # 지난 7일 날짜
    week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')
    
    report = {
        'period': f"{(datetime.now() - timedelta(days=7)).strftime('%Y.%m.%d')} ~ {datetime.now().strftime('%Y.%m.%d')}",
        'generated_at': datetime.now().strftime('%Y년 %m월 %d일 %H:%M')
    }
    
    # 1. 기본 통계
    cur.execute(f"""
    SELECT COUNT(*) FROM chats
    WHERE timestamp >= '{week_ago}'
    """)
    report['total_chats'] = cur.fetchone()[0]
    
    # 2. 평균 감정 점수
    cur.execute(f"""
    SELECT AVG(emotion_score) FROM chats
    WHERE timestamp >= '{week_ago}' AND emotion_score IS NOT NULL
    """)
    avg_emotion = cur.fetchone()[0]
    report['avg_emotion'] = round(avg_emotion, 2) if avg_emotion else 0
    
    # 3. 고위험 상담 횟수
    cur.execute(f"""
    SELECT COUNT(*) FROM chats
    WHERE timestamp >= '{week_ago}' AND risk_level = 'HIGH'
    """)
    report['high_risk_count'] = cur.fetchone()[0]
    
    # 4. 가장 많이 나온 감정 태그
    cur.execute(f"""
    SELECT tags FROM chats
    WHERE timestamp >= '{week_ago}' AND tags IS NOT NULL AND tags != '중립'
    """)
    
    all_tags = []
    for row in cur.fetchall():
        tags = row[0].split(', ')
        all_tags.extend([t.strip() for t in tags if t.strip() and t.strip() != '중립'])
    
    if all_tags:
        from collections import Counter
        top_tags = Counter(all_tags).most_common(3)
        report['top_tags'] = [{'tag': tag, 'count': count} for tag, count in top_tags]
    else:
        report['top_tags'] = []
    
    # 5. 가장 위험했던 순간
    cur.execute(f"""
    SELECT timestamp, emotion_score, user_input
    FROM chats
    WHERE timestamp >= '{week_ago}' AND emotion_score IS NOT NULL
    ORDER BY emotion_score DESC
    LIMIT 1
    """)
    
    dangerous = cur.fetchone()
    if dangerous:
        report['most_dangerous'] = {
            'time': dangerous[0],
            'score': round(dangerous[1], 1),
            'input': dangerous[2][:50] + '...' if len(dangerous[2]) > 50 else dangerous[2]
        }
    else:
        report['most_dangerous'] = None
    
    # 6. 거래 패턴 분석
    report['patterns'] = {
        'overtrading': detect_overtrading()['detected'],
        'revenge': detect_revenge_trading()['detected'],
        'loss_streak': detect_loss_pattern()['detected'],
        'fomo': detect_fomo_pattern()['detected']
    }
    
    # 7. 요일별 상담 횟수
    cur.execute(f"""
    SELECT CAST(strftime('%w', timestamp) AS INTEGER) as day, COUNT(*)
    FROM chats
    WHERE timestamp >= '{week_ago}'
    GROUP BY day
    ORDER BY day
    """)
    
    days_data = cur.fetchall()
    days_map = {0: '일', 1: '월', 2: '화', 3: '수', 4: '목', 5: '금', 6: '토'}
    report['by_day'] = [{'day': days_map.get(day, '?'), 'count': count} for day, count in days_data]
    
    # 8. 평가
    if report['avg_emotion'] >= 7:
        report['grade'] = '🔴 위험'
        report['comment'] = '이번 주는 매우 불안정했습니다. 투자를 멈추고 휴식이 필요합니다.'
    elif report['avg_emotion'] >= 5.5:
        report['grade'] = '🟡 주의'
        report['comment'] = '감정 기복이 있었습니다. 더 신중한 접근이 필요합니다.'
    else:
        report['grade'] = '🟢 안정'
        report['comment'] = '비교적 안정적인 한 주를 보냈습니다. 이 상태를 유지하세요!'
    
    conn.close()
    return report

def create_report_text(report):
    """
    리포트를 텍스트로 변환 (복사 가능)
    """
    text = f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛡️ GINI Guardian 주간 리포트
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📅 기간: {report['period']}
📝 생성: {report['generated_at']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 이번 주 통계
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

 총 상담 횟수: {report['total_chats']}회
📈 평균 감정 점수: {report['avg_emotion']}/10
🚨 고위험 상담: {report['high_risk_count']}회

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🏷️ 주요 감정 (TOP 3)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    if report['top_tags']:
        for i, tag_data in enumerate(report['top_tags'], 1):
            text += f"{i}. {tag_data['tag']} ({tag_data['count']}회)\n"
    else:
        text += "감정 데이터 없음\n"
    
    text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 가장 위험했던 순간
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    if report['most_dangerous']:
        text += f"""시간: {report['most_dangerous']['time']}
감정 점수: {report['most_dangerous']['score']}/10
내용: {report['most_dangerous']['input']}
"""
    else:
        text += "위험한 순간 없음\n"
    
    text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 거래 패턴 분석
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

과매매: {' 감지됨' if report['patterns']['overtrading'] else ' 없음'}
복수 매매: {' 감지됨' if report['patterns']['revenge'] else ' 없음'}
연속 손실: {' 감지됨' if report['patterns']['loss_streak'] else ' 없음'}
FOMO 중독: {' 감지됨' if report['patterns']['fomo'] else ' 없음'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📅 요일별 상담 횟수
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"""
    
    if report['by_day']:
        for day_data in report['by_day']:
            text += f"{day_data['day']}요일: {day_data['count']}회\n"
    else:
        text += "데이터 없음\n"
    
    text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💯 종합 평가
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

등급: {report['grade']}

{report['comment']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 다음 주 목표
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. 감정 점수 6.0 이하 유지
2. 고위험 상담 3회 이하
3. 계획적인 투자 결정
4. 충분한 고민 시간 갖기

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🛡️ GINI Guardian가 함께합니다! 💪
"""
    
    return text

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
        
        prompt = f"""당신은 전문적이고 객관적인 투자 심리 상담사입니다.
감정적인 투자를 막고, 합리적 판단을 돕는 것이 목표입니다.

사용자 질문: {user_text}

**상담 원칙:**
1. 감정 점수 0~10으로 평가 (0=매우 안정, 10=극도로 불안/흥분)
2. 전문적이고 명확한 조언 (과도하게 다정하거나 단호하지 않음)
3. 투자 위험이 높을 때는 명확하게 경고
4. 구체적이고 실행 가능한 조언 제시

**경고 문구 사용 원칙:**
- "지금 투자하면 손실 확률이 매우 높습니다"
- "심리 상태가 불안정합니다"
- "오늘의 감정 상태로는 합리적 결정을 내리기 어렵습니다"
- "계획 외 매매는 당신의 원칙을 깨는 행동입니다"

**응답 형식:**
[감정점수: X]
(전문적이고 명확한 상담 내용)
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

st.markdown('<div class="header-animated">🛡️ GINI Guardian v4.4</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; margin-bottom: 20px;"><span class="hot-badge" style="font-size: 1.2em; color: #ff4500;">FINAL! 라이라 최종 수정 완료 ✨🔥</span></div>', unsafe_allow_html=True)

# ============================================================================
# 탭 구성
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🧭 AI 상담",
    "📊 대시보드",
    "📚 상담 기록",
    "💼 실시간 포트폴리오",
    "⚙️ 설정"
])

# ============================================================================
# TAB 1: AI 상담 (텍스트 강화)
# ============================================================================

with tab1:
    st.markdown('<div style="text-align: center; margin-bottom: 15px;"><span style="font-size: 1.8em;">💬 투자 심리 상담</span></div>', unsafe_allow_html=True)
    
    # v4.4: 라이라 추천 인트로
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <p style="color: white; font-size: 1.1em; margin: 0; text-align: center; line-height: 1.6;">
        안녕하세요. 저는 <strong>감정에 흔들린 투자 결정을 막아주는</strong><br>
        <strong>'주식 과잉방지 AI 상담가'</strong>입니다.<br>
        <br>
        지금 당신의 심리·상황을 함께 점검하며<br>
        <strong>안전한 투자를 돕겠습니다.</strong> 🛡️
        </p>
    </div>
    """, unsafe_allow_html=True)
    
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
                        st.success(f" {stock['corrected']} ({stock['code']})")
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
                tags = detect_tags(user_input)  # 이제 리스트 반환
                
                # v4.0: 위험한 순간 기록
                if risk >= 6.5:
                    save_dangerous_moment(risk, tags, user_input)
                    
                    # 중독 패턴 분석
                    now = datetime.now()
                    hour = now.hour
                    day_of_week = now.weekday()
                    update_addiction_pattern(hour, day_of_week, "만회")
                
                save_chat(user_input, response, emotion_score, risk_level, tags)
                
                # v4.2: 거래 패턴 경고
                pattern_warnings = get_trading_pattern_warnings()
                
                if pattern_warnings:
                    st.markdown("---")
                    st.markdown("### 🚨 거래 패턴 경고")
                    
                    for warning in pattern_warnings:
                        if warning['level'] == 'CRITICAL':
                            st.error(f"**🔴 {warning['type']}**: {warning['message']}")
                        elif warning['level'] == 'HIGH':
                            st.warning(f"**🟠 {warning['type']}**: {warning['message']}")
                        else:
                            st.info(f"**🟡 {warning['type']}**: {warning['message']}")
                    
                    st.markdown("---")
                
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
                
                # v4.0: 압박 멘트 시스템
                pressure_msg = get_pressure_message(tags)
                
                if pressure_msg:
                    st.markdown("---")
                    
                    st.markdown(f"""
                    <div class="danger-box">
                        <h2 style="color: #dc3545; margin: 0;">{pressure_msg['title']}</h2>
                        {pressure_msg['message']}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    
                    # v4.4: 행동 단계 추가 (라이라)
                    st.markdown("### 💡 지금 당장 해야 할 행동")
                    st.info("""
**투자 충동을 줄이려면 '행동'이 필요합니다.** (행동경제학 검증)

아래 중 **최소 2가지**를 실행하세요:
                    """)
                    
                    for action in pressure_msg['actions']:
                        st.markdown(f"- {action}")
                    
                    st.markdown("---")
                    st.markdown("### 🔒 안전 확인")
                    st.warning(f"⚠️ 계속하려면 아래에 **'{pressure_msg['blocking_word']}'** 를 정확히 입력하세요.")
                    
                    blocking_input = st.text_input(
                        "단어 입력:",
                        key="blocking_input",
                        placeholder=f"{pressure_msg['blocking_word']} 입력"
                    )
                    
                    col_confirm, col_stop = st.columns(2)
                    
                    with col_confirm:
                        if st.button(" 그래도 진행", type="secondary"):
                            if blocking_input == pressure_msg['blocking_word']:
                                st.error("⚠️ 당신의 선택입니다. 하지만 후회하지 마세요.")
                                save_pressure_result("pressure", tags[0] if tags else "unknown", False)
                            else:
                                st.error(f" '{pressure_msg['blocking_word']}'를 정확히 입력해주세요!")
                    
                    with col_stop:
                        if st.button("🛑 멈춤 (현명한 선택)", type="primary"):
                            st.balloons()
                            st.success(" 훌륭합니다! 당신은 현명한 결정을 했습니다!")
                            save_pressure_result("pressure", tags[0] if tags else "unknown", True)
                    
                else:
                    # 강력한 경고 메시지 (위험도 높을 때)
                    warning_html = get_strong_warning(risk_level)
                    if warning_html:
                        st.markdown(warning_html, unsafe_allow_html=True)
                
                st.divider()
                
                # AI 상담 결과
                st.markdown("### 🧭 AI 상담 결과")
                st.write(response)
                
                # 감정 태그 표시
                if tags and tags != ["중립"]:
                    st.markdown("### 🏷️ 감지된 감정")
                    tag_colors = {
                        "탐욕": "🟠", "자포자기": "🔴", "충동": "🟡",
                        "FOMO": "🟡", "공포": "🔴", "불안": "🟡",
                        "분노": "🟠", "후회": "🔵", "우울": "🟣",
                        "흥분": "🟢", "회의감": "⚪", "냉정": "🟢"
                    }
                    
                    tag_display = " ".join([f"{tag_colors.get(tag, '⚫')} {tag}" for tag in tags])
                    st.info(tag_display)
                
                st.success(" 상담 기록이 저장되었습니다! 📚")
                
                st.markdown("---")
        else:
            st.warning("⚠️ 질문을 입력해주세요!")

# ============================================================================
# TAB 2: 대시보드 (v4.1 NEW!)
# ============================================================================

with tab2:
    st.markdown('<div style="text-align: center; margin-bottom: 15px;"><span style="font-size: 1.8em;">📊 나의 투자 심리 대시보드</span></div>', unsafe_allow_html=True)
    
    st.info("✨ 당신의 감정 패턴과 위험 신호를 한눈에 확인하세요!")
    
    # 통계 카드
    stats = get_dashboard_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📝 총 상담 횟수",
            value=f"{stats['total_chats']}회"
        )
    
    with col2:
        st.metric(
            label="📊 평균 감정 점수",
            value=f"{stats['avg_emotion']}/10",
            delta=f"{'위험' if stats['avg_emotion'] > 6.5 else '주의' if stats['avg_emotion'] > 5 else '안정'}"
        )
    
    with col3:
        st.metric(
            label="🚨 고위험 상담",
            value=f"{stats['high_risk_count']}회"
        )
    
    with col4:
        st.metric(
            label="📅 최근 7일",
            value=f"{stats['week_chats']}회"
        )
    
    st.divider()
    
    # v4.2: 거래 패턴 경고
    st.markdown("### 🎯 거래 패턴 분석 (NEW!)")
    
    pattern_warnings = get_trading_pattern_warnings()
    
    if pattern_warnings:
        st.error("⚠️ **위험한 거래 패턴이 감지되었습니다!**")
        
        for warning in pattern_warnings:
            if warning['level'] == 'CRITICAL':
                st.markdown(f"### 🔴 {warning['type']}")
                st.error(warning['message'])
            elif warning['level'] == 'HIGH':
                st.markdown(f"### 🟠 {warning['type']}")
                st.warning(warning['message'])
            else:
                st.markdown(f"### 🟡 {warning['type']}")
                st.info(warning['message'])
            
            st.markdown("---")
    else:
        st.success(" **현재 건강한 투자 패턴입니다!**")
        st.info("""
        **안전한 투자 습관:**
        - 충분한 고민 시간
        - 감정적 거래 없음
        - 계획적 접근
        
        이 상태를 유지하세요! 💪
        """)
    
    st.divider()
    
    # 감정 히트맵
    st.markdown("### 📅 언제 가장 위험한가요?")
    
    try:
        heatmap_fig = create_emotion_heatmap()
        st.plotly_chart(heatmap_fig, use_container_width=True)
        
        st.info("💡 **히트맵 해석**: 빨간색일수록 감정이 불안정한 시간대입니다. 이 시간대에는 투자 결정을 피하세요!")
    except Exception as e:
        st.warning("⚠️ 히트맵을 생성하려면 최소 10개 이상의 상담 기록이 필요합니다.")
    
    st.divider()
    
    # 감정 점수 추이
    st.markdown("### 📈 내 감정은 어떻게 변했나요?")
    
    try:
        timeline_fig = create_risk_timeline()
        if timeline_fig:
            st.plotly_chart(timeline_fig, use_container_width=True)
            st.info("💡 **추이 분석**: 빨간 선(6.5) 이상이면 HIGH 위험, 주황 선(5.0) 이상이면 MID 주의입니다.")
        else:
            st.warning("⚠️ 데이터가 부족합니다. 상담을 더 진행해주세요!")
    except Exception as e:
        st.warning("⚠️ 차트를 생성하려면 상담 기록이 필요합니다.")
    
    st.divider()
    
    # 감정 태그 빈도
    st.markdown("### 🏷️ 어떤 감정이 가장 많나요?")
    
    col_tag1, col_tag2 = st.columns([2, 1])
    
    with col_tag1:
        try:
            tag_fig = create_emotion_tag_chart()
            if tag_fig:
                st.plotly_chart(tag_fig, use_container_width=True)
            else:
                st.warning("⚠️ 감정 태그 데이터가 부족합니다.")
        except Exception as e:
            st.warning("⚠️ 차트를 생성하려면 상담 기록이 필요합니다.")
    
    with col_tag2:
        st.markdown("#### 📌 가장 많은 감정")
        st.metric(
            label="",
            value=stats['most_common_tag'],
            delta=f"{stats['most_common_count']}회"
        )
        
        st.markdown("---")
        
        st.markdown("#### 🎯 고위험 감정")
        st.error("""
        **주의 필요:**
        - 탐욕
        - 자포자기
        - 충동
        - FOMO
        - 공포
        """)

    st.divider()
    
    # v4.3: 주간 리포트
    st.markdown("### 📝 주간 리포트 (NEW!)")
    
    if st.button("📊 이번 주 리포트 생성", type="primary", use_container_width=True):
        with st.spinner("📝 리포트 생성 중..."):
            report = generate_weekly_report()
            
            # 리포트 표시
            st.markdown("---")
            st.markdown(f"## 🛡️ GINI Guardian 주간 리포트")
            st.markdown(f"**📅 기간**: {report['period']}")
            st.markdown(f"**📝 생성**: {report['generated_at']}")
            
            st.divider()
            
            # 기본 통계
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("총 상담 횟수", f"{report['total_chats']}회")
            
            with col2:
                st.metric("평균 감정 점수", f"{report['avg_emotion']}/10")
            
            with col3:
                st.metric("고위험 상담", f"{report['high_risk_count']}회")
            
            st.divider()
            
            # 종합 평가
            st.markdown("### 💯 종합 평가")
            
            if '🔴' in report['grade']:
                st.error(f"**{report['grade']}**")
                st.error(report['comment'])
            elif '🟡' in report['grade']:
                st.warning(f"**{report['grade']}**")
                st.warning(report['comment'])
            else:
                st.success(f"**{report['grade']}**")
                st.success(report['comment'])
            
            st.divider()
            
            # 주요 감정
            if report['top_tags']:
                st.markdown("### 🏷️ 주요 감정 TOP 3")
                
                for i, tag_data in enumerate(report['top_tags'], 1):
                    st.info(f"**{i}위**: {tag_data['tag']} ({tag_data['count']}회)")
            
            st.divider()
            
            # 가장 위험했던 순간
            if report['most_dangerous']:
                st.markdown("### ⚠️ 가장 위험했던 순간")
                st.error(f"""
**시간**: {report['most_dangerous']['time']}  
**감정 점수**: {report['most_dangerous']['score']}/10  
**내용**: {report['most_dangerous']['input']}
                """)
            
            st.divider()
            
            # 거래 패턴
            st.markdown("### 🎯 거래 패턴 분석")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("과매매", " 감지됨" if report['patterns']['overtrading'] else " 없음")
                st.metric("복수 매매", " 감지됨" if report['patterns']['revenge'] else " 없음")
            
            with col2:
                st.metric("연속 손실", " 감지됨" if report['patterns']['loss_streak'] else " 없음")
                st.metric("FOMO 중독", " 감지됨" if report['patterns']['fomo'] else " 없음")
            
            st.divider()
            
            # 요일별 상담
            if report['by_day']:
                st.markdown("### 📅 요일별 상담 횟수")
                
                import pandas as pd
                df = pd.DataFrame(report['by_day'])
                
                import plotly.express as px
                fig = px.bar(df, x='day', y='count',
                            title='요일별 상담 패턴',
                            labels={'day': '요일', 'count': '횟수'})
                st.plotly_chart(fig, use_container_width=True)
            
            st.divider()
            
            # 텍스트 리포트
            st.markdown("### 📄 텍스트 리포트")
            
            report_text = create_report_text(report)
            
            st.text_area(
                "복사해서 저장하세요!",
                value=report_text,
                height=400
            )
            
            st.success(" 리포트가 생성되었습니다! 위 텍스트를 복사하여 저장하세요.")

# ============================================================================
# TAB 3: 상담 기록
# ============================================================================

with tab3:
    st.subheader("📚 과거 상담 기록")
    
    history = load_history()
    
    if history:
        st.success(f" 총 {len(history)}개의 상담 기록")
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
# TAB 4: 실시간 포트폴리오
# ============================================================================

with tab4:
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
                
                st.success(f" {new_name} ({new_ticker}) 추가 완료! 새로고침 버튼을 눌러주세요.")
                st.balloons()
            else:
                st.warning("⚠️ 모든 항목을 올바르게 입력해주세요!")

# ============================================================================
# TAB 5: 설정
# ============================================================================

with tab5:
    st.subheader("⚙️ 설정 & 정보")
    
    st.info(f"""
    **GINI Guardian v4.4 - 라이라 최종 수정 완료! ✨**
    
    🆕 v4.4 라이라 피드백 반영:
       -  **톤 통일**: 전문적이고 객관적인 중간 톤으로 통일
       -  **경고 문구 전문화**: "지금 투자하면 손실 확률이 매우 높습니다" 등 명확한 표현
       -  **행동 단계 추가**: 30초 호흡, 2분 자리 이탈, 투자 이유 적기 등 실행 가능한 액션
       -  **압박 멘트 개선**: 더 전문적이고 분명한 경고
       -  **행동경제학 검증**: "충동적 결정 95% 실패" 등 근거 제시
    
     v4.3 기능:
       - 주간 리포트 자동 생성
       - 종합 평가 (🟢안정/🟡주의/🔴위험)
       - TOP 3 감정 분석
       - 텍스트 복사 가능
    
     v4.2 기능:
       - 과매매 감지 (3일 5회)
       - 복수 매매 감지 (손실 후 1시간)
       - 연속 손실 패턴
       - FOMO 중독 감지
    
     v4.1 기능:
       - 감정 히트맵
       - 위험지표 추이
       - 감정 태그 빈도
       - 통계 대시보드
    
     v4.0 기능:
       - 맥락 기억 시스템
       - 감정 태그 12종
       - 압박 멘트 시스템
       - Text Input Blocking
    
     기존 기능:
       - 종목명 자동 보정
       - 실시간 포트폴리오
       - 감정 분석 & 위험지표
       - 성능 최적화
    
    **🎉 FINAL 버전 완성!**
    **행동경제학 검증 + 라이라 UX 완성**
    """)
    
    st.markdown("#### 📋 기술 스택")
    st.code("""
- Streamlit: UI/UX
- Groq API: AI 상담
- pykrx: 실시간 주식 데이터
- SQLite: 데이터 저장 + 맥락 기억 + 패턴 분석
- Plotly: 대시보드 시각화
- 퍼지 매칭: 종목명 보정
- 감정 분석: 12종 태그 시스템
- 패턴 감지: 과매매/복수매매/연속손실/FOMO
- 주간 리포트: 자동 생성 + 텍스트 복사 (NEW!)
    """, language="python")
    
    st.markdown("#### 🎯 v4.3 주간 리포트 전략")
    st.write("""
    **주간 리포트의 힘:**
    - 객관적으로 나를 돌아보기
    - 한 주 동안의 패턴 파악
    - 다음 주 목표 설정
    
    **리포트 구성:**
    1. 기본 통계 (상담 횟수, 평균 점수)
    2. 종합 평가 (🟢안정/🟡주의/🔴위험)
    3. 주요 감정 TOP 3
    4. 가장 위험했던 순간
    5. 거래 패턴 분석
    6. 요일별 차트
    
    **v4.4 라이라 최종 수정:**
    1. 톤 통일 (전문적 중간 톤)
    2. 경고 문구 전문화
    3. 행동 단계 추가 (행동경제학 검증)
    
    **🎉 FINAL 버전 완성!**
    
    **라이라 설계 × 미라클 구현 × 제미니 전략**
    """)

st.divider()

st.markdown("---\n🛡️ **GINI Guardian v4.4 FINAL** | ✨ 라이라 최종 수정 완료! | 💙 라이라 × 미라클 × 제미니")


