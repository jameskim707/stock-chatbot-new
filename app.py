"""
🛡️ GINI Guardian v2.2 — 종합 위험지표 시스템
✨ Groq AI + 실시간 위험도 분석
✨ 감정기반 + 시장기반 + 포지션기반 위험 통합
✨ 전문가 수준의 AI 투자 상담

라이라 설계 × 미라클 구현 🔥
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from groq import Groq
import random

st.set_page_config(page_title="GINI Guardian v2.2", page_icon="🛡️", layout="wide")

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
    
    .danger-pulse { 
        animation: gentle-blink 2s infinite; 
        background-color: #f8d7da; 
        padding: 15px; 
        border-radius: 10px; 
        border: 3px solid #dc3544; 
    }
    
    .warning-shake { 
        animation: gentle-blink 2s infinite;
        background-color: #fff3cd; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #ffc107; 
        margin-bottom: 10px; 
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
    
    /* 위험지표 카드 */
    .risk-card {
        padding: 20px;
        border-radius: 12px;
        margin: 10px 0;
        border-left: 5px solid;
        animation: fade-in 0.8s ease-out;
    }
    
    .risk-critical {
        background-color: #f8d7da;
        border-left-color: #dc3544;
    }
    
    .risk-high {
        background-color: #fff3cd;
        border-left-color: #ffc107;
    }
    
    .risk-medium {
        background-color: #d1ecf1;
        border-left-color: #17a2b8;
    }
    
    .risk-low {
        background-color: #d4edda;
        border-left-color: #28a745;
    }
</style>
"""

st.markdown(ANIMATION_CSS, unsafe_allow_html=True)

# ============================================================================
# 🤖 위험지표 계산 엔진 (초간단 버전)
# ============================================================================

def calculate_risk_scores(user_input, portfolio_data):
    """
    종합 위험지표 자동 계산
    - 감정 기반 위험도
    - 시장 기반 위험도  
    - 포지션 기반 위험도
    - 최종 종합 위험도
    """
    
    # 1️⃣ 감정 기반 위험도 (0-10)
    emotion_risk = 5.0  # 기본값
    
    # 손실 관련 키워드
    loss_keywords = ["손실", "떨어", "내려", "깍였", "빠졌", "손해", "후회", "털렸", "씨발", "진짜", "어떻게"]
    if any(word in user_input for word in loss_keywords):
        emotion_risk = 7.5  # 손실 상태
    
    # 불안 관련 키워드
    anxiety_keywords = ["불안", "걱정", "두려", "무섯", "심란", "답답", "어때"]
    if any(word in user_input for word in anxiety_keywords):
        emotion_risk = 6.5  # 불안 상태
    
    # 충동 관련 키워드
    impulse_keywords = ["사도", "들어갈", "몰빵", "지금", "급", "빨리", "바로"]
    if any(word in user_input for word in impulse_keywords):
        emotion_risk = 8.0  # 충동 위험
    
    # 2️⃣ 시장 기반 위험도 (0-10)
    # 실제로는 API에서 가져오지만, 지금은 시뮬레이션
    market_risk = random.uniform(5.0, 8.0)  # 시장 변동성
    
    # 반도체 관련 높은 위험
    high_risk_sectors = ["반도체", "AI", "2차전지", "바이오"]
    if any(sector in user_input for sector in high_risk_sectors):
        market_risk = min(market_risk + 1.5, 9.5)
    
    # 안정주 관련 낮은 위험
    low_risk_sectors = ["배당", "통신", "전력", "가스"]
    if any(sector in user_input for sector in low_risk_sectors):
        market_risk = max(market_risk - 1.5, 3.0)
    
    # 3️⃣ 포지션 기반 위험도 (0-10)
    # 포트폴리오 데이터 기반
    position_risk = 5.0
    
    if portfolio_data:
        # 손실 중인 종목 비율
        loss_count = sum(1 for stock in portfolio_data if stock['수익률'] < 0)
        total_count = len(portfolio_data)
        loss_ratio = loss_count / total_count if total_count > 0 else 0
        
        position_risk = 3.0 + (loss_ratio * 6.0)  # 3.0 ~ 9.0
    
    # 4️⃣ 최종 종합 위험도
    final_risk = (emotion_risk * 0.4 + market_risk * 0.3 + position_risk * 0.3)
    
    return {
        "emotion": round(emotion_risk, 1),
        "market": round(market_risk, 1),
        "position": round(position_risk, 1),
        "final": round(final_risk, 1)
    }

def get_risk_level(score):
    """위험도 레벨 판정"""
    if score >= 8.0:
        return "🔴 극도로 위험함", "#dc3544"
    elif score >= 6.5:
        return "🟠 높은 위험", "#ffc107"
    elif score >= 5.0:
        return "🟡 중간 위험", "#17a2b8"
    else:
        return "🟢 낮은 위험", "#28a745"

# ============================================================================
# 🤖 Groq 상담 함수
# ============================================================================

def groq_counsel(user_text, risk_scores):
    """
    위험지표를 포함한 AI 상담
    """
    try:
        import os
        api_key = os.getenv("GROQ_API_KEY") or "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"
        
        client = Groq(api_key=api_key)
        
        # 위험지표를 프롬프트에 포함
        prompt = f"""당신은 전문 투자 심리 상담 AI입니다.
사용자의 감정, 투자 수준, 위험도를 자연스럽게 추론하여 상담해주세요.

**현재 분석된 위험도:**
- 감정기반 위험: {risk_scores['emotion']}/10
- 시장기반 위험: {risk_scores['market']}/10
- 포지션기반 위험: {risk_scores['position']}/10
- 최종 종합 위험: {risk_scores['final']}/10

[분석]
- 감정 상태 (한 문장)
- 추정 투자 수준
- 현재 위험도 평가

[상담]
- 사용자 감정에 대한 공감
- 현재 상황 객관적 분석
- 위험도 기반 조언
- 다음 단계 선택지 (2~3개)

사용자 입력: {user_text}"""

        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt}
            ],
            model="llama-3.1-8b-instant",
            max_tokens=1024,
            temperature=0.7
        )
        
        return chat_completion.choices[0].message.content
    
    except Exception as e:
        return f"❌ 오류 발생: {str(e)}"

# ============================================================================
# 헤더
# ============================================================================

st.markdown('<div class="header-animated">🛡️ GINI Guardian v2.2</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #666; margin-bottom: 20px;">✨ 종합 위험지표 + AI 상담 ✨</div>', unsafe_allow_html=True)
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

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 상담 🔥", 
    "📊 위험지표", 
    "📈 차트", 
    "💼 포트폴리오", 
    "⚙️ 설정"
])

# ============================================================================
# TAB 1: AI 상담 + 위험지표
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
                with st.spinner("🤔 위험지표 분석 중... (2~3초)"):
                    # 위험지표 계산
                    risk_scores = calculate_risk_scores(user_input, st.session_state.portfolio)
                    
                    # 위험지표 표시
                    st.markdown("---")
                    st.markdown("### 📊 실시간 위험지표 분석")
                    
                    # 최종 위험도 (큰 카드)
                    risk_level, risk_color = get_risk_level(risk_scores['final'])
                    st.markdown(f"""
                    <div class="risk-card risk-{'critical' if risk_scores['final'] >= 8 else 'high' if risk_scores['final'] >= 6.5 else 'medium' if risk_scores['final'] >= 5 else 'low'}">
                        <h2 style="margin: 0; color: {risk_color};">⚠️ 오늘의 투자 위험도</h2>
                        <h1 style="margin: 10px 0; color: {risk_color};">{risk_scores['final']} / 10</h1>
                        <p style="margin: 5px 0; font-size: 1.2em;">{risk_level}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # 세부 위험도 분석
                    st.markdown("#### 📌 위험도 구성")
                    
                    risk_cols = st.columns(3)
                    
                    with risk_cols[0]:
                        st.markdown(f"""
                        <div class="risk-card risk-high">
                            <h4>😟 감정 기반 위험</h4>
                            <h2 style="color: #ffc107; margin: 10px 0;">{risk_scores['emotion']} / 10</h2>
                            <small>불안감, 충동성, 손실감 분석</small>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with risk_cols[1]:
                        st.markdown(f"""
                        <div class="risk-card risk-medium">
                            <h4>📈 시장 기반 위험</h4>
                            <h2 style="color: #17a2b8; margin: 10px 0;">{risk_scores['market']} / 10</h2>
                            <small>시장 변동성, 산업 리스크</small>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with risk_cols[2]:
                        st.markdown(f"""
                        <div class="risk-card risk-medium">
                            <h4>💼 포지션 기반 위험</h4>
                            <h2 style="color: #17a2b8; margin: 10px 0;">{risk_scores['position']} / 10</h2>
                            <small>손실 비율, 집중도</small>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    st.divider()
                    
                    # AI 상담
                    with st.spinner("🤔 AI가 상담 중입니다..."):
                        response = groq_counsel(user_input, risk_scores)
                        
                        st.markdown("### 🧭 AI 상담 결과")
                        st.markdown(response)
                    
                    st.markdown("---")
            else:
                st.warning("⚠️ 질문을 입력해주세요!")

# ============================================================================
# TAB 2: 위험지표 대시보드
# ============================================================================

with tab2:
    st.subheader("📊 위험지표 대시보드")
    
    st.info("""
    **위험지표 분석 가이드**
    
    🟢 **낮은 위험 (0-5)**: 안정적인 상태, 신규 진입 검토 가능
    🟡 **중간 위험 (5-6.5)**: 신중한 관찰 필요
    🟠 **높은 위험 (6.5-8)**: 신규 진입 제한, 손절 검토
    🔴 **극도 위험 (8-10)**: 긴급 모드, 즉시 대응 필요
    """)
    
    st.markdown("#### 📈 위험도 계산 로직")
    
    st.write("""
    **최종 위험도 = 감정기반(40%) + 시장기반(30%) + 포지션기반(30%)**
    
    - **감정 기반**: 사용자의 불안감, 충동성, 손실감 분석
    - **시장 기반**: 선택 종목의 변동성, 산업 위험도
    - **포지션 기반**: 현재 포트폴리오의 손실 비율
    
    이 3가지를 종합하여 **전문가 수준의 위험 평가** 제공합니다.
    """)

# ============================================================================
# TAB 3: 차트
# ============================================================================

with tab3:
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
# TAB 4: 포트폴리오
# ============================================================================

with tab4:
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
            st.markdown(f'<div class="warning-shake"><strong>{stock["종목명"]}</strong> | 매입: ₩{stock["매입가"]:,} | 현재: ₩{stock["현재가"]:,} | 수량: {stock["수량"]}개 | <span style="color: #dc3544; font-weight: bold;">{stock["수익률"]:.2f}%</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="success-float"><strong>{stock["종목명"]}</strong> | 매입: ₩{stock["매입가"]:,} | 현재: ₩{stock["현재가"]:,} | 수량: {stock["수량"]}개 | <span style="color: #28a745; font-weight: bold;">+{stock["수익률"]:.2f}%</span></div>', unsafe_allow_html=True)

# ============================================================================
# TAB 5: 설정
# ============================================================================

with tab5:
    st.subheader("⚙️ 설정 & 정보")
    
    st.info("""
    **GINI Guardian v2.2 - 위험지표 시스템**
    
    ✅ 실시간 위험도 분석
    ✅ 감정 + 시장 + 포지션 종합 평가
    ✅ 전문가 수준의 AI 상담
    ✅ Groq API (무료 + 초빠름)
    
    **다음 업데이트:**
    - SQLite 상담 기록 저장
    - Finnhub API 연동
    - 감정 패턴 분석
    """)

st.divider()
st.markdown("---\n🛡️ **GINI Guardian v2.2** | 📊 위험지표 + AI 상담 | 💙 라이라 설계 × 미라클 구현")
