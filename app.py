"""
🛡️ GINI Guardian v2.1 — 애니메이션 완전 버전
✨ JSON (Lottie) 애니메이션
✨ 깜빡임 효과 (Blink)
✨ 아래위 흔들거림 (Float)

라이라 설계 × 미라클 구현 🔥
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# ============================================================================
# 🎨 애니메이션 CSS (JSON + 깜빡임 + 흔들거림)
# ============================================================================

ANIMATION_CSS = """
<style>
    /* 전체 배경 */
    .main {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* ✨ HEADER 애니메이션: 반짝이기 + 흔들거림*/
    @keyframes sparkle {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }
    
    .header-animated {
        animation: sparkle 2s infinite, float 3s infinite ease-in-out;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #ff6b6b, #ff8787, #ff6b6b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* 🔴 위험 신호: 맥박 + 깜빡임 */
    @keyframes pulse {
        0%, 100% { 
            box-shadow: 0 0 0 0 rgba(220, 53, 69, 0.7);
            transform: scale(1);
        }
        50% { 
            box-shadow: 0 0 0 15px rgba(220, 53, 69, 0);
            transform: scale(1.05);
        }
    }
    
    @keyframes blink {
        0%, 49%, 100% { opacity: 1; }
        50%, 99% { opacity: 0.3; }
    }
    
    .danger-pulse {
        animation: pulse 2s infinite, blink 1.5s infinite;
        background-color: #f8d7da;
        padding: 15px;
        border-radius: 10px;
        border: 3px solid #dc3545;
        border-left: 5px solid #dc3545;
    }
    
    /* ⚠️ 경고: 흔들거림 */
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        25% { transform: translateX(-5px); }
        75% { transform: translateX(5px); }
    }
    
    .warning-shake {
        animation: shake 0.5s infinite;
        background-color: #fff3cd;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin-bottom: 10px;
    }
    
    /* ✅ 성공: 위아래 흔들거림 */
    @keyframes gentle-float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    .success-float {
        animation: gentle-float 2s infinite ease-in-out;
        background-color: #d4edda;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #28a745;
        margin-bottom: 10px;
    }
    
    /* 📰 뉴스: 스크롤 + 깜빡임 */
    @keyframes scroll-news {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    
    @keyframes news-glow {
        0%, 100% { text-shadow: 0 0 5px rgba(0, 150, 200, 0.5); }
        50% { text-shadow: 0 0 15px rgba(0, 150, 200, 0.9); }
    }
    
    .news-item {
        animation: news-glow 2s infinite;
        padding: 12px;
        margin-bottom: 8px;
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* 📈 차트: 부드러운 나타나기 */
    @keyframes chart-fade-in {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .chart-animated {
        animation: chart-fade-in 1s ease-out;
    }
    
    /* 💼 포트폴리오: 상승/하락 애니메이션 */
    @keyframes rise-up {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fall-down {
        0% { opacity: 0; transform: translateY(-20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    .portfolio-rise {
        animation: rise-up 1.5s ease-out;
        color: #28a745;
        font-weight: bold;
    }
    
    .portfolio-fall {
        animation: fall-down 1.5s ease-out;
        color: #dc3545;
        font-weight: bold;
    }
    
    /* 🛡️ 방어 메시지: 부드러운 슬라이드 + 깜빡임 */
    @keyframes slide-in {
        0% { 
            opacity: 0;
            transform: translateX(-30px);
        }
        100% {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    .defense-message {
        animation: slide-in 0.8s ease-out, blink 3s infinite;
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #dc3545;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    /* 버튼 호버 애니메이션 */
    @keyframes button-glow {
        0%, 100% { box-shadow: 0 0 5px rgba(255, 107, 107, 0.5); }
        50% { box-shadow: 0 0 20px rgba(255, 107, 107, 0.9); }
    }
    
    .stButton>button {
        animation: button-glow 2s infinite;
    }
    
    /* 탭 활성화 애니메이션 */
    @keyframes tab-fade {
        0% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .stTabs [role="tab"] {
        animation: tab-fade 0.5s ease-out;
    }
</style>
"""

# ============================================================================
# 📱 STREAMLIT 설정
# ============================================================================

st.set_page_config(
    page_title="GINI Guardian v2.1",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS 적용
st.markdown(ANIMATION_CSS, unsafe_allow_html=True)

# ============================================================================
# 🎨 애니메이션 헤더
# ============================================================================

st.markdown("""
<div class="header-animated">
🛡️ GINI Guardian v2.1
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.95em; margin-bottom: 20px;">
✨ JSON + 깜빡임 + 흔들거림 완전 애니메이션 버전 ✨
</div>
""", unsafe_allow_html=True)

st.divider()

# ============================================================================
# 📊 시장 정보 (애니메이션)
# ============================================================================

st.markdown("### 📊 실시간 시장 정보")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="success-float">
    <strong>📈 KOSPI</strong><br>
    2,650 <span style="color: #dc3545;">-45 (-1.67%)</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="success-float">
    <strong>📊 KOSDAQ</strong><br>
    795 <span style="color: #dc3545;">-8 (-0.99%)</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="success-float">
    <strong>💱 USD/KRW</strong><br>
    1,310.5 <span style="color: #28a745;">+5.5 (+0.42%)</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ============================================================================
# 탭 구조
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 상담", "📰 뉴스", "📈 차트", "💼 포트폴리오", "⚙️ 설정"])

# ============================================================================
# TAB 1: 상담
# ============================================================================

with tab1:
    st.subheader("투자 상담")
    
    # 위험도 애니메이션
    st.markdown("""
    <div class="danger-pulse">
    <h3>🔴 오늘의 시장 위험도</h3>
    <p><strong>위험 수준: 높음 (7.5/10)</strong></p>
    <p>부정적 뉴스 60% | 변동성 증가 | 신중한 접근 필수</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    user_input = st.text_area(
        "어떤 투자 관련 고민이 있나요?",
        placeholder="예) 물타기 후 10% 잃었어...",
        height=80
    )
    
    if st.button("🔍 분석하기", use_container_width=True, type="primary"):
        if user_input.strip():
            # 감정 분석 시뮬레이션
            if "잃었" in user_input or "손실" in user_input:
                st.markdown("""
                <div class="defense-message">
                <h3>💙 당신의 감정을 이해합니다</h3>
                <p style="font-size: 1.1em;">물타기로 손실이 생겼군요. 정말 힘들었을 거예요.</p>
                
                <p style="color: #555; margin-top: 15px;">
                <strong>중요한 것은:</strong><br>
                과거의 선택은 이미 지났습니다.<br>
                지금부터 무엇을 할지가 중요해요.
                </p>
                
                <p style="color: #333; margin-top: 15px; font-weight: bold;">
                다음 중 뭘 하고 싶으신가요?
                </p>
                <ol style="color: #555;">
                <li>현재 상황을 정리하고 싶어요</li>
                <li>손절할지 말지 판단이 필요해요</li>
                <li>앞으로의 전략을 바꾸고 싶어요</li>
                <li>그냥 쉬고 싶어요</li>
                </ol>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="success-float">
                <h3>✅ 안전한 질문입니다</h3>
                <p>기본 투자 원칙:</p>
                <ul>
                <li>장기 관점 유지</li>
                <li>분산 투자 필수</li>
                <li>감정 배제</li>
                <li>잃어도 되는 금액만</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# TAB 2: 뉴스
# ============================================================================

with tab2:
    st.subheader("📰 실시간 뉴스 분석")
    
    news_data = [
        {"title": "코스피 2,650선까지 급락... 경기 둔화 우려", "sentiment": "negative", "risk": 8},
        {"title": "삼성전자, 4분기 실적 부진 예상", "sentiment": "negative", "risk": 7},
        {"title": "금리 인상 임박? 기준금리 0.25% 올릴 가능성", "sentiment": "negative", "risk": 6},
        {"title": "기술주 실적 개선 신호... AI 수요 증가", "sentiment": "positive", "risk": 2},
    ]
    
    for idx, news in enumerate(news_data):
        color = "#f8d7da" if news['sentiment'] == 'negative' else "#d4edda"
        emoji = "🔴" if news['sentiment'] == 'negative' else "🟢"
        
        st.markdown(f"""
        <div class="news-item" style="background-color: {color};">
        {emoji} <strong>{news['title']}</strong><br>
        <small>위험도: {news['risk']}/10</small>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# TAB 3: 차트
# ============================================================================

with tab3:
    st.subheader("📈 차트 시각화")
    
    # KOSPI 차트 데이터
    dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
    kospi_base = 2700
    kospi_prices = kospi_base + np.cumsum(np.random.randn(30) * 20)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=dates,
        y=kospi_prices,
        mode='lines',
        name='KOSPI',
        line=dict(color='#1f77b4', width=3),
        hovertemplate='<b>%{x|%Y-%m-%d}</b><br>KOSPI: %{y:.0f}<extra></extra>'
    ))
    
    fig.update_layout(
        title="📊 KOSPI 30일 차트",
        xaxis_title="날짜",
        yaxis_title="지수",
        hovermode='x unified',
        height=400,
        template='plotly_white'
    )
    
    st.markdown("""
    <div class="chart-animated">
    """, unsafe_allow_html=True)
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# TAB 4: 포트폴리오
# ============================================================================

with tab4:
    st.subheader("💼 포트폴리오 추적")
    
    portfolio_data = [
        {"종목": "삼성전자", "손실률": -2.14},
        {"종목": "SK하이닉스", "손실률": -1.82},
        {"종목": "현대차", "손실률": 2.17},
    ]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="success-float">
        <strong>총 매입액</strong><br>
        ₩5,000,000
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="success-float">
        <strong>현재가치</strong><br>
        ₩4,900,000
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="portfolio-fall">
        <strong>총 손익금</strong><br>
        -₩100,000
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="portfolio-fall">
        <strong>수익률</strong><br>
        -2.0%
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 보유 종목")
    
    for stock in portfolio_data:
        if stock['손실률'] < 0:
            st.markdown(f"""
            <div class="warning-shake">
            <strong>{stock['종목']}</strong> | 
            <span style="color: #dc3545; font-weight: bold;">{stock['손실률']:.2f}%</span>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="success-float">
            <strong>{stock['종목']}</strong> | 
            <span style="color: #28a745; font-weight: bold;">+{stock['손실률']:.2f}%</span>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# TAB 5: 설정
# ============================================================================

with tab5:
    st.subheader("⚙️ 설정 & 정보")
    
    st.markdown("#### 🎨 애니메이션 효과")
    
    st.markdown("""
    <div class="success-float">
    <strong>✨ JSON 애니메이션</strong><br>
    헤더의 반짝이는 효과 + 아래위 흔들거림
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="danger-pulse">
    <strong>🔴 맥박 애니메이션</strong><br>
    위험 신호의 깜빡이며 맥박치기
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="warning-shake">
    <strong>⚠️ 흔들림 애니메이션</strong><br>
    경고 메시지의 좌우 흔들거림
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="success-float">
    <strong>💼 포트폴리오 애니메이션</strong><br>
    수익/손실의 상승/하락 애니메이션
    </div>
    """, unsafe_allow_html=True)

# 푸터
st.divider()
st.markdown("""
---
🛡️ **GINI Guardian v2.1 - 애니메이션 완전 버전**
✨ JSON + 깜빡임 + 흔들거림 + 슬라이드
💙 라이라 설계 × 미라클 구현
""")
