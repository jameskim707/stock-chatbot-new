import streamlit as st
from groq import Groq
import os
import random
import yfinance as yf
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import time
from typing import Tuple

# ============================================================
# GINI Guardian - 7대 초보 질문 자동방어 모듈 (인라인)
# ============================================================

def detect_buy_signal(user_input: str) -> bool:
    """매수 관련 질문 감지"""
    buy_keywords = [
        "매수", "사야", "들어가", "진입", "매입", "사볼까", 
        "지금 사도", "언제 사", "사도 될까", "매집", "매수하면",
        "어떻게 사", "얼마에 사"
    ]
    return any(keyword in user_input for keyword in buy_keywords)

def detect_sell_signal(user_input: str) -> bool:
    """매도 관련 질문 감지"""
    sell_keywords = [
        "매도", "팔아", "빠져나갈까", "손절", "손절할까", 
        "매도하면", "언제 팔", "팔 타이밍", "익절", "팔아도"
    ]
    return any(keyword in user_input for keyword in sell_keywords)

def detect_amount_signal(user_input: str) -> bool:
    """금액/올인/몰빵 관련 질문 감지"""
    amount_keywords = [
        "올인", "몰빵", "전재산", "전부", "다", "얼마", 
        "금액", "몇 퍼센트", "비중", "자금", "풀로", "대출",
        "신용", "담보", "빚투", "빌려서"
    ]
    return any(keyword in user_input for keyword in amount_keywords)

def detect_risky_behavior(user_input: str) -> bool:
    """위험한 투자 행동 감지"""
    risky_keywords = [
        "빚투", "신용", "대출", "담보", "레버리지", "선물",
        "마이크로", "단타", "스윙", "물타기", "나이팅게일",
        "추천", "카톡", "방", "정보", "비결", "꿀팁"
    ]
    return any(keyword in user_input for keyword in risky_keywords)

def detect_hope_circuit(user_input: str) -> bool:
    """희망 회로 감지 (회복 기대, 필승 신념 등)"""
    hope_keywords = [
        "복구", "회복", "올라올", "반드시", "무조건", "확실",
        "믿어", "신뢰", "곧", "분명", "틀림없", "장기보유",
        "나중에", "언젠가", "분할"
    ]
    return any(keyword in user_input for keyword in hope_keywords)

def get_responsibility_clause() -> str:
    """책임전가 차단 문구"""
    clauses = [
        "최종 투자 결정은 전적으로 당신의 몫입니다.",
        "손실 발생 시 책임은 당신에게 있으며, 저는 책임을 질 수 없습니다.",
        "제가 드리는 의견은 참고용일 뿐 투자 권유가 아닙니다.",
        "당신의 투자 결정에 대해 저는 책임질 수 없습니다."
    ]
    return random.choice(clauses)

def get_psychological_stability() -> str:
    """심리 안정 문구"""
    messages = [
        "지금 마음이 흔들려 계신 것 같습니다. 한 발 물러서서 생각해 보세요.",
        "투자는 마라톤입니다. 한 번의 거래가 전부가 아닙니다.",
        "감정적인 결정은 후회로 이어집니다. 침착함을 유지하세요.",
        "현재의 선택이 미래의 후회가 되지 않도록 신중하세요."
    ]
    return random.choice(messages)

def get_risk_awareness() -> str:
    """위험 인지 문구"""
    messages = [
        "시장은 항상 예측 불가능합니다. 언제든 손실이 날 수 있습니다.",
        "과거의 성공이 미래의 성공을 보장하지 않습니다.",
        "전문가도 시장을 정확히 예측하지 못합니다.",
        "당신이 감수할 수 있는 손실의 범위를 먼저 정하세요."
    ]
    return random.choice(messages)

def get_self_decision_induction() -> str:
    """자기결정 유도 문구"""
    messages = [
        "당신은 이 상황에 대해 어떻게 생각하시나요?",
        "다른 사람의 말이 아닌, 당신의 판단을 먼저 세워보세요.",
        "당신이 이 위험을 감수할 준비가 정말 되셨나요?",
        "당신의 투자 목표와 기간을 다시 한번 확인해 보세요."
    ]
    return random.choice(messages)

def get_market_data_reference() -> str:
    """시장 데이터 참고 문장"""
    messages = [
        "현재 시장의 변동성이 상당합니다. 차트를 확인해 보세요.",
        "장기 추이를 보면 시장은 항상 변동합니다.",
        "단기 등락은 자연스러운 현상입니다.",
        "시장의 거시적 흐름을 먼저 파악하세요."
    ]
    return random.choice(messages)

def generate_safe_response(user_input: str, market_context: str = "") -> str:
    """위험 질문이 감지되면 안전한 답변을 자동 생성"""
    response_parts = []
    
    # 1. 공감과 인정
    response_parts.append("당신의 투자 고민을 이해합니다. 많은 투자자들이 같은 고민을 합니다.")
    response_parts.append("")
    
    # 2. 책임 명확화 (따뜻하게)
    response_parts.append(f"🛡️ {get_responsibility_clause()}")
    response_parts.append("")
    
    # 3. 심리 안정
    response_parts.append("💭 " + get_psychological_stability())
    response_parts.append("")
    
    # 4. 위험 인지 (구체적으로)
    response_parts.append("⚠️ " + get_risk_awareness())
    response_parts.append("")
    
    # 5. 실제 체크리스트
    response_parts.append("【 투자하기 전에 확인하세요 】")
    response_parts.append("✓ 잃어도 괜찮은 금액인가요?")
    response_parts.append("✓ 3년 이상 보유할 계획인가요?")
    response_parts.append("✓ 충동적인 결정은 아닌가요?")
    response_parts.append("✓ 전문가 의견이 아닌 당신의 판단인가요?")
    response_parts.append("")
    
    # 6. 자기결정 유도
    response_parts.append("이 질문들에 모두 '예'라고 답할 수 있다면, 당신은 충분히 준비된 것입니다.")
    response_parts.append("하나라도 '아니오'라면, 더 신중하게 생각해 보세요.")
    response_parts.append("")
    
    # 7. 희망 메시지
    response_parts.append("💪 당신의 투자 여정을 응원합니다.")
    response_parts.append("신중한 결정이 최고의 수익입니다.")
    
    return "\n".join(response_parts)

def analyze_user_input(user_input: str) -> Tuple[bool, str]:
    """사용자 입력을 분석하여 위험한 질문인지 판단"""
    risk_types = []
    
    if detect_buy_signal(user_input):
        risk_types.append("매수")
    if detect_sell_signal(user_input):
        risk_types.append("매도")
    if detect_amount_signal(user_input):
        risk_types.append("금액/올인")
    if detect_risky_behavior(user_input):
        risk_types.append("위험행동")
    if detect_hope_circuit(user_input):
        risk_types.append("희망회로")
    
    is_risky = len(risk_types) > 0
    risk_type = ", ".join(risk_types) if risk_types else "일반 질문"
    
    return is_risky, risk_type

def should_trigger_defense_module(user_input: str) -> bool:
    """자동방어 모듈을 발동할지 판단"""
    is_risky, _ = analyze_user_input(user_input)
    return is_risky

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
        "확신이 없는데 남의 말듣고 들어가다간 저녁에 소주 또 깐다",
        "물타기는 물귀신이다. 네 돈을 태우지 마라.",
        "더 잃기 전에 끊어내라. 미친 짓이다."
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
    ],
    "버티기": [
        "버티면 복구가 될 것 같냐? 망상이다.",
        "더 잃기 전에 끊어내라. 미친 짓이다.",
        "감정은 네 적이다. 투자와 감정은 분리해라.",
        "정신 차려라. 빛으로 투자하지 마라.",
        "네 무덤을 파고 있다. 제정신이냐?"
    ],
    "주식담보대출": [
        "주식 담보 대출은 칼날 위에서 춤추는 행위다.",
        "네가 버틸 수 없는 하락이 오면, 대출 때문에 모든 것을 잃는다.",
        "당장 그 계획을 폐기해라.",
        "빚으로 투자하지 마라. 네 무덤을 파고 있다.",
        "제정신이냐? 투기가 아니라 도박이다."
    ],
    "FOMO": [
        "FOMO(Fear Of Missing Out)는 패배자의 감정이다.",
        "놓치면 그만이다. 잃지 않는 게 중요하다.",
        "곧 깡통을 찰 것이다. 서울역 가고싶냐?",
        "멈춰라. 목표 없는 투자는 방황이다.",
        "방황하다 돈만 잃는다. 왜 하는지 말해봐라."
    ],
    "도박": [
        "도박장에 온 것을 환영한다. 돈 다 잃기 싫으면 당장 손 떼라.",
        "네 돈은 네 책임이다. 나는 조언만 한다.",
        "운명을 남에게 맡기지 마라.",
        "투기가 아니라 도박이다.",
        "현실을 직시해라. 도망치지 마라."
    ],
    "희망회로": [
        "허황된 꿈꾸지 마라. 그런 일은 너에게 일어나지 않는다.",
        "네가 특별한 줄 아느냐?",
        "도망치는 자는 시장에서 돈을 잃는다.",
        "네가 뭘 잘못했는지 말해봐라.",
        "감정 상할 시간 없다. 네 돈 잃는 게 더 기분 나쁜 일이다."
    ]
}

# 관심 종목 풀 (일주일 단위 로테이션)
관심종목_풀 = {
    # 대형주
    "005930.KS": {"name": "삼성전자", "code": "005930"},
    "000660.KS": {"name": "SK하이닉스", "code": "000660"},
    "051910.KS": {"name": "LG화학", "code": "051910"},
    "034020.KS": {"name": "두산밥위스", "code": "034020"},
    
    # IT/통신
    "035420.KS": {"name": "NAVER", "code": "035420"},
    "035720.KS": {"name": "카카오", "code": "035720"},
    "323410.KS": {"name": "카카오뱅크", "code": "323410"},
    "011200.KS": {"name": "HMM", "code": "011200"},
    
    # 바이오/제약
    "207940.KS": {"name": "삼성바이오로직스", "code": "207940"},
    "068270.KS": {"name": "셀트리온", "code": "068270"},
    "326030.KS": {"name": "SK바이오팜", "code": "326030"},
    "096530.KS": {"name": "씨젠", "code": "096530"},
    
    # 에너지/소재
    "373220.KS": {"name": "LG에너지솔루션", "code": "373220"},
    "006400.KS": {"name": "삼성SDI", "code": "006400"},
    "010950.KS": {"name": "S-Oil", "code": "010950"},
    "002210.KS": {"name": "동성화학", "code": "002210"},
    
    # 방위산업/중공업
    "012450.KS": {"name": "한화에어로스페이스", "code": "012450"},
    "009540.KS": {"name": "HD한국조선해양", "code": "009540"},
    "042660.KS": {"name": "한화전기", "code": "042660"},
    "000080.KS": {"name": "하이트진로", "code": "000080"},
    
    # 엔터테인먼트/미디어
    "352820.KS": {"name": "하이브", "code": "352820"},
    "041510.KS": {"name": "SM", "code": "041510"},
    "097950.KS": {"name": "CJ ENM", "code": "097950"},
    "036200.KS": {"name": "한화솔루션", "code": "036200"},
    
    # 금융
    "086790.KS": {"name": "하나금융지주", "code": "086790"},
    "071050.KS": {"name": "한국금융지주", "code": "071050"},
    "005387.KS": {"name": "현대차", "code": "005387"},
    "006360.KS": {"name": "GE에너지", "code": "006360"},
    
    # 로봇/자동화
    "277810.KS": {"name": "레인보우로보틱스", "code": "277810"},
    "011070.KS": {"name": "LG이노텍", "code": "011070"},
    "035900.KS": {"name": "JYP엔터테인먼트", "code": "035900"},
    "012330.KS": {"name": "현대모비스", "code": "012330"},
    
    # 추가 유망주
    "088260.KS": {"name": "삼성전기", "code": "088260"},
    "241560.KS": {"name": "두산퓨얼셀", "code": "241560"},
    "010620.KS": {"name": "현대석유화학", "code": "010620"},
    "009150.KS": {"name": "삼성전기", "code": "009150"},
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
    
    # 상담 상태 초기화
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # 상담 입력 영역
    col_input, col_button = st.columns([4, 1])
    
    with col_input:
        user_input = st.text_input("메시지를 입력하세요:", key="chat_input", placeholder="예: 삼성전자 지금 사도 될까요?")
    
    with col_button:
        send_button = st.button("🚀 보내기", type="primary", use_container_width=True)
    
    if send_button and user_input:
        try:
            # 자동방어 모듈 활성화
            is_risky, risk_type = analyze_user_input(user_input)
            
            if should_trigger_defense_module(user_input):
                # 위험 감지 - 자동방어 모듈 발동
                st.warning(f"🚨 위험 질문 감지됨: {risk_type}")
                st.info("🛡️ 자동방어 모듈이 활성화되었습니다.")
                
                safe_response = generate_safe_response(user_input)
                st.write("### 🔸 GINI Guardian 응답:")
                st.info(safe_response)
                
                # 대화 기록 저장
                st.session_state.chat_history.append({
                    "user": user_input,
                    "bot": safe_response,
                    "type": "defense"
                })
            
            else:
                # 일반 질문 - Groq AI에게 넘김
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
                                        "당신은 GINI Guardian입니다. "
                                        "사용자의 투자 고민을 친절하게 듣고, 객관적인 정보와 분석을 제공하는 상담 챗봇입니다. "
                                        "하지만 최종 투자 결정은 절대 대신 내려드릴 수 없으며, 손실 발생 시 책임을 질 수 없음을 명확히 해야 합니다. "
                                        "\n"
                                        "【 상담 패턴 】\n"
                                        "1. 사용자의 관심사에 공감하기\n"
                                        "2. 해당 종목/투자의 긍정적 정보 제시\n"
                                        "3. 객관적인 리스크 요소 설명\n"
                                        "4. 시장 변동성과 불확실성 언급\n"
                                        "5. '이러한 위험을 감수할 준비가 되셨나요?'라고 질문 되돌리기\n"
                                        "6. '최종 결정은 당신의 몫입니다'로 권한 부여\n"
                                        "7. '손실 발생 시 책임은 저에게 묻지 마세요'로 책임 명확화\n"
                                        "\n"
                                        f"현재 시장 상황:\n{market_context}"
                                    )
                                },
                                {"role": "user", "content": user_input}
                            ],
                            stream=False
                        )
                        
                        bot_response = response.choices[0].message.content
                        st.write("### 🔸 GINI Guardian 응답:")
                        st.info(bot_response)
                        
                        # 대화 기록 저장
                        st.session_state.chat_history.append({
                            "user": user_input,
                            "bot": bot_response,
                            "type": "general"
                        })
                        
                    except Exception as e:
                        st.error(f"❌ API 호출 오류: {str(e)}")
        
        except Exception as e:
            st.error(f"❌ 처리 중 오류 발생: {str(e)}")
    
    elif send_button:
        st.warning("💬 메시지를 입력해주세요.")
    
    # 대화 기록 표시
    st.divider()
    if st.session_state.chat_history:
        st.write("### 📋 대화 기록")
        for i, chat in enumerate(st.session_state.chat_history):
            st.write(f"**👤 당신:** {chat['user']}")
            st.write(f"**🤖 Guardian:** {chat['bot']}")
            st.divider()

# 탭3: 내 포트폴리오
with tab3:
    st.markdown('<h2><span class="icon-bounce">📈</span> 내 포트폴리오</h2>', unsafe_allow_html=True)
    
    # 포트폴리오 세션 상태 초기화
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = []
    
    # 1단계: 보유 종목 입력
    st.markdown('<h3>🔥 1단계: 보유 종목 등록</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        stock_name = st.text_input("종목명", placeholder="예: 삼성전자")
    
    with col2:
        buy_price = st.number_input("매입가 (원)", min_value=0, value=0, step=1000)
    
    with col3:
        quantity = st.number_input("수량 (주)", min_value=0, value=0, step=1)
    
    stock_code = st.text_input("종목 코드", placeholder="예: 005930.KS")
    
    if st.button("✅ 종목 추가", use_container_width=True, type="primary"):
        if stock_name and buy_price > 0 and quantity > 0 and stock_code:
            new_stock = {
                "name": stock_name,
                "code": stock_code,
                "buy_price": buy_price,
                "quantity": quantity,
                "buy_amount": buy_price * quantity
            }
            st.session_state.portfolio.append(new_stock)
            st.success(f"✅ {stock_name}이(가) 추가되었습니다!")
        else:
            st.error("❌ 모든 필드를 올바르게 입력해주세요.")
    
    st.divider()
    
    # 2단계: 수익률 계산
    if st.session_state.portfolio:
        st.markdown('<h3>🔥 2단계: 수익률 분석</h3>', unsafe_allow_html=True)
        
        with st.spinner('📊 실시간 가격 불러오는 중...'):
            portfolio_data = []
            total_buy_amount = 0
            total_current_amount = 0
            
            for stock in st.session_state.portfolio:
                try:
                    ticker = yf.Ticker(stock['code'])
                    current_price = ticker.history(period="1d")['Close'].iloc[-1]
                    current_amount = current_price * stock['quantity']
                    profit_loss = current_amount - stock['buy_amount']
                    profit_loss_rate = (profit_loss / stock['buy_amount']) * 100 if stock['buy_amount'] > 0 else 0
                    
                    portfolio_data.append({
                        "종목명": stock['name'],
                        "매입가": f"{stock['buy_price']:,.0f}원",
                        "현재가": f"{current_price:,.0f}원",
                        "수량": f"{stock['quantity']}주",
                        "매입액": f"{stock['buy_amount']:,.0f}원",
                        "현재액": f"{current_amount:,.0f}원",
                        "수익/손실": f"{profit_loss:,.0f}원",
                        "수익률": f"{profit_loss_rate:+.2f}%"
                    })
                    
                    total_buy_amount += stock['buy_amount']
                    total_current_amount += current_amount
                    
                except Exception as e:
                    st.warning(f"⚠️ {stock['name']} 가격 조회 실패: {str(e)}")
            
            # 수익률 테이블 표시
            if portfolio_data:
                st.dataframe(portfolio_data, use_container_width=True)
                
                # 전체 포트폴리오 수익률
                st.divider()
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("📊 총 매입액", f"{total_buy_amount:,.0f}원")
                
                with col2:
                    st.metric("💰 총 현재액", f"{total_current_amount:,.0f}원")
                
                with col3:
                    total_profit_loss = total_current_amount - total_buy_amount
                    total_profit_rate = (total_profit_loss / total_buy_amount) * 100 if total_buy_amount > 0 else 0
                    
                    if total_profit_loss >= 0:
                        st.metric("📈 총 수익/손실", f"{total_profit_loss:,.0f}원", f"{total_profit_rate:+.2f}%")
                    else:
                        st.metric("📉 총 수익/손실", f"{total_profit_loss:,.0f}원", f"{total_profit_rate:+.2f}%")
                
                st.divider()
                
                # 3단계: 리스크 분석
                st.markdown('<h3>🔥 3단계: 리스크 분석</h3>', unsafe_allow_html=True)
                
                # 종목별 비중 계산
                risk_analysis = []
                max_single_stock = 0
                high_volatility_count = 0
                
                for stock in st.session_state.portfolio:
                    stock_ratio = (stock['buy_amount'] / total_buy_amount) * 100 if total_buy_amount > 0 else 0
                    risk_analysis.append({
                        "종목": stock['name'],
                        "비중": f"{stock_ratio:.1f}%"
                    })
                    max_single_stock = max(max_single_stock, stock_ratio)
                
                st.write("**종목별 비중:**")
                st.dataframe(risk_analysis, use_container_width=True)
                
                # 위험 경고
                st.write("**⚠️ 위험 분석:**")
                
                if max_single_stock > 40:
                    st.error(f"🚨 단일 종목 비중이 {max_single_stock:.1f}%로 높습니다! (권장: 20% 이하)")
                    st.info("💡 포트폴리오 다양화를 추천합니다.")
                elif max_single_stock > 20:
                    st.warning(f"⚠️ 단일 종목 비중이 {max_single_stock:.1f}%로 중간 수준입니다. (권장: 20% 이하)")
                else:
                    st.success(f"✅ 종목 다양화가 잘 되어있습니다. (최대 비중: {max_single_stock:.1f}%)")
                
                st.divider()
                
                # 4단계: 맞춤 조언
                st.markdown('<h3>🔥 4단계: GINI Guardian 맞춤 조언</h3>', unsafe_allow_html=True)
                
                advice_parts = []
                advice_parts.append("📋 **당신의 포트폴리오 분석:**\n")
                
                # 수익 상황에 따른 조언
                if total_profit_loss > 0:
                    advice_parts.append(f"✅ 현재 {total_profit_rate:+.2f}% 수익 상태입니다.")
                    advice_parts.append("💡 이 상태를 유지하되, 욕심내지 않도록 주의하세요.\n")
                else:
                    advice_parts.append(f"⚠️ 현재 {total_profit_rate:+.2f}% 손실 상태입니다.")
                    advice_parts.append("💡 장기 관점에서 회복을 기대하되, 추가 손실 방지가 중요합니다.\n")
                
                # 포트폴리오 구성에 따른 조언
                if max_single_stock > 40:
                    advice_parts.append("🚨 **즉시 조치 필요:**")
                    advice_parts.append(f"• 단일 종목 비중이 {max_single_stock:.1f}%로 너무 높습니다.")
                    advice_parts.append("• 다른 종목으로 분산 투자하세요.\n")
                
                # 투자 성향별 조언
                advice_parts.append("📊 **포트폴리오 개선 방안:**")
                advice_parts.append("• 변동성이 높은 종목은 전체의 30% 이하로 유지하세요.")
                advice_parts.append("• ETF나 안정적인 대형주로 기초를 다지세요.")
                advice_parts.append("• 급등/급락에 흔들리지 마세요.")
                advice_parts.append("• 정기적으로 포트폴리오를 점검하세요.\n")
                
                # 마지막 조언
                advice_parts.append("💪 **GINI Guardian의 조언:**")
                advice_parts.append("당신의 포트폴리오는 당신의 투자 철학을 담고 있습니다.")
                advice_parts.append("단기 수익보다 장기 안정성을 우선하세요.")
                advice_parts.append("감정적 결정은 피하고, 계획에 따라 실행하세요.")
                
                st.info("\n".join(advice_parts))
        
        # 포트폴리오 관리
        st.divider()
        st.markdown('<h3>📋 포트폴리오 관리</h3>', unsafe_allow_html=True)
        
        if st.button("🗑️ 포트폴리오 초기화", type="secondary", use_container_width=True):
            st.session_state.portfolio = []
            st.success("포트폴리오가 초기화되었습니다.")
            st.rerun()
    
    else:
        st.info("📝 위에서 종목을 추가하면 포트폴리오 분석이 시작됩니다!")

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
    st.caption("Version 5.0 - Enhanced Warning Messages")
    st.caption("© 2024 GINI Guardian")
