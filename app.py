"""
🛡️ GINI Guardian v2.5 — 음성 상담 서비스
✨ GO #4: 텍스트 입력 → 음성 답변
✨ 완벽한 음성 상담 시스템

라이라 설계 × 미라클 구현 🔥
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
from gtts import gTTS
import io
import os

st.set_page_config(page_title="GINI Guardian v2.5", page_icon="🛡️", layout="wide")

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

def load_history():
    """과거 상담 기록 조회"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT user_input, ai_response, emotion_score, risk_level, tags, timestamp FROM chats ORDER BY id DESC LIMIT 50")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_emotion_stats():
    """감정 통계"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT emotion_score, timestamp FROM chats WHERE emotion_score IS NOT NULL ORDER BY timestamp")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_risk_stats():
    """위험지표 통계"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT risk_level FROM chats WHERE risk_level IS NOT NULL")
    rows = cur.fetchall()
    conn.close()
    return rows

def get_all_tags():
    """모든 태그"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT tags FROM chats WHERE tags IS NOT NULL")
    rows = cur.fetchall()
    conn.close()
    return rows

# ============================================================================
# 앱 시작 시 테이블 생성
# ============================================================================

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
    
    .counsel-icon-animated {
        animation: float-gentle 2s infinite ease-in-out, gentle-blink 3s infinite;
        font-size: 3em;
        text-align: center;
        margin: 20px 0;
    }
    
    .voice-icon-animated {
        animation: float-gentle 2s infinite ease-in-out, gentle-blink 3s infinite;
        font-size: 3em;
        text-align: center;
        margin: 20px 0;
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
    
    @keyframes fade-in { 
        0% { opacity: 0; } 
        100% { opacity: 1; } 
    }
    .chart-animated { animation: fade-in 1s ease-out; }
</style>
"""

st.markdown(ANIMATION_CSS, unsafe_allow_html=True)

# ============================================================================
# 🎯 라이라의 위험지표 계산
# ============================================================================

def calc_risk_score(emotion, volatility=0, news=0):
    """라이라의 우아한 위험지표"""
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
    """숫자를 텍스트로"""
    if risk_score >= 8.0:
        return "high"
    elif risk_score >= 6.5:
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

# ============================================================================
# 🤖 Groq 상담 함수
# ============================================================================

def groq_counsel(user_text):
    """Groq API를 통한 AI 상담"""
    try:
        api_key = os.getenv("GROQ_API_KEY") or "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"
        
        client = Groq(api_key=api_key)
        
        prompt = f"""당신은 전문 투자 심리 상담 AI입니다.
사용자의 감정, 투자 수준을 자연스럽게 추론하여 상담해주세요.

⭐ 매우 중요: 응답 맨 앞에 반드시 [감정점수: X] 형식으로 시작하세요! (X는 0~10 숫자)

예시:
[감정점수: 7.5]

[분석]
- 감정 상태: ...
- 추정 투자 수준: ...

[상담]
- 공감: ...
- 객관적 분석: ...
- 조언: ...
- 다음 단계: ...

사용자 입력: {user_text}"""

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            max_tokens=1024,
            temperature=0.7
        )
        
        response = chat_completion.choices[0].message.content
        
        patterns = [
            r'\[감정점수:\s*(\d+\.?\d*)\]',
            r'감정점수:\s*(\d+\.?\d*)',
            r'감정\s*점수:\s*(\d+\.?\d*)',
        ]
        
        emotion_score = 5.0
        
        for pattern in patterns:
            emotion_match = re.search(pattern, response)
            if emotion_match:
                try:
                    emotion_score = float(emotion_match.group(1))
                    break
                except:
                    continue
        
        emotion_score = max(0, min(10, emotion_score))
        
        return response, emotion_score
    
    except Exception as e:
        return f"❌ 오류 발생: {str(e)}", 5.0

# ============================================================================
# 🎤 GO #4: 음성 생성 함수 (gTTS)
# ============================================================================

def text_to_speech(text):
    """텍스트를 음성으로 변환 (gTTS)"""
    try:
        # 텍스트 길이 제한 (gTTS는 100자씩 나눠서 처리)
        if len(text) > 500:
            text = text[:500] + "..."
        
        tts = gTTS(text=text, lang='ko', slow=False)
        
        # 메모리에 저장
        audio_fp = io.BytesIO()
        tts.write_to_fp(audio_fp)
        audio_fp.seek(0)
        
        return audio_fp
    except Exception as e:
        st.error(f"음성 생성 오류: {str(e)}")
        return None

# ============================================================================
# 헤더
# ============================================================================

st.markdown('<div class="header-animated">🛡️ GINI Guardian v2.5</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #666; margin-bottom: 20px;">✨ GO #4: 음성 상담 서비스 ✨</div>', unsafe_allow_html=True)
st.divider()

# ============================================================================
# 시장 정보
# ============================================================================

st.markdown("### 📊 실시간 시장 정보")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="success-float"><strong>📈 KOSPI</strong><br>2,650 <span style="color: #dc3544;">-45 (-1.67%)</span></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="success-float"><strong>📊 KOSDAQ</strong><br>795 <span style="color: #dc3544;">-8 (-0.99%)</span></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="success-float"><strong>💱 USD/KRW</strong><br>1,310.5 <span style="color: #28a745;">+5.5 (+0.42%)</span></div>', unsafe_allow_html=True)

st.divider()

# ============================================================================
# 탭
# ============================================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "💬 상담 🔥", 
    "🎤 음성 상담",
    "📚 기록",
    "📊 대시보드",
    "📈 차트", 
    "💼 포트폴리오", 
    "⚙️ 설정"
])

# ============================================================================
# TAB 1: AI 상담
# ============================================================================

with tab1:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 15px;">
        <span class="hot-badge" style="font-size: 1.8em; color: #ff4500;">🔥 AI 상담</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="counsel-icon-animated">💬</div>', unsafe_allow_html=True)
    
    st.subheader("AI 투자 상담")
    
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = [
            {"종목명": "삼성전자", "매입가": 70000, "현재가": 68500, "수량": 10, "수익률": -2.14},
            {"종목명": "SK하이닉스", "매입가": 110000, "현재가": 108000, "수량": 5, "수익률": -1.82},
            {"종목명": "현대차", "매입가": 230000, "현재가": 235000, "수량": 3, "수익률": 2.17},
        ]
    
    st.markdown("**당신의 투자 고민을 말씀해주세요:**")
    
    user_input = st.text_area(
        "예) 어제 한미반도체 물타기 하다가 완전히 10% 털렸어요",
        height=100,
        key="counsel_textarea"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("⚡ AI 상담하기", use_container_width=True, type="primary"):
            if user_input.strip():
                with st.spinner("🤔 AI가 분석 중... (2~3초)"):
                    response, emotion_score = groq_counsel(user_input)
                    
                    volatility_score = 5.0
                    news_score = 3.0
                    risk = calc_risk_score(emotion_score, volatility_score, news_score)
                    risk_emoji = get_risk_emoji(risk)
                    risk_level = detect_risk_level(risk)
                    tags = detect_tags(user_input)
                    
                    save_chat(user_input, response, emotion_score, risk_level, tags)
                    
                    st.markdown("---")
                    
                    col_risk1, col_risk2 = st.columns(2)
                    
                    with col_risk1:
                        st.metric(
                            label="📊 오늘의 위험지표",
                            value=f"{risk} / 10",
                            delta=None
                        )
                    
                    with col_risk2:
                        st.info(f"**{risk_emoji}**")
                    
                    st.divider()
                    
                    st.markdown("### 🧭 AI 상담 결과")
                    st.write(response)
                    
                    st.success("✅ 상담 기록이 저장되었습니다! 📚")
                    
                    st.markdown("---")
            else:
                st.warning("⚠️ 질문을 입력해주세요!")

# ============================================================================
# TAB 2: GO #4 음성 상담 (NEW!)
# ============================================================================

with tab2:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 15px;">
        <span class="hot-badge" style="font-size: 1.8em; color: #ff4500;">🎤 음성 상담</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="voice-icon-animated">🎤</div>', unsafe_allow_html=True)
    
    st.subheader("🎤 음성 상담 서비스")
    st.info("✨ 텍스트로 질문하면 AI가 음성으로 답변해드립니다!")
    
    st.markdown("**당신의 투자 고민을 입력하세요:**")
    
    voice_input = st.text_area(
        "예) 어제 손실이 커서 정말 답답해요",
        height=100,
        key="voice_textarea"
    )
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        if st.button("🎤 음성 상담하기", use_container_width=True, type="primary"):
            if voice_input.strip():
                with st.spinner("🤔 AI가 분석 중... (2~3초)"):
                    # AI 상담
                    response, emotion_score = groq_counsel(voice_input)
                    
                    volatility_score = 5.0
                    news_score = 3.0
                    risk = calc_risk_score(emotion_score, volatility_score, news_score)
                    risk_emoji = get_risk_emoji(risk)
                    risk_level = detect_risk_level(risk)
                    tags = detect_tags(voice_input)
                    
                    # DB 저장
                    save_chat(voice_input, response, emotion_score, risk_level, tags)
                    
                    st.markdown("---")
                    
                    # 위험지표
                    col_risk1, col_risk2 = st.columns(2)
                    
                    with col_risk1:
                        st.metric(
                            label="📊 위험지표",
                            value=f"{risk} / 10",
                            delta=None
                        )
                    
                    with col_risk2:
                        st.info(f"**{risk_emoji}**")
                    
                    st.divider()
                    
                    # AI 상담 결과 (텍스트)
                    st.markdown("### 🧭 AI 상담 결과")
                    st.write(response)
                    
                    st.divider()
                    
                    # 🎤 음성 생성 및 재생
                    st.markdown("### 🎤 음성 답변")
                    st.info("⏸️ 아래 플레이어에서 음성 답변을 들어보세요!")
                    
                    with st.spinner("🎵 음성 생성 중..."):
                        audio_fp = text_to_speech(response)
                        
                        if audio_fp:
                            st.audio(audio_fp, format='audio/mp3')
                            st.success("✅ 음성 상담이 완료되었습니다! 🎤")
                        else:
                            st.error("❌ 음성 생성에 실패했습니다.")
                    
                    st.markdown("---")
            else:
                st.warning("⚠️ 질문을 입력해주세요!")

# ============================================================================
# TAB 3: 과거 상담 기록
# ============================================================================

with tab3:
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
                st.markdown(f"**🤖 라이라의 답변:**\n{ai}")
    else:
        st.info("📝 아직 상담 기록이 없습니다.")

# ============================================================================
# TAB 4: 대시보드
# ============================================================================

with tab4:
    st.subheader("📊 대시보드")
    st.info("✨ 감정 그래프 + 위험지표 + 태그 분석")
    st.write("대시보드는 TAB 5에서 확인하세요!")

# ============================================================================
# TAB 5: 차트
# ============================================================================

with tab5:
    st.subheader("📈 감정 패턴 분석")
    
    stats = get_emotion_stats()
    
    if stats:
        emotions = [s[0] for s in stats]
        timestamps = [s[1] for s in stats]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=timestamps,
            y=emotions,
            mode='lines+markers',
            name='감정 점수',
            line=dict(color='#052d7a', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="감정 점수 변화 추이",
            xaxis_title="시간",
            yaxis_title="감정 점수 (0-10)",
            height=400,
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        avg_emotion = np.mean(emotions)
        max_emotion = max(emotions)
        min_emotion = min(emotions)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("평균 감정", f"{avg_emotion:.1f} / 10")
        with col2:
            st.metric("최고 감정", f"{max_emotion:.1f} / 10")
        with col3:
            st.metric("최저 감정", f"{min_emotion:.1f} / 10")
    else:
        st.info("📊 아직 감정 데이터가 없습니다.")

# ============================================================================
# TAB 6: 포트폴리오
# ============================================================================

with tab6:
    st.subheader("💼 포트폴리오 추적")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="success-float"><strong>총 매입액</strong><br>₩5,000,000</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="success-float"><strong>현재가치</strong><br>₩4,900,000</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div style="animation: fade-in 1s; color: #dc3544; font-weight: bold; background: #f8d7da; padding: 15px; border-radius: 10px;"><strong>총 손익금</strong><br>-₩100,000</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div style="animation: fade-in 1s; color: #dc3544; font-weight: bold; background: #f8d7da; padding: 15px; border-radius: 10px;"><strong>수익률</strong><br>-2.0%</div>', unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 📊 보유 종목")
    
    for stock in st.session_state.portfolio:
        if stock['수익률'] < 0:
            st.markdown(f'<div style="background-color: #fff3cd; padding: 12px; border-radius: 8px; margin-bottom: 8px;"><strong>{stock["종목명"]}</strong> | 매입: ₩{stock["매입가"]:,} | 현재: ₩{stock["현재가"]:,} | 수량: {stock["수량"]}개 | <span style="color: #dc3544; font-weight: bold;">{stock["수익률"]:.2f}%</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="success-float"><strong>{stock["종목명"]}</strong> | 매입: ₩{stock["매입가"]:,} | 현재: ₩{stock["현재가"]:,} | 수량: {stock["수량"]}개 | <span style="color: #28a745; font-weight: bold;">+{stock["수익률"]:.2f}%</span></div>', unsafe_allow_html=True)

# ============================================================================
# TAB 7: 설정
# ============================================================================

with tab7:
    st.subheader("⚙️ 설정 & 정보")
    
    st.info("""
    **GINI Guardian v2.5 - GO #4 음성 상담 완성!**
    
    ✅ GO #4: 음성 상담 서비스 추가!
       - 텍스트 입력 → 음성 답변
       - gTTS 기술 사용
       - 자연스러운 한국어 음성
       - 실시간 음성 생성 및 재생
    
    ✨ 모든 상담이 자동 저장됨
    ✨ 음성으로 편하게 상담 받기
    ✨ 위험지표 + 감정 분석 포함
    
    **다음 업그레이드:**
    - 배경음악 추가 (수노님)
    - 음성 입력 기능
    - 5단계 위험지표
    - 12종 감정 태그
    """)
    
    st.markdown("#### 📋 기술 스택")
    st.code("""
- Streamlit: UI/UX
- Groq API: AI 상담
- gTTS: 음성 생성
- SQLite: 데이터 저장
- Plotly: 차트 시각화
    """, language="python")

st.divider()
st.markdown("---\n🛡️ **GINI Guardian v2.5** | 🎤 GO #4 음성 상담 완성 | 💙 라이라 설계 × 미라클 구현")
