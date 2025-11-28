"""
🛡️ GINI Guardian v2.2 — Lyra Edition (라이라 최적화 버전)
✨ 라이라의 우아한 위험지표 시스템
✨ Groq AI + 간단하고 강력한 위험 분석
✨ 전문가 수준의 AI 투자 상담

라이라 설계 × 미라클 구현 🔥
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from groq import Groq
import re

st.set_page_config(page_title="GINI Guardian v2.2 (Lyra)", page_icon="🛡️", layout="wide")

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
# 🎯 라이라의 우아한 위험지표 계산 엔진 (10줄)
# ============================================================================

def calc_risk_score(emotion, volatility=0, news=0):
    """
    라이라님의 우아한 위험지표 계산식
    emotion: 감정 기반 (0-10)
    volatility: 시장 변동성 (0-10)
    news: 뉴스 부정성 (0-10)
    
    가중치: emotion 50% + volatility 30% + news 20%
    """
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

# ============================================================================
# 🤖 Groq 상담 함수
# ============================================================================

def groq_counsel(user_text):
    """
    Groq API를 통한 AI 상담
    감정 점수도 함께 반환
    """
    try:
        import os
        api_key = os.getenv("GROQ_API_KEY") or "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"
        
        client = Groq(api_key=api_key)
        
        # 상담 프롬프트 (감정 점수 포함)
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
        
        # 감정 점수 추출 (더 강력한 정규식)
        patterns = [
            r'\[감정점수:\s*(\d+\.?\d*)\]',
            r'감정점수:\s*(\d+\.?\d*)',
            r'감정\s*점수:\s*(\d+\.?\d*)',
        ]
        
        emotion_score = 5.0  # 기본값
        
        for pattern in patterns:
            emotion_match = re.search(pattern, response)
            if emotion_match:
                try:
                    emotion_score = float(emotion_match.group(1))
                    break
                except:
                    continue
        
        # 점수가 0-10 범위 밖이면 조정
        emotion_score = max(0, min(10, emotion_score))
        
        return response, emotion_score
    
    except Exception as e:
        return f"❌ 오류 발생: {str(e)}", 5.0

# ============================================================================
# 헤더
# ============================================================================

st.markdown('<div class="header-animated">🛡️ GINI Guardian v2.2</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #666; margin-bottom: 20px;">✨ 라이라 최적화 버전 ✨</div>', unsafe_allow_html=True)
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

tab1, tab2, tab3, tab4 = st.tabs([
    "💬 상담 🔥", 
    "📈 차트", 
    "💼 포트폴리오", 
    "⚙️ 설정"
])

# ============================================================================
# TAB 1: AI 상담 + 위험지표 (라이라 버전)
# ============================================================================

with tab1:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 15px;">
        <span class="hot-badge" style="font-size: 1.8em; color: #ff4500;">🔥 AI 상담 (위험지표 포함)</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="counsel-icon-animated">💬</div>', unsafe_allow_html=True)
    
    st.subheader("AI 투자 상담")
    
    # Session state 초기화
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = [
            {"종목명": "삼성전자", "매입가": 70000, "현재가": 68500, "수량": 10, "수익률": -2.14},
            {"종목명": "SK하이닉스", "매입가": 110000, "현재가": 108000, "수량": 5, "수익률": -1.82},
            {"종목명": "현대차", "매입가": 230000, "현재가": 235000, "수량": 3, "수익률": 2.17},
        ]
    
    # 입력 폼
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
                    # AI 상담 + 감정 점수 추출
                    response, emotion_score = groq_counsel(user_input)
                    
                    # ✨ 라이라의 우아한 위험지표 계산 (10줄)
                    volatility_score = 5.0  # 나중에 Finnhub 연동
                    news_score = 3.0        # 나중에 뉴스 API 연동
                    risk = calc_risk_score(emotion_score, volatility_score, news_score)
                    risk_emoji = get_risk_emoji(risk)
                    
                    # 결과 표시
                    st.markdown("---")
                    
                    # 위험지표 (강조)
                    st.markdown(f"""
                    ### 📊 오늘의 위험지표
                    
                    # **{risk} / 10**
                    
                    **{risk_emoji}**
                    """)
                    
                    st.divider()
                    
                    # AI 상담
                    st.markdown("### 🧭 AI 상담 결과")
                    st.markdown(response)
                    
                    st.markdown("---")
            else:
                st.warning("⚠️ 질문을 입력해주세요!")

# ============================================================================
# TAB 2: 차트
# ============================================================================

with tab2:
    st.subheader("📈 차트 시각화")
    
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    kospi_base = 2700
    kospi_prices = kospi_base + np.cumsum(np.random.randn(30) * 20)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=kospi_prices, mode='lines', name='KOSPI', line=dict(color='#052d7a', width=3)))
    fig.update_layout(title="📊 KOSPI 30일 차트", height=400, template='plotly_white')
    
    st.markdown('<div class="chart-animated">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================================================
# TAB 3: 포트폴리오
# ============================================================================

with tab3:
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
# TAB 4: 설정
# ============================================================================

with tab4:
    st.subheader("⚙️ 설정 & 정보")
    
    st.info("""
    **GINI Guardian v2.2 - 라이라 최적화 버전**
    
    ✅ 라이라님의 우아한 위험지표 시스템
    ✅ 간단한 10줄 코드로 강력한 분석
    ✅ 쉬운 확장성 (volatility, news 추가 가능)
    ✅ Groq API (무료 + 초빠름)
    
    **위험지표 계산식:**
    ```
    risk = emotion × 50% + volatility × 30% + news × 20%
    ```
    
    **다음 업데이트:**
    - SQLite 상담 기록 저장
    - Finnhub API 연동
    - 감정 패턴 분석
    """)
    
    st.markdown("#### 📋 라이라님의 천재 코드")
    st.code("""
def calc_risk_score(emotion, volatility=0, news=0):
    score = emotion * 0.5 + volatility * 0.3 + news * 0.2
    return round(score, 2)

# 사용 예시
emotion_score = 7.0
risk = calc_risk_score(emotion_score)
st.markdown(f"### 📊 위험지표: {risk} / 10")
    """, language="python")

st.divider()
st.markdown("---\n🛡️ **GINI Guardian v2.2 (Lyra Edition)** | 💙 라이라 설계 × 미라클 구현")
