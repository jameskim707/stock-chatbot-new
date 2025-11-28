"""
🛡️ GINI Guardian v2.1 — 애니메이션 완전 버전 (상담 수정)
✨ JSON + 깜빡임 + 흔들거림 + 빠른 상담

라이라 설계 × 미라클 구현 🔥
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import numpy as np

# ============================================================================
# 🎨 애니메이션 CSS
# ============================================================================

ANIMATION_CSS = """
<style>
    .main { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); }
    
    /* ✨ 깜빡임만 - 차분하고 세련됨 */
    @keyframes gentle-blink { 
        0%, 100% { opacity: 1; } 
        50% { opacity: 0.7; } 
    }
    
    .header-animated {
        animation: gentle-blink 3s infinite;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(45deg, #1f77b4, #4a9eff, #1f77b4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* 위험 신호: 깜빡임만 (움직임 없음) */
    .danger-pulse { 
        animation: gentle-blink 2s infinite; 
        background-color: #f8d7da; 
        padding: 15px; 
        border-radius: 10px; 
        border: 3px solid #dc3545; 
    }
    
    /* 경고: 깜빡임만 (움직임 없음) */
    .warning-shake { 
        animation: gentle-blink 2s infinite;
        background-color: #fff3cd; 
        padding: 15px; 
        border-radius: 10px; 
        border-left: 5px solid #ffc107; 
        margin-bottom: 10px; 
    }
    
    /* 성공: 깜빡임만 (움직임 없음) */
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
    
    /* 방어 메시지: 천천히 나타나기 + 깜빡임 */
    .defense-message { 
        animation: fade-in 0.8s ease-out, gentle-blink 2s infinite;
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%); 
        padding: 20px; 
        border-radius: 15px; 
        border-left: 5px solid #dc3545; 
    }
</style>
"""

st.set_page_config(page_title="GINI Guardian v2.1", page_icon="🛡️", layout="wide")
st.markdown(ANIMATION_CSS, unsafe_allow_html=True)

# ============================================================================
# 헤더
# ============================================================================

st.markdown('<div class="header-animated">🛡️ GINI Guardian v2.1</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: #666; margin-bottom: 20px;">✨ 애니메이션 완전 버전 ✨</div>', unsafe_allow_html=True)
st.divider()

# ============================================================================
# 시장 정보
# ============================================================================

st.markdown("### 📊 실시간 시장 정보")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<div class="success-float"><strong>📈 KOSPI</strong><br>2,650 <span style="color: #dc3545;">-45 (-1.67%)</span></div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="success-float"><strong>📊 KOSDAQ</strong><br>795 <span style="color: #dc3545;">-8 (-0.99%)</span></div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="success-float"><strong>💱 USD/KRW</strong><br>1,310.5 <span style="color: #28a745;">+5.5 (+0.42%)</span></div>', unsafe_allow_html=True)

st.divider()

# ============================================================================
# 탭
# ============================================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 상담", "📰 뉴스", "📈 차트", "💼 포트폴리오", "⚙️ 설정"])

# ============================================================================
# TAB 1: 상담
# ============================================================================

with tab1:
    st.subheader("투자 상담")
    
    # 위험도 애니메이션
    st.markdown('<div class="danger-pulse"><h3>🔴 오늘의 시장 위험도</h3><p><strong>위험 수준: 높음 (7.5/10)</strong></p><p>부정적 뉴스 60% | 변동성 증가 | 신중한 접근 필수</p></div>', unsafe_allow_html=True)
    
    st.divider()
    
    # 입력 폼
    user_input = st.text_area("어떤 투자 관련 고민이 있나요?", placeholder="예) 물타기 후 10% 잃었어...", height=80, key="counsel_input")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        pass
    
    with col2:
        analyze_button = st.button("🔍 분석", use_container_width=True, type="primary", key="analyze_btn")
    
    # 분석 결과
    if analyze_button:
        if user_input.strip():
            st.write("")
            
            # 감정 감지
            has_loss = "잃었" in user_input or "손실" in user_input or "떨어" in user_input or "내려" in user_input
            has_anxiety = "불안" in user_input or "걱정" in user_input or "두려" in user_input
            has_impulse = "사도" in user_input or "들어갈" in user_input or "몰빵" in user_input or "지금" in user_input
            
            if has_loss or has_anxiety:
                # 공감형 응답
                st.markdown('<div class="defense-message"><h3>💙 당신의 감정을 이해합니다</h3></div>', unsafe_allow_html=True)
                st.write("")
                
                st.info("""
                힘들었겠네요. 정말로요.

                **중요한 것은:**
                과거의 선택은 이미 지났습니다.
                지금부터 무엇을 할지가 중요해요.

                **다음 중 뭘 하고 싶으신가요?**
                1. 현재 상황을 정리하고 싶어요
                2. 손절할지 말지 판단이 필요해요
                3. 앞으로의 전략을 바꾸고 싶어요
                4. 그냥 쉬고 싶어요
                """)
                
            elif has_impulse:
                st.markdown('<div class="warning-shake"><h3>⚠️ 신중할 시간입니다</h3></div>', unsafe_allow_html=True)
                st.write("")
                
                st.warning("""
                지금은 시장이 불안정합니다.

                **확인해보세요:**
                ✓ 이 돈을 잃어도 괜찮은가요?
                ✓ 감정적 판단은 아닌가요?
                ✓ 3년 이상 보유할 수 있나요?
                ✓ 명확한 근거가 있나요?

                이 질문 중 하나라도 "아니오"라면
                **지금은 움직일 때가 아닙니다.**
                """)
                
            else:
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
    fig.add_trace(go.Scatter(x=dates, y=kospi_prices, mode='lines', name='KOSPI', line=dict(color='#1f77b4', width=3)))
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
        st.markdown('<div style="animation: fall-down 1.5s ease-out; color: #dc3545; font-weight: bold; background: #f8d7da; padding: 15px; border-radius: 10px;"><strong>총 손익금</strong><br>-₩100,000</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div style="animation: fall-down 1.5s ease-out; color: #dc3545; font-weight: bold; background: #f8d7da; padding: 15px; border-radius: 10px;"><strong>수익률</strong><br>-2.0%</div>', unsafe_allow_html=True)
    
    st.divider()
    
    st.markdown("### 보유 종목")
    st.markdown('<div class="warning-shake"><strong>삼성전자</strong> | <span style="color: #dc3545; font-weight: bold;">-2.14%</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="warning-shake"><strong>SK하이닉스</strong> | <span style="color: #dc3545; font-weight: bold;">-1.82%</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="success-float"><strong>현대차</strong> | <span style="color: #28a745; font-weight: bold;">+2.17%</span></div>', unsafe_allow_html=True)

# ============================================================================
# TAB 5: 설정
# ============================================================================

with tab5:
    st.subheader("⚙️ 설정 & 정보")
    
    st.markdown("#### 🎨 애니메이션 효과")
    
    st.markdown('<div class="success-float"><strong>✨ JSON 애니메이션</strong><br>헤더의 반짝이는 효과 + 아래위 흔들거림</div>', unsafe_allow_html=True)
    st.markdown('<div class="danger-pulse"><strong>🔴 맥박 애니메이션</strong><br>위험 신호의 깜빡이며 맥박치기</div>', unsafe_allow_html=True)
    st.markdown('<div class="warning-shake"><strong>⚠️ 흔들림 애니메이션</strong><br>경고 메시지의 좌우 흔들거림</div>', unsafe_allow_html=True)
    st.markdown('<div class="success-float"><strong>💼 포트폴리오 애니메이션</strong><br>수익/손실의 상승/하락 애니메이션</div>', unsafe_allow_html=True)

# 푸터
st.divider()
st.markdown("---\n🛡️ **GINI Guardian v2.1** | ✨ JSON + 깜빡임 + 흔들거림 | 💙 라이라 설계 × 미라클 구현")
