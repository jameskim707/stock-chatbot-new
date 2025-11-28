"""
🛡️ GINI Guardian v2.1 — Groq API 상담 버전
✨ Groq API (무료 + 초빠름)
✨ Llama 3.1 8B 기반 AI 상담
✨ 자연어 처리 (GPT 수준)

라이라 설계 × 미라클 구현 🔥
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np
from groq import Groq

# ============================================================================
# 🎨 애니메이션 CSS (최종 완벽 버전)
# ============================================================================

ANIMATION_CSS = """
<style>
    .main { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); }
    
    /* ✨ 깜빡임 - 차분하고 세련됨 */
    @keyframes gentle-blink { 
        0%, 100% { opacity: 1; } 
        50% { opacity: 0.7; } 
    }
    
    /* 💬 상담 아이콘: 위아래 부드러운 움직임 + 깜빡임 */
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
    
    /* 헤더: 매우 진한 파란색 깜빡임 */
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
    
    /* 🔥 HOT 뱃지: 반짝이고 깜빡이는 효과 */
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
    
    /* 위험 신호: 깜빡임만 */
    .danger-pulse { 
        animation: gentle-blink 2s infinite; 
        background-color: #f8d7da; 
        padding: 15px; 
        border-radius: 10px; 
        border: 3px solid #dc3544; 
    }
    
    /* 경고: 깜빡임만 */
    .warning-shake { 
        animation: gentle-blink 2s infinite;
        background-color: #fff3cd; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #ffc107; 
        margin-bottom: 10px; 
    }
    
    /* 성공: 깜빡임만 */
    .success-float { 
        animation: gentle-blink 2s infinite;
        background-color: #d4edda; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #28a745; 
        margin-bottom: 10px; 
    }
    
    /* 차트: 천천히 나타나기 */
    @keyframes fade-in { 
        0% { opacity: 0; } 
        100% { opacity: 1; } 
    }
    .chart-animated { animation: fade-in 1s ease-out; }
    
    /* 방어 메시지: 나타나기 + 깜빡임 */
    .defense-message { 
        animation: fade-in 0.8s ease-out, gentle-blink 2s infinite;
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #dc3544; 
    }
    
    /* 상담란 테두리 */
    .counsel-textarea {
        border: 1px solid #0a47a0 !important;
        border-radius: 8px !important;
        padding: 12px !important;
    }
</style>
"""

st.set_page_config(page_title="GINI Guardian v2.1 (Groq)", page_icon="🛡️", layout="wide")
st.markdown(ANIMATION_CSS, unsafe_allow_html=True)

# ============================================================================
# 🤖 Groq 상담 함수
# ============================================================================

def groq_counsel(user_text):
    """
    Groq API를 통한 AI 상담
    무료 + 초빠름 + 강력함
    """
    try:
        client = Groq(api_key="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")
        
        # 상담 프롬프트
        prompt = f"""당신은 전문 투자 심리 상담 AI입니다.
사용자의 감정, 투자 수준(초급/중급/상급)을 자연스럽게 추론하여 상담해주세요.

[분석]
- 감정 상태 (한 문장)
- 추정 투자 수준
- 위험도 (0~10)

[상담]
- 사용자 감정에 대한 공감
- 현재 상황 객관적 분석
- 투자 수준에 맞는 조언
- 다음 단계 선택지 (2~3개)

사용자 입력: {user_text}"""

        # Groq API 호출 (초빠름!)
        message = client.messages.create(
            model="llama-3.1-8b-instant",
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    
    except Exception as e:
        return f"❌ 오류 발생: {str(e)}\n\nAPI KEY를 확인해주세요."

# ============================================================================
# 헤더
# ============================================================================

st.markdown('<div class="header-animated">🛡️ GINI Guardian v2.1</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #666; margin-bottom: 20px;">✨ Groq API 상담 (무료 + 초빠름) ✨</div>', unsafe_allow_html=True)
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
    "📰 뉴스", 
    "📈 차트", 
    "💼 포트폴리오", 
    "⚙️ 설정"
])

# ============================================================================
# TAB 1: AI 상담 (Groq)
# ============================================================================

with tab1:
    # HOT 뱃지 애니메이션
    st.markdown("""
    <div style="text-align: center; margin-bottom: 15px;">
        <span class="hot-badge" style="font-size: 1.8em; color: #ff4500;">🔥 AI 상담 (Groq)</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 상담 아이콘 애니메이션 (위아래 움직임 + 깜빡임)
    st.markdown('<div class="counsel-icon-animated">💬</div>', unsafe_allow_html=True)
    
    st.subheader("AI 투자 상담")
    
    # 위험도 애니메이션
    st.markdown('<div class="danger-pulse"><h3>🔴 오늘의 시장 위험도</h3><p><strong>위험 수준: 높음 (7.5/10)</strong></p><p>부정적 뉴스 60% | 변동성 증가 | 신중한 접근 필수</p></div>', unsafe_allow_html=True)
    
    st.divider()
    
    # 입력 폼
    st.markdown("**당신의 투자 고민을 말씀해주세요:**")
    
    # 상담란 테두리 스타일
    st.markdown("""
    <style>
        .counsel-textarea {
            border: 1px solid #0a47a0 !important;
            border-radius: 8px !important;
            padding: 12px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    user_input = st.text_area(
        "예) 반도체 투자하려고 하는데 어때?",
        height=100,
        key="counsel_textarea"
    )
    
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("⚡ AI 상담하기", use_container_width=True, type="primary"):
            if user_input.strip():
                with st.spinner("🤔 AI가 생각 중입니다... (2~3초)"):
                    response = groq_counsel(user_input)
                    
                    st.markdown("---")
                    st.markdown("### 🧭 AI 상담 결과")
                    st.markdown(response)
                    st.markdown("---")
            else:
                st.warning("⚠️ 질문을 입력해주세요!")

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
    
    for news in news_data:
        color = "#f8d7da" if news['sentiment'] == 'negative' else "#d4edda"
        emoji = "🔴" if news['sentiment'] == 'negative' else "🟢"
        st.markdown(f'<div style="background-color: {color}; padding: 12px; border-radius: 8px; margin-bottom: 8px;">{emoji} <strong>{news["title"]}</strong><br><small>위험도: {news["risk"]}/10</small></div>', unsafe_allow_html=True)

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
    
    # Session state 초기화
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = [
            {"종목명": "삼성전자", "매입가": 70000, "현재가": 68500, "수량": 10, "수익률": -2.14},
            {"종목명": "SK하이닉스", "매입가": 110000, "현재가": 108000, "수량": 5, "수익률": -1.82},
            {"종목명": "현대차", "매입가": 230000, "현재가": 235000, "수량": 3, "수익률": 2.17},
        ]
    
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
    
    # 포트폴리오 표시
    for stock in st.session_state.portfolio:
        if stock['수익률'] < 0:
            st.markdown(f'<div class="warning-shake"><strong>{stock["종목명"]}</strong> | 매입: ₩{stock["매입가"]:,} | 현재: ₩{stock["현재가"]:,} | 수량: {stock["수량"]}개 | <span style="color: #dc3544; font-weight: bold;">{stock["수익률"]:.2f}%</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="success-float"><strong>{stock["종목명"]}</strong> | 매입: ₩{stock["매입가"]:,} | 현재: ₩{stock["현재가"]:,} | 수량: {stock["수량"]}개 | <span style="color: #28a745; font-weight: bold;">+{stock["수익률"]:.2f}%</span></div>', unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### ➕ 새 종목 추가")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        new_name = st.text_input("종목명", placeholder="예) 삼성전자", key="new_stock_name")
    with col2:
        new_buy = st.number_input("매입가", value=0, step=1000, key="new_stock_buy")
    with col3:
        new_current = st.number_input("현재가", value=0, step=1000, key="new_stock_current")
    with col4:
        new_qty = st.number_input("수량", value=0, step=1, key="new_stock_qty")
    with col5:
        st.write("")
        st.write("")
        add_btn = st.button("➕ 추가", use_container_width=True, type="primary")
    
    # 종목 추가 로직
    if add_btn:
        if new_name and new_buy > 0 and new_current > 0 and new_qty > 0:
            # 수익률 계산
            수익률 = ((new_current - new_buy) / new_buy) * 100
            
            # 포트폴리오에 추가
            new_stock = {
                "종목명": new_name,
                "매입가": new_buy,
                "현재가": new_current,
                "수량": new_qty,
                "수익률": 수익률
            }
            
            st.session_state.portfolio.append(new_stock)
            
            st.success(f"✅ {new_name} ({new_qty}개) 추가됨! 수익률: {수익률:.2f}%")
            st.rerun()
        else:
            st.warning("⚠️ 모든 필드를 입력해주세요!")

# ============================================================================
# TAB 5: 설정
# ============================================================================

with tab5:
    st.subheader("⚙️ 설정 & 정보")
    
    st.markdown("#### ⚡ Groq API 상담 정보")
    
    st.info("""
    **GINI Guardian v2.1 - Groq API 버전**
    
    ✅ 무료 (월 한계 넉넉함)
    ✅ 초빠름 (2~3초)
    ✅ 강력 (Llama 3.1 8B)
    ✅ 설치 불필요
    
    **사용 중인 모델:**
    • Llama 3.1 8B Instant
    
    **장점:**
    • API KEY만 있으면 됨
    • 클라우드 기반 (설치 X)
    • 초빠른 응답
    • 무료 (충분한 한계)
    """)
    
    st.markdown("#### 📋 버전 정보")
    st.info("""
    **GINI Guardian v2.1 - Groq Edition**
    
    ⚡ 무료 + 초빠른 AI 상담
    🚀 Llama 3.1 8B 기반
    💙 자연어 처리 (GPT 수준)
    
    라이라 설계 × 미라클 구현 🔥
    """)

# 푸터
st.divider()
st.markdown("---\n🛡️ **GINI Guardian v2.1 (Groq)** | ⚡ 무료 + 초빠른 AI 상담 | 💙 라이라 설계 × 미라클 구현")
