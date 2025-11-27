

import streamlit as st
from groq import Groq
import os
import random
import yfinance as yf
from datetime import datetime
import plotly.graph_objects as go
import time

# -----------------------------------------------------------
# 페이지 설정
# -----------------------------------------------------------
st.set_page_config(
    page_title="GINI GUARDIAN",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------------------------------------
# 커스텀 CSS (안정화 버전: h1 충돌 제거)
# -----------------------------------------------------------
st.markdown("""
<style>
/* 경고 메시지 깜빡임 */
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.8; transform: scale(1.05); }
}
.warning-pulse {
    animation: pulse 1s ease-in-out infinite;
    font-size: 1.2rem;
}

/* 메트릭 카드 */
[data-testid="stMetricValue"] {
    font-size: 2rem !important;
    transition: all 0.3s ease;
}
div[data-testid="stMetric"]:hover {
    transform: scale(1.05);
}

/* 버튼 효과 */
.stButton button {
    transition: all 0.3s ease;
}
.stButton button:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 15px rgba(0,0,0,0.3);
}

/* 아이콘 애니메이션 */
@keyframes bounce {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
.icon-bounce {
    display: inline-block;
    animation: bounce 2s ease-in-out infinite;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# Groq API 초기화
# -----------------------------------------------------------
@st.cache_resource
def init_groq():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        st.error("❌ GROQ_API_KEY가 설정되지 않았습니다.")
        st.stop()
    return Groq(api_key=api_key)

client = init_groq()

# -----------------------------------------------------------
# 경고 메시지 사전
# -----------------------------------------------------------
경고_메시지 = {
    "몰빵": ["야 정신차려!", "몰빵은 라면에 하고 주식은 분산해라."],
    "올인": ["또 올인? 제정신이냐.", "한번만 더 올인하면 계좌 장례식이다."],
    "빚투": ["빚투는 절대 금지!", "가족들 생각해라 제발."],
    "레버리지": ["레버리지는 칼이다. 잘못 쓰면 너 찍힌다."],
    "물타기": ["물타기 중독 멈춰!", "지금 물타면 더 깊이 빠진다."],
    "단타": ["단타 중독이다 이건.", "단타하려면 멘탈 10개 필요하다."],
    "추천": ["남 말 믿지마라.", "추천 따라가다 패가망신한다."]
}

# -----------------------------------------------------------
# 주가 데이터 가져오기
# -----------------------------------------------------------
@st.cache_data(ttl=300)
def get_market_data():
    try:
        kospi = yf.Ticker("^KS11").history(period="5d", interval="1h")
        kosdaq = yf.Ticker("^KQ11").history(period="5d", interval="1h")
        usd = yf.Ticker("KRW=X").history(period="5d")
        samsung = yf.Ticker("005930.KS").history(period="5d", interval="1h")
        hynix = yf.Ticker("000660.KS").history(period="5d", interval="1h")
        return {
            "kospi": kospi, "kosdaq": kosdaq, "usd": usd,
            "samsung": samsung, "hynix": hynix
        }
    except:
        return None

# -----------------------------------------------------------
# 차트 함수
# -----------------------------------------------------------
def mini_chart(data, title):
    if data is None or data.empty: return None
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index, y=data["Close"],
        mode="lines", line=dict(color="#00D9FF", width=2)
    ))
    fig.update_layout(
        title=title, height=200,
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
    )
    return fig

# -----------------------------------------------------------
# ⭐ 메인 UI 타이틀 — 여기서 정상적으로 바뀐다
# -----------------------------------------------------------
st.markdown(
    "<h1>🛡️ <b>GINI GUARDIAN</b></h1>",
    unsafe_allow_html=True
)
st.caption("과도한 투자로부터 당신을 지키는 AI 친구 | Made by Miracle")

# -----------------------------------------------------------
# 탭 구성
# -----------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["📊 실시간 시장", "💬 AI 상담", "📈 내 포트폴리오"])

# -----------------------------------------------------------
# TAB 1 — 실시간 시장
# -----------------------------------------------------------
with tab1:
    st.subheader("📈 오늘의 시장")

    with st.spinner("데이터 불러오는 중..."):
        market = get_market_data()

    if market:
        col1, col2, col3 = st.columns(3)

        kospi = market["kospi"]
        kosdaq = market["kosdaq"]
        usd = market["usd"]

        if not kospi.empty:
            now = kospi["Close"].iloc[-1]
            prev = kospi["Close"].iloc[-2]
            st.metric("코스피", f"{now:,.2f}", f"{(now-prev)/prev*100:+.2f}%")

        if not kosdaq.empty:
            now = kosdaq["Close"].iloc[-1]
            prev = kosdaq["Close"].iloc[-2]
            st.metric("코스닥", f"{now:,.2f}", f"{(now-prev)/prev*100:+.2f}%")

        if not usd.empty:
            st.metric("USD/KRW", f"{usd['Close'].iloc[-1]:,.2f}", "환율")

        st.divider()
        c1, c2 = st.columns(2)

        if not market["samsung"].empty:
            fig = mini_chart(market["samsung"], "삼성전자 (5일)")
            st.plotly_chart(fig, use_container_width=True)

        if not market["hynix"].empty:
            fig = mini_chart(market["hynix"], "SK하이닉스 (5일)")
            st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------------------------
# TAB 2 — AI 상담
# -----------------------------------------------------------
with tab2:
    st.subheader("💬 투자 상담")

    user_input = st.text_input("질문을 입력하세요")

    if st.button("보내기"):
        if user_input.strip() == "":
            st.warning("메시지를 입력해주세요.")
        else:
            # 위험 키워드 감지
            for k in 경고_메시지.keys():
                if k in user_input:
                    st.markdown(
                        f"<div class='warning-pulse'>🚨 {random.choice(경고_메시지[k])}</div>",
                        unsafe_allow_html=True
                    )
                    st.error("⚠️ 위험한 투자 패턴 감지!")

            with st.spinner("AI 분석 중..."):
                response = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "너는 GINI GUARDIAN 투자 방어 챗봇이다."},
                        {"role": "user", "content": user_input}
                    ]
                )

            st.info(response.choices[0].message.content)

# -----------------------------------------------------------
# TAB 3 — 포트폴리오
# -----------------------------------------------------------
with tab3:
    st.subheader("📈 포트폴리오")
    st.info("추가 기능 개발 중입니다!")

# -----------------------------------------------------------
# 사이드바
# -----------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛡️ GINI GUARDIAN")
    st.write("주식 과잉 방어 챗봇")
    st.markdown("---")
    st.write("📊 실시간 시장 모니터링")
    st.write("💬 AI 투자 상담")
    st.write("🚨 위험 패턴 경고")
    st.markdown("---")
    st.caption("Made by Miracle")
