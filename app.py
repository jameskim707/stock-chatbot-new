import streamlit as st
from groq import Groq
import os
import random
import yfinance as yf
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import time

# 페이지 설정
st.set_page_config(
    page_title="GINI Guardian",
    page_icon="🛡️",
    layout="wide"
)

# 커스텀 CSS
st.markdown("""
<style>
    /* 경고 메시지 강하게 깜빡임 */
    @keyframes pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.8; transform: scale(1.05); }
    }
    
    .warning-pulse {
        animation: pulse 1s ease-in-out infinite;
        font-size: 1.2rem;
    }
    
    /* 메트릭 카드 호버 효과 */
    [data-testid="stMetricValue"] {
        font-size: 2rem !important;
        transition: all 0.3s ease;
    }
    
    div[data-testid="stMetric"]:hover {
        transform: scale(1.05);
        transition: all 0.3s ease;
    }
    
    /* 버튼 애니메이션 */
    .stButton button {
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
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
    
    @keyframes sparkle {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    .icon-bounce {
        display: inline-block;
        animation: bounce 2s ease-in-out infinite;
    }
    
    .icon-sparkle {
        display: inline-block;
        animation: sparkle 1.5s ease-in-out infinite;
    }
    
    .icon-rotate {
        display: inline-block;
        animation: rotate 3s linear infinite;
    }
    
    @keyframes rotate {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
    
    /* 탭 호버 효과 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
    }
    
    /* AI 상담 탭 강조 */
    .stTabs [data-baseweb="tab-list"] button:nth-child(2) {
        animation: pulse 2s ease-in-out infinite;
        background: linear-gradient(90deg, rgba(255,100,100,0.2), rgba(100,100,255,0.2));
        font-weight: bold;
    }
    
    /* 제목 반짝임 */
    h1 {
        animation: sparkle 3s ease-in-out infinite;
    }
    
    /* 안내 배너 */
    .ai-banner {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #4a90e2 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 25px 0;
        animation: pulse 2s ease-in-out infinite;
        box-shadow: 0 8px 25px rgba(30, 60, 114, 0.5);
    }
    
    .ai-banner h3 {
        color: white;
        margin: 0;
        font-size: 1.6rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
</style>
""", unsafe_allow_html=True)

# Groq API 초기화
@st.cache_resource
def init_groq():
    try:
        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            st.error("GROQ_API_KEY가 설정되지 않았습니다.")
            st.stop()
        return Groq(api_key=api_key)
    except Exception as e:
        st.error(f"Groq 클라이언트 초기화 실패: {e}")
        st.stop()

client = init_groq()

# 경고 메시지 데이터베이스
경고_메시지 = {
    "몰빵": [
        "야, 정신을 안드로메다에다 갔다났냐?",
        "몰빵은 스파게티 한그릇에 해라, 주식에 몰빵하다간 홈리스 된다",
        "야, 애들 학원비 어떡할 건데? 또 날리게?",
        "그 돈으로 와이프 선물 하나 사줘. 그게 더 행복해"
    ],
    "올인": [
        "또? 진심 또 하려고? 미쳤냐?",
        "테트리스는 내려가면 빠지지만 주식은 내려가면 폐가망신이다",
        "월세일 다음 주인데 정신 차려",
        "오늘 치킨 시켜먹어. 그게 확률 더 높아"
    ],
    "빚투": [
        "가족들한테 뭐라고 할 건데? 또 날렸다고?",
        "명절에 처가 가서 뭐라고 할 건데? '주식 또 날렸습니다'?",
        "오늘밤에 니 와이프한테 바가지 긁히고 쫓겨나고 싶어?",
        "부모님 용돈 드려. 그게 진짜 효도야"
    ],
    "레버리지": [
        "야, 계좌 보고 정신 차려. -15%야 지금",
        "내일 아침에 통장 보고 소주 한 병 각인데 괜찮아?",
        "지금 니가 날리려는 돈이 니 한 달 식비야",
        "자식 책 10권 살 수 있는 돈이야"
    ],
    "물타기": [
        "야, 지금까지 몇 번 말렸는데 또 하게?",
        "내일 아침에 후회할 거 빤한데 왜 그래?",
        "주식에 감정을 넣어서 하다간 골로가버린다, 이 친구야!",
        "확신이 없는데 남의 말듣고 들어가다간 저녁에 소주 또 깐다"
    ],
    "단타": [
        "지금 화났지? 그래서 또 하려는 거지? 멈춰!",
        "또? 진심 또 하려고? 미쳤냐?",
        "오늘 치킨 시켜먹어. 그게 확률 더 높아",
        "야, 지금까지 몇 번 말렸는데 또 하게?"
    ],
    "추천": [
        "확신이 없는데 남의 말듣고 들어가다간 저녁에 소주 또 깐다",
        "ㅇㅇ이 추천했다고? 그 사람 계좌 본 적 있어?",
        "주식에 감정을 넣어서 하다간 골로가버린다, 이 친구야!",
        "내일 아침에 후회할 거 빤한데 왜 그래?"
    ]
}

# 관심 종목 풀
관심종목_풀 = {
    "005930.KS": {"name": "삼성전자", "code": "005930"},
    "000660.KS": {"name": "SK하이닉스", "code": "000660"},
    "035420.KS": {"name": "NAVER", "code": "035420"},
    "035720.KS": {"name": "카카오", "code": "035720"},
    "323410.KS": {"name": "카카오뱅크", "code": "323410"},
    "207940.KS": {"name": "삼성바이오로직스", "code": "207940"},
    "068270.KS": {"name": "셀트리온", "code": "068270"},
    "326030.KS": {"name": "SK바이오팜", "code": "326030"},
    "373220.KS": {"name": "LG에너지솔루션", "code": "373220"},
    "006400.KS": {"name": "삼성SDI", "code": "006400"},
    "012450.KS": {"name": "한화에어로스페이스", "code": "012450"},
    "009540.KS": {"name": "HD한국조선해양", "code": "009540"},
    "352820.KS": {"name": "하이브", "code": "352820"},
    "041510.KS": {"name": "SM", "code": "041510"},
    "086790.KS": {"name": "하나금융지주", "code": "086790"},
    "071050.KS": {"name": "한국금융지주", "code": "071050"},
    "277810.KS": {"name": "레인보우로보틱스", "code": "277810"},
}

# 실시간 시장 데이터 가져오기
@st.cache_data(ttl=300)
def get_market_data():
    try:
        kospi = yf.Ticker("^KS11")
        kospi_data = kospi.history(period="5d", interval="1h")
        
        kosdaq = yf.Ticker("^KQ11")
        kosdaq_data = kosdaq.history(period="5d", interval="1h")
        
        usd_krw = yf.Ticker("KRW=X")
        usd_data = usd_krw.history(period="5d")
        
        # 랜덤으로 4개 종목 선택
        selected_tickers = random.sample(list(관심종목_풀.keys()), 4)
        
        stocks_data = {}
        for ticker in selected_tickers:
            stock = yf.Ticker(ticker)
            stocks_data[ticker] = {
                "name": 관심종목_풀[ticker]["name"],
                "code": 관심종목_풀[ticker]["code"],
                "data": stock.history(period="5d", interval="1h")
            }
        
        return {
            "kospi": kospi_data,
            "kosdaq": kosdaq_data,
            "usd_krw": usd_data,
            "stocks": stocks_data
        }
    except Exception as e:
        return None

# 차트 생성 함수
def create_mini_chart(data, title):
    if data is None or data.empty or len(data) < 2:
        return None
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=data.index,
        y=data['Close'],
        mode='lines',
        line=dict(color='#00D9FF', width=2),
        fill='tozeroy',
        fillcolor='rgba(0, 217, 255, 0.1)'
    ))
    
    fig.update_layout(
        title=title,
        height=200,
        margin=dict(l=0, r=0, t=30, b=0),
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig

# 메인 UI
st.markdown('<h1><span class="icon-sparkle">🛡️</span> GINI Guardian</h1>', unsafe_allow_html=True)
st.caption("과도한 투자로부터 당신을 지키는 AI 친구 | Made by Miracle 🔥")

# AI 상담 안내 배너
st.markdown("""
<div class="ai-banner">
    <h3>🤖 궁금한 종목이 있으신가요? AI 상담 탭에서 무료로 물어보세요!</h3>
</div>
""", unsafe_allow_html=True)

# 탭 생성
tab1, tab2, tab3 = st.tabs([
    "📊 실시간 시장", 
    "💬 AI 상담 🔥", 
    "📈 내 포트폴리오"
])

# 탭1: 실시간 시장
with tab1:
    # 새로고침 버튼
    col_refresh, col_time = st.columns([1, 4])
    with col_refresh:
        if st.button("🔄 새로고침", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    with col_time:
        st.info(f"⏰ 마지막 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} (5분마다 자동 갱신)")
    
    st.markdown('<h2><span class="icon-bounce">📈</span> 오늘의 시장</h2>', unsafe_allow_html=True)
    
    # 데이터 로드
    with st.spinner('📡 실시간 데이터 불러오는 중...'):
        market_data = get_market_data()
    
    if market_data:
        # 주요 지수
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if not market_data["kospi"].empty:
                kospi_close = market_data["kospi"]["Close"].iloc[-1]
                kospi_prev = market_data["kospi"]["Close"].iloc[-2] if len(market_data["kospi"]) > 1 else kospi_close
                kospi_change = ((kospi_close - kospi_prev) / kospi_prev) * 100
                
                st.metric(
                    "📊 코스피", 
                    f"{kospi_close:,.2f}",
                    f"{kospi_change:+.2f}%",
                    delta_color="normal"
                )
        
        with col2:
            if not market_data["kosdaq"].empty:
                kosdaq_close = market_data["kosdaq"]["Close"].iloc[-1]
                kosdaq_prev = market_data["kosdaq"]["Close"].iloc[-2] if len(market_data["kosdaq"]) > 1 else kosdaq_close
                kosdaq_change = ((kosdaq_close - kosdaq_prev) / kosdaq_prev) * 100
                
                st.metric(
                    "📊 코스닥", 
                    f"{kosdaq_close:,.2f}",
                    f"{kosdaq_change:+.2f}%",
                    delta_color="normal"
                )
        
        with col3:
            if not market_data["usd_krw"].empty:
                usd_close = market_data["usd_krw"]["Close"].iloc[-1]
                st.markdown(f'<div class="icon-sparkle">💵</div>', unsafe_allow_html=True)
                st.metric(
                    "USD/KRW", 
                    f"{usd_close:,.2f}원",
                    "환율"
                )
        
        st.divider()
        
        # 랜덤 종목 4개 섹션
        st.markdown('<h3><span class="icon-bounce">📈</span> 오늘의 추천 종목 (랜덤 4개)</h3>', unsafe_allow_html=True)
        
        # 2x2 그리드
        row1_col1, row1_col2 = st.columns(2)
        row2_col1, row2_col2 = st.columns(2)
        
        stock_items = list(market_data["stocks"].items())
        
        # 첫 번째 줄
        with row1_col1:
            if len(stock_items) > 0:
                ticker, info = stock_items[0]
                if not info["data"].empty and len(info["data"]) >= 2:
                    fig = create_mini_chart(info["data"], f"{info['name']} (5일)")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                        current = info["data"]["Close"].iloc[-1]
                        prev = info["data"]["Close"].iloc[-2]
                        change = ((current - prev) / prev) * 100
                        st.metric(info['name'], f"{current:,.0f}원", f"{change:+.2f}%")
                        # 네이버 증권 링크
                        naver_url = f"https://finance.naver.com/item/main.nhn?code={info['code']}"
                        st.link_button("📈 상세정보 보기", naver_url, use_container_width=True)
                else:
                    st.info(f"📊 {info['name']} 데이터 준비 중...")
        
        with row1_col2:
            if len(stock_items) > 1:
                ticker, info = stock_items[1]
                if not info["data"].empty and len(info["data"]) >= 2:
                    fig = create_mini_chart(info["data"], f"{info['name']} (5일)")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                        current = info["data"]["Close"].iloc[-1]
                        prev = info["data"]["Close"].iloc[-2]
                        change = ((current - prev) / prev) * 100
                        st.metric(info['name'], f"{current:,.0f}원", f"{change:+.2f}%")
                        naver_url = f"https://finance.naver.com/item/main.nhn?code={info['code']}"
                        st.link_button("📈 상세정보 보기", naver_url, use_container_width=True)
                else:
                    st.info(f"📊 {info['name']} 데이터 준비 중...")
        
        # 두 번째 줄
        with row2_col1:
            if len(stock_items) > 2:
                ticker, info = stock_items[2]
                if not info["data"].empty and len(info["data"]) >= 2:
                    fig = create_mini_chart(info["data"], f"{info['name']} (5일)")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                        current = info["data"]["Close"].iloc[-1]
                        prev = info["data"]["Close"].iloc[-2]
                        change = ((current - prev) / prev) * 100
                        st.metric(info['name'], f"{current:,.0f}원", f"{change:+.2f}%")
                        naver_url = f"https://finance.naver.com/item/main.nhn?code={info['code']}"
                        st.link_button("📈 상세정보 보기", naver_url, use_container_width=True)
                else:
                    st.info(f"📊 {info['name']} 데이터 준비 중...")
        
        with row2_col2:
            if len(stock_items) > 3:
                ticker, info = stock_items[3]
                if not info["data"].empty and len(info["data"]) >= 2:
                    fig = create_mini_chart(info["data"], f"{info['name']} (5일)")
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                        current = info["data"]["Close"].iloc[-1]
                        prev = info["data"]["Close"].iloc[-2]
                        change = ((current - prev) / prev) * 100
                        st.metric(info['name'], f"{current:,.0f}원", f"{change:+.2f}%")
                        naver_url = f"https://finance.naver.com/item/main.nhn?code={info['code']}"
                        st.link_button("📈 상세정보 보기", naver_url, use_container_width=True)
                else:
                    st.info(f"📊 {info['name']} 데이터 준비 중...")
        
        st.divider()
        st.caption("🎲 새로고침 버튼을 누르면 다른 종목을 볼 수 있어요!")

# 탭2: AI 상담
with tab2:
    st.markdown('<h2><span class="icon-bounce">💬</span> AI 투자 상담</h2>', unsafe_allow_html=True)
    
    user_input = st.text_input("메시지를 입력하세요:", key="chat_input", placeholder="예: 삼성전자 지금 사도 될까요?")
    
    if st.button("🚀 보내기", type="primary", use_container_width=True):
        if user_input:
            # 위험 키워드 감지
            위험_감지 = False
            감지된_키워드 = None
            
            for 키워드 in 경고_메시지.keys():
                if 키워드 in user_input:
                    위험_감지 = True
                    감지된_키워드 = 키워드
                    break
            
            # 위험 감지 시 랜덤 경고 표시
            if 위험_감지:
                경고 = random.choice(경고_메시지[감지된_키워드])
                st.markdown(f'<div class="warning-pulse">🚨 <b>{경고}</b></div>', unsafe_allow_html=True)
                st.error("⚠️ 잠깐! 한 번 더 생각해보세요.")
            
            # AI 응답
            with st.spinner('🤖 AI가 생각하는 중...'):
                try:
                    # 시장 데이터를 컨텍스트로 제공
                    market_context = ""
                    if market_data:
                        if not market_data["kospi"].empty:
                            kospi_close = market_data["kospi"]["Close"].iloc[-1]
                            market_context += f"현재 코스피: {kospi_close:,.2f}\n"
                        
                        # 랜덤 종목 정보도 추가
                        stock_info = "\n추천 종목:\n"
                        for ticker, info in market_data["stocks"].items():
                            if not info["data"].empty:
                                price = info["data"]["Close"].iloc[-1]
                                stock_info += f"- {info['name']}: {price:,.0f}원\n"
                        market_context += stock_info
                    
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {
                                "role": "system",
                                "content": (
                                    "너는 GINI Guardian이다. "
                                    "사용자의 과도한 투자, 몰빵, 단타 중독을 방지하고 "
                                    "심리적 안정과 위험 감지를 돕는 방어형 챗봇이다. "
                                    "친근하지만 단호하게 조언해줘. "
                                    f"현재 시장 상황:\n{market_context}"
                                )
                            },
                            {"role": "user", "content": user_input}
                        ],
                        stream=False
                    )
                    
                    st.write("### 🔸 GINI Guardian 응답:")
                    st.info(response.choices[0].message.content)
                    
                except Exception as e:
                    st.error(f"❌ API 호출 오류: {e}")
        else:
            st.warning("💬 메시지를 입력해주세요.")

# 탭3: 내 포트폴리오
with tab3:
    st.markdown('<h2><span class="icon-bounce">📈</span> 내 포트폴리오</h2>', unsafe_allow_html=True)
    st.info("🚧 개발 중입니다. 곧 만나보실 수 있습니다!")
    
    with st.form("portfolio_form"):
        st.subheader("💰 투자 프로필 설정")
        보유현금 = st.number_input("보유 현금 (만원)", min_value=0, value=500, step=100)
        투자성향 = st.selectbox("투자 성향", ["안정형 🛡️", "중립형 ⚖️", "공격형 🔥"])
        submitted = st.form_submit_button("📊 분석하기", use_container_width=True)
        
        if submitted:
            with st.spinner('분석 중...'):
                time.sleep(1)
            st.success(f"💰 보유 현금: {보유현금}만원")
            st.success(f"📊 투자 성향: {투자성향}")
            st.balloons()

# 사이드바
with st.sidebar:
    st.markdown('<div class="icon-sparkle">🛡️</div>', unsafe_allow_html=True)
    st.markdown("### GINI Guardian")
    st.markdown("**주식 과잉 방어 챗봇**")
    st.markdown("---")
    
    # 큰 AI 상담 버튼
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #4a90e2 100%);
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 20px 0;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(30, 60, 114, 0.6);
        animation: pulse 2s ease-in-out infinite;
    ">
        <h2 style="color: white; margin: 0; font-size: 3rem;">🤖</h2>
        <h3 style="color: white; margin: 10px 0;">AI에게 물어보기</h3>
        <p style="color: rgba(255,255,255,0.9); margin: 0; font-size: 0.9rem;">
            24시간 무료 상담<br/>
            투자 고민 해결!
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("#### 📌 주요 기능")
    st.markdown("""
    - <span class="icon-bounce">📊</span> 실시간 시장 모니터링
    - <span class="icon-bounce">📈</span> 랜덤 종목 추천 (4개)
    - <span class="icon-sparkle">💬</span> AI 투자 상담
    - <span class="icon-sparkle">🚨</span> 위험 거래 경고
    - 📈 포트폴리오 분석 (준비중)
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div class="icon-rotate">🔥</div> <b>Made by Miracle</b>', unsafe_allow_html=True)
    st.caption("Version 4.0 - With Naver Links")
    st.caption("© 2024 GINI Guardian")
