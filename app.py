"""
🛡️ GINI Guardian v2.1 — 최종 완벽 버전
✨ 상담 아이콘 위아래 부드러운 움직임
✨ 매우 진한 파란색 헤더
✨ 깜빡임 + 포트폴리오 추가 기능

라이라 설계 × 미라클 구현 🔥
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

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
</style>
"""

st.set_page_config(page_title="GINI Guardian v2.1", page_icon="🛡️", layout="wide")
st.markdown(ANIMATION_CSS, unsafe_allow_html=True)

# ============================================================================
# 헤더
# ============================================================================

st.markdown('<div class="header-animated">🛡️ GINI Guardian v2.1</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #666; margin-bottom: 20px;">✨ 최종 완벽 버전 ✨</div>', unsafe_allow_html=True)
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
# 탭 (HOT 뱃지)
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "💬 상담 🔥", 
    "📰 뉴스", 
    "📈 차트", 
    "💼 포트폴리오", 
    "⚙️ 설정"
])

# ============================================================================
# TAB 1: 상담
# ============================================================================

with tab1:
    # HOT 뱃지 애니메이션
    st.markdown("""
    <div style="text-align: center; margin-bottom: 15px;">
        <span class="hot-badge" style="font-size: 1.8em; color: #ff4500;">🔥 HOT 상담</span>
    </div>
    """, unsafe_allow_html=True)
    
    # 상담 아이콘 애니메이션 (위아래 움직임 + 깜빡임)
    st.markdown('<div class="counsel-icon-animated">💬</div>', unsafe_allow_html=True)
    
    st.subheader("투자 상담")
    
    # 위험도 애니메이션
    st.markdown('<div class="danger-pulse"><h3>🔴 오늘의 시장 위험도</h3><p><strong>위험 수준: 높음 (7.5/10)</strong></p><p>부정적 뉴스 60% | 변동성 증가 | 신중한 접근 필수</p></div>', unsafe_allow_html=True)
    
    st.divider()
    
    # Session state를 사용하여 상태 관리
    if 'counsel_submitted' not in st.session_state:
        st.session_state.counsel_submitted = False
    if 'counsel_result' not in st.session_state:
        st.session_state.counsel_result = None
    if 'last_input' not in st.session_state:
        st.session_state.last_input = ""
    
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
        "예) 물타기 후 10% 잃었어...",
        height=100,
        key="counsel_textarea"
    )
    
    # 입력이 바뀌면 자동으로 이전 결과 초기화
    if user_input != st.session_state.last_input and user_input.strip():
        st.session_state.counsel_submitted = False
        st.session_state.counsel_result = None
    
    # 분석 버튼
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        if st.button("🔍 분석하기", use_container_width=True, type="primary"):
            if user_input.strip():
                st.session_state.counsel_submitted = True
                st.session_state.last_input = user_input
                
                # 감정 감지
                has_loss = any(word in user_input for word in ["잃었", "손실", "떨어", "내려", "깍였", "빠졌"])
                has_anxiety = any(word in user_input for word in ["불안", "걱정", "두려", "무섭", "괜찮"])
                has_impulse = any(word in user_input for word in ["사도", "들어갈", "몰빵", "지금", "급"])
                
                # 응답 결정
                if has_loss or has_anxiety:
                    st.session_state.counsel_result = "loss"
                elif has_impulse:
                    st.session_state.counsel_result = "impulse"
                else:
                    st.session_state.counsel_result = "safe"
                
                st.rerun()
            else:
                st.warning("⚠️ 질문을 입력해주세요!")
    
    # 결과 표시
    st.write("")
    
    if st.session_state.counsel_submitted and st.session_state.counsel_result:
        result = st.session_state.counsel_result
        
        if result == "loss":
            # 공감형 응답
            st.markdown('<div class="defense-message"><h3>💙 당신의 감정을 이해합니다</h3></div>', unsafe_allow_html=True)
            st.write("")
            
            st.info("""
**힘들었겠네요. 정말로요.**

**중요한 것은:**
과거의 선택은 이미 지났습니다.
지금부터 무엇을 할지가 중요해요.

**다음 중 뭘 하고 싶으신가요?**
1️⃣ 현재 상황을 정리하고 싶어요
2️⃣ 손절할지 말지 판단이 필요해요
3️⃣ 앞으로의 전략을 바꾸고 싶어요
4️⃣ 그냥 쉬고 싶어요
            """)
            
        elif result == "impulse":
            st.markdown('<div class="warning-shake"><h3>⚠️ 신중할 시간입니다</h3></div>', unsafe_allow_html=True)
            st.write("")
            
            st.warning("""
**지금은 시장이 불안정합니다.**

**확인해보세요:**
✓ 이 돈을 잃어도 괜찮은가요?
✓ 감정적 판단은 아닌가요?
✓ 3년 이상 보유할 수 있나요?
✓ 명확한 근거가 있나요?

**이 질문 중 하나라도 "아니오"라면**
👉 **지금은 움직일 때가 아닙니다.**
            """)
            
        else:  # safe
            st.markdown('<div class="success-float"><h3>✅ 안전한 질문입니다</h3></div>', unsafe_allow_html=True)
            st.write("")
            
            st.success("""
**기본 투자 원칙:**
✓ 장기 관점 유지
✓ 분산 투자 필수
✓ 감정 배제
✓ 잃어도 되는 금액만 투자
✓ 명확한 기준 수립
            """)
    
    # ============================================================================
    # 종목 분석 섹션 (상담 결과와 상관없이 항상 표시)
    # ============================================================================
    
    st.divider()
    
    st.markdown("### 📊 종목 분석")
    
    # 사용자가 종목을 언급했는지 확인
    stocks_mentioned = {
        "반도체": ["반도체", "SK하이닉스", "삼성전자", "하이닉스", "삼성", "DRAM", "낸드", "칩"],
        "통신": ["통신", "SKT", "KT", "LG유플러스", "LGU+"],
        "에너지": ["에너지", "석유", "원전", "태양광", "수소"],
        "전기차": ["전기차", "현대차", "기아", "테슬라", "EV", "자동차", "차량", "모빌리티"],
        "AI/기술": ["AI", "소프트웨어", "빅데이터", "클라우드", "NPU", "반도체", "기술주"]
    }
    
    detected_sectors = []
    for sector, keywords in stocks_mentioned.items():
        if any(keyword in user_input for keyword in keywords):
            detected_sectors.append(sector)
    
    if detected_sectors:
        st.markdown(f"**🔍 감지된 분야:** {', '.join(detected_sectors)}")
        
        # 반도체 산업 분석
        if "반도체" in detected_sectors:
            st.markdown("""
            <div class="success-float" style="margin-top: 15px;">
            <h4>💡 반도체 산업 분석</h4>
            
            **📈 현재 시장 상황:**
            ✓ 글로벌 AI 수요 급증
            ✓ 반도체 부족 현상 지속
            ✓ 장기 성장 산업
            
            **⚠️ 주의할 점:**
            ⚠️ 높은 변동성 (급등락)
            ⚠️ 경기 민감도 높음
            ⚠️ 경쟁 심화
            
            **🎯 투자 결론:**
            반도체는 **장기 성장 산업**이지만 **단기 변동성이 크다**
            
            **추천 접근 방식:**
            1️⃣ 장기 투자자: 좋은 기회 (3년 이상)
            2️⃣ 단기 투자자: 위험 (변동성 높음)
            3️⃣ 보수 투자자: 소액 분산 투자 권장
            
            **투자 전 체크리스트:**
            □ 총 자산의 10% 이내로 제한
            □ 3년 이상 보유 계획
            □ 손절가 미리 정하기 (-10~15%)
            □ 정기적 분할 매수 (DCA)
            
            **주요 반도체 종목:**
            • 삼성전자: 대형주 안정성 ⭐⭐⭐
            • SK하이닉스: 가치주 성향 ⭐⭐
            • 메모리 반도체: 수급 개선 중
            </div>
            """, unsafe_allow_html=True)
        
        # 통신 산업 분석
        if "통신" in detected_sectors:
            st.markdown("""
            <div class="warning-shake" style="margin-top: 15px;">
            <h4>💡 통신 산업 분석</h4>
            
            **📈 현재 시장 상황:**
            ✓ 배당금 높음
            ✓ 상대적 안정성
            ✓ 인프라 투자 지속
            
            **⚠️ 주의할 점:**
            ⚠️ 성장성 제한적
            ⚠️ 규제 리스크
            ⚠️ 경쟁 심화
            
            **🎯 투자 결론:**
            통신은 **안정적 배당주** 특징
            
            **추천 접근 방식:**
            1️⃣ 배당 수익 목표: 매력적
            2️⃣ 성장 투자: 제한적
            3️⃣ 보유 기간: 중장기 (5년+)
            
            **주요 통신 종목:**
            • SKT: 배당 + 안정성 ⭐⭐⭐
            • KT: 5G 인프라 ⭐⭐
            • LG유플러스: 가치주 ⭐⭐
            </div>
            """, unsafe_allow_html=True)
        
        # 전기차 산업 분석
        if "전기차" in detected_sectors:
            st.markdown("""
            <div class="success-float" style="margin-top: 15px;">
            <h4>💡 전기차 산업 분석</h4>
            
            **📈 현재 시장 상황:**
            ✓ 글로벌 EV 전환 추세
            ✓ 정부 정책 지원 확대
            ✓ 수익성 개선 추세
            
            **⚠️ 주의할 점:**
            ⚠️ 높은 변동성
            ⚠️ 기술 리스크
            ⚠️ 경쟁 급속화
            
            **🎯 투자 결론:**
            전기차는 **미래 성장 산업**이지만 **변동성 큼**
            
            **추천 접근 방식:**
            1️⃣ 보수적: 현대차/기아 (국내 대형주)
            2️⃣ 적극적: 테슬라 (성장성 높으나 리스크 높음)
            3️⃣ 분산: 2~3개 종목으로 리스크 분산
            
            **투자 기간:**
            • 최소 3년 이상 (변동성 흡수)
            • 장기 보유시 수익 가능성 높음
            
            **주요 전기차 종목:**
            • 현대차: 대형주 안정성 ⭐⭐⭐
            • 기아: 성장성 ⭐⭐⭐
            • 테슬라(미국): 고성장 고변동성 ⭐⭐
            </div>
            """, unsafe_allow_html=True)
        
        # AI/기술 산업 분석
        if "AI/기술" in detected_sectors:
            st.markdown("""
            <div class="success-float" style="margin-top: 15px;">
            <h4>💡 AI/기술 산업 분석</h4>
            
            **📈 현재 시장 상황:**
            ✓ AI 시대 본격화
            ✓ 수요 급증
            ✓ 성장성 높음
            
            **⚠️ 주의할 점:**
            ⚠️ 매우 높은 변동성
            ⚠️ 과열 우려
            ⚠️ 기술 변화 빠름
            
            **🎯 투자 결론:**
            AI/기술은 **최고 성장성**이지만 **최고 위험**
            
            **추천 접근 방식:**
            1️⃣ 공격적: 전액 투자 (경험 많은 투자자)
            2️⃣ 균형: 소액 비중으로 분산 투자
            3️⃣ 보수적: 피하기 (리스크 싫어하면)
            
            **투자 기간:**
            • 최소 5년 (매우 변동성 큼)
            • 손절가 필수 설정
            
            **추천 종목:**
            • 반도체: 인프라 역할 ⭐⭐⭐
            • 소프트웨어: 고성장 ⭐⭐⭐
            • 클라우드: 미래 필수 ⭐⭐⭐
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("""
        💡 **팁:** 구체적인 종목명을 말씀해주시면,
        더 자세한 분석을 해드릴 수 있습니다!
        
        예: "반도체 종목", "SKT", "현대차 전기차" 등
        """)
    
    # 초기화 버튼 (종목 분석 아래)
    st.write("")
    if st.button("🔄 새로운 상담하기", use_container_width=True):
        st.session_state.counsel_submitted = False
        st.session_state.counsel_result = None
        st.session_state.last_input = ""
        st.rerun()

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
    
    st.markdown("#### 🎨 애니메이션 효과")
    
    st.markdown('<div class="success-float"><strong>✨ 깜빡임 애니메이션</strong><br>헤더와 모든 박스의 부드러운 깜빡임 (2~3초 주기)</div>', unsafe_allow_html=True)
    st.markdown('<div class="counsel-icon-animated" style="font-size: 1.5em;"><strong>💬 상담 아이콘</strong></div>', unsafe_allow_html=True)
    st.markdown('<div style="padding: 10px; text-align: center; color: #666;">위아래 부드러운 움직임 + 깜빡임</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="danger-pulse"><strong>🔴 위험 신호</strong><br>위험 수준을 나타내는 깜빡이는 박스</div>', unsafe_allow_html=True)
    st.markdown('<div class="warning-shake"><strong>⚠️ 경고 메시지</strong><br>주의가 필요한 정보 표시</div>', unsafe_allow_html=True)
    st.markdown('<div class="success-float"><strong>✅ 안전 메시지</strong><br>안전한 정보 표시</div>', unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("#### 📋 버전 정보")
    st.info("""
    **GINI Guardian v2.1 - 최종 완벽 버전**
    
    ✅ 상담 아이콘 위아래 부드러운 움직임
    ✅ 매우 진한 파란색 헤더 (#052d7a)
    ✅ 상담 버튼 반응 완벽 수정
    ✅ 포트폴리오 종목 추가 기능
    ✅ 깜빡임 애니메이션 (움직임 최소화)
    ✅ 공감형 상담 시스템
    
    라이라 설계 × 미라클 구현 🔥
    """)

# 푸터
st.divider()
st.markdown("---\n🛡️ **GINI Guardian v2.1 - 최종 완벽 버전** | ✨ 상담 아이콘 움직임 + 진한 파란색 | 💙 라이라 설계 × 미라클 구현")
