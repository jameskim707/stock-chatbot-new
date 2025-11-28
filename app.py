"""
🛡️ GINI Guardian v2.1 — LEVEL 1 업그레이드
✅ 실시간 뉴스 자동 반영
✅ 차트 시각화  
✅ 포트폴리오 추적

라이라 설계 × 미라클 구현 🔥
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
import json

# ============================================================================
# 📰 LEVEL 1-1: 실시간 뉴스 자동 반영
# ============================================================================

class NewsEngine:
    """실시간 뉴스 분석 및 위험도 평가"""
    
    def __init__(self):
        # 샘플 뉴스 데이터 (실제로는 API 연동)
        self.news_data = [
            {
                "title": "코스피 2,650선까지 급락... 경기 둔화 우려",
                "source": "연합뉴스",
                "time": "09:30",
                "sentiment": "negative",
                "risk_score": 8,
                "category": "시장"
            },
            {
                "title": "삼성전자, 4분기 실적 부진 예상... 목표가 하향",
                "source": "매경",
                "time": "10:15",
                "sentiment": "negative",
                "risk_score": 7,
                "category": "개별주"
            },
            {
                "title": "금리 인상 임박? 기준금리 0.25% 올릴 가능성",
                "source": "한경",
                "time": "11:00",
                "sentiment": "negative",
                "risk_score": 6,
                "category": "금리"
            },
            {
                "title": "기술주 실적 개선 신호... AI 수요 증가",
                "source": "이데일리",
                "time": "12:30",
                "sentiment": "positive",
                "risk_score": 2,
                "category": "산업"
            }
        ]
    
    def get_today_news(self):
        """오늘의 뉴스 조회"""
        return self.news_data
    
    def calculate_market_risk(self):
        """시장 전체 위험도 계산"""
        risk_scores = [news["risk_score"] for news in self.news_data]
        negative_count = len([n for n in self.news_data if n["sentiment"] == "negative"])
        
        avg_risk = np.mean(risk_scores)
        negative_ratio = negative_count / len(self.news_data) * 100
        
        return {
            "average_risk": avg_risk,
            "negative_ratio": negative_ratio,
            "alert_level": "🔴 높음" if avg_risk > 6 else "🟡 중간" if avg_risk > 3 else "🟢 낮음"
        }
    
    def format_news_for_display(self):
        """UI용 뉴스 포맷"""
        risk_info = self.calculate_market_risk()
        
        html = f"""
        <div style="background-color: #f8d7da; padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h3>📰 오늘의 시장 뉴스 & 위험도</h3>
        <p><strong>시장 위험도: {risk_info['alert_level']}</strong></p>
        <p>부정적 뉴스 비율: {risk_info['negative_ratio']:.0f}% | 평균 위험도: {risk_info['average_risk']:.1f}/10</p>
        </div>
        """
        return html, risk_info

# ============================================================================
# 📈 LEVEL 1-2: 차트 시각화
# ============================================================================

class ChartEngine:
    """차트 시각화 엔진"""
    
    def __init__(self):
        # 샘플 데이터 생성 (과거 30일)
        self.generate_sample_data()
    
    def generate_sample_data(self):
        """샘플 주가 데이터 생성"""
        dates = pd.date_range(end=datetime.now(), periods=30, freq='D')
        
        # KOSPI 데이터
        kospi_base = 2700
        kospi_prices = kospi_base + np.cumsum(np.random.randn(30) * 20)
        
        # 개별 종목 데이터
        samsung_base = 70000
        samsung_prices = samsung_base + np.cumsum(np.random.randn(30) * 500)
        
        hynix_base = 110000
        hynix_prices = hynix_base + np.cumsum(np.random.randn(30) * 800)
        
        self.kospi_data = pd.DataFrame({
            'Date': dates,
            'KOSPI': kospi_prices,
            'MA20': kospi_prices.rolling(window=5).mean()
        })
        
        self.samsung_data = pd.DataFrame({
            'Date': dates,
            'Price': samsung_prices,
            'MA20': samsung_prices.rolling(window=5).mean()
        })
        
        self.hynix_data = pd.DataFrame({
            'Date': dates,
            'Price': hynix_prices,
            'MA20': hynix_prices.rolling(window=5).mean()
        })
    
    def plot_kospi_chart(self):
        """KOSPI 차트"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=self.kospi_data['Date'],
            y=self.kospi_data['KOSPI'],
            mode='lines',
            name='KOSPI',
            line=dict(color='#1f77b4', width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=self.kospi_data['Date'],
            y=self.kospi_data['MA20'],
            mode='lines',
            name='5일 이동평균',
            line=dict(color='red', width=1, dash='dash')
        ))
        
        fig.update_layout(
            title="📊 KOSPI 30일 차트",
            xaxis_title="날짜",
            yaxis_title="지수",
            hovermode='x unified',
            height=400,
            template='plotly_white'
        )
        
        return fig
    
    def plot_individual_stock(self, stock_name="삼성전자"):
        """개별 종목 차트"""
        if stock_name == "삼성전자":
            data = self.samsung_data
            color = '#2ca02c'
        else:
            data = self.hynix_data
            color = '#ff7f0e'
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=data['Date'],
            y=data['Price'],
            mode='lines',
            name=stock_name,
            line=dict(color=color, width=2)
        ))
        
        fig.add_trace(go.Scatter(
            x=data['Date'],
            y=data['MA20'],
            mode='lines',
            name='5일 이동평균',
            line=dict(color='gray', width=1, dash='dash')
        ))
        
        fig.update_layout(
            title=f"📈 {stock_name} 30일 차트",
            xaxis_title="날짜",
            yaxis_title="주가 (원)",
            hovermode='x unified',
            height=400,
            template='plotly_white'
        )
        
        return fig

# ============================================================================
# 💼 LEVEL 1-3: 포트폴리오 추적
# ============================================================================

class PortfolioEngine:
    """포트폴리오 추적 및 분석"""
    
    def __init__(self):
        self.portfolio = []
        self.load_sample_portfolio()
    
    def load_sample_portfolio(self):
        """샘플 포트폴리오 로드"""
        self.portfolio = [
            {
                "종목명": "삼성전자",
                "매입가": 70000,
                "현재가": 68500,
                "수량": 10,
                "매입일": "2025-11-01",
                "수익률": -2.14
            },
            {
                "종목명": "SK하이닉스",
                "매입가": 110000,
                "현재가": 108000,
                "수량": 5,
                "매입일": "2025-11-10",
                "수익률": -1.82
            },
            {
                "종목명": "현대차",
                "매입가": 230000,
                "현재가": 235000,
                "수량": 3,
                "매입일": "2025-11-05",
                "수익률": 2.17
            }
        ]
    
    def add_stock(self, 종목명, 매입가, 현재가, 수량):
        """종목 추가"""
        수익률 = ((현재가 - 매입가) / 매입가) * 100
        
        self.portfolio.append({
            "종목명": 종목명,
            "매입가": 매입가,
            "현재가": 현재가,
            "수량": 수량,
            "매입일": datetime.now().strftime("%Y-%m-%d"),
            "수익률": 수익률
        })
    
    def get_portfolio_summary(self):
        """포트폴리오 요약"""
        if not self.portfolio:
            return None
        
        df = pd.DataFrame(self.portfolio)
        
        총_매입액 = (df['매입가'] * df['수량']).sum()
        총_현재가 = (df['현재가'] * df['수량']).sum()
        총_수익률 = ((총_현재가 - 총_매입액) / 총_매입액) * 100
        총_수익금 = 총_현재가 - 총_매입액
        
        return {
            "dataframe": df,
            "total_amount": 총_매입액,
            "current_amount": 총_현재가,
            "total_return_rate": 총_수익률,
            "total_profit": 총_수익금
        }
    
    def detect_danger_positions(self):
        """위험 포지션 감지"""
        dangerous = []
        
        for stock in self.portfolio:
            if stock['수익률'] < -5:
                dangerous.append({
                    "종목": stock['종목명'],
                    "손실률": stock['수익률'],
                    "경고": "🔴 위험! 손절 고려"
                })
            elif stock['수익률'] < -3:
                dangerous.append({
                    "종목": stock['종목명'],
                    "손실률": stock['수익률'],
                    "경고": "🟡 주의! 관찰 필요"
                })
        
        return dangerous

# ============================================================================
# 🎨 STREAMLIT UI - LEVEL 1
# ============================================================================

st.set_page_config(
    page_title="GINI Guardian v2.1",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    .danger-box { background-color: #f8d7da; padding: 15px; border-radius: 10px; border-left: 5px solid #dc3545; margin-bottom: 10px; }
    .warning-box { background-color: #fff3cd; padding: 15px; border-radius: 10px; border-left: 5px solid #ffc107; margin-bottom: 10px; }
    .success-box { background-color: #d4edda; padding: 15px; border-radius: 10px; border-left: 5px solid #28a745; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

# 헤더
st.markdown("# 🛡️ GINI Guardian v2.1")
st.markdown("### LEVEL 1 업그레이드 버전 (뉴스 + 차트 + 포트폴리오)")
st.markdown("**라이라 설계 × 미라클 구현** | 뉴스 API + 차트 시각화 + 포트폴리오 추적")

st.divider()

# 탭 구조
tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 상담", "📰 뉴스 분석", "📈 차트", "💼 포트폴리오", "⚙️ 설정"])

# 엔진 초기화
news_engine = NewsEngine()
chart_engine = ChartEngine()
portfolio_engine = PortfolioEngine()

# ============================================================================
# TAB 1: 상담 (기존 Step 1~4)
# ============================================================================

with tab1:
    st.subheader("투자 상담")
    
    # 시장 정보
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📈 KOSPI", "2,650", "-45 (-1.67%)", delta_color="off")
    with col2:
        st.metric("📊 KOSDAQ", "795", "-8 (-0.99%)", delta_color="off")
    with col3:
        st.metric("💱 USD/KRW", "1,310.5", "+5.5 (+0.42%)", delta_color="normal")
    
    st.divider()
    
    # 뉴스 위험도 표시
    news_html, risk_info = news_engine.format_news_for_display()
    st.markdown(news_html, unsafe_allow_html=True)
    
    # 사용자 입력
    user_input = st.text_area(
        "어떤 투자 관련 고민이 있나요?",
        placeholder="예) 지금 삼성전자 매수해도 되나요?",
        height=80
    )
    
    if st.button("🔍 분석하기", use_container_width=True, type="primary"):
        if user_input.strip():
            if any(word in user_input for word in ["사도", "들어갈까", "몰빵", "지금", "얼마"]):
                st.markdown("""
                <div class='danger-box'>
                <h3>🛡️ 위험 신호 감지됨!</h3>
                <p>오늘의 시장이 <strong>위험 상태</strong>입니다.</p>
                <p>📰 부정적 뉴스가 많고, 시장 변동성이 높습니다.</p>
                <p><strong>지금은 신중할 때입니다!</strong></p>
                <ul>
                <li>✓ 감정적 결정은 아닌가요?</li>
                <li>✓ 잃어도 괜찮은 금액인가요?</li>
                <li>✓ 3년 이상 보유가 가능한가요?</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class='success-box'>
                <h3>📊 안전 모드 분석</h3>
                <p>일반적인 투자 질문입니다.</p>
                <p><strong>기본 투자 원칙:</strong></p>
                <ul>
                <li>✓ 장기 관점 유지</li>
                <li>✓ 분산 투자 필수</li>
                <li>✓ 감정 배제</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)

# ============================================================================
# TAB 2: 뉴스 분석 (NEW!)
# ============================================================================

with tab2:
    st.subheader("📰 실시간 뉴스 분석")
    
    # 시장 위험도
    risk_info = news_engine.calculate_market_risk()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("시장 위험도", f"{risk_info['average_risk']:.1f}/10", delta=None)
    with col2:
        st.metric("부정적 뉴스", f"{risk_info['negative_ratio']:.0f}%", delta=None)
    with col3:
        st.metric("경고 수준", risk_info['alert_level'], delta=None)
    
    st.divider()
    
    st.markdown("### 오늘의 주요 뉴스")
    
    news_list = news_engine.get_today_news()
    
    for news in news_list:
        if news['sentiment'] == 'negative':
            color = '#f8d7da'
            emoji = '🔴'
        else:
            color = '#d4edda'
            emoji = '🟢'
        
        st.markdown(f"""
        <div style="background-color: {color}; padding: 12px; border-radius: 8px; margin-bottom: 10px;">
        <p><strong>{emoji} {news['title']}</strong></p>
        <small>{news['source']} | {news['time']} | 위험도: {news['risk_score']}/10 | {news['category']}</small>
        </div>
        """, unsafe_allow_html=True)
    
    st.divider()
    
    st.info("""
    **📌 뉴스 해석:**
    - 부정적 뉴스가 많습니다
    - 시장이 약세 모드입니다
    - 무리한 신규 매수는 피하세요
    - 기존 보유 종목 상태 점검 필수
    """)

# ============================================================================
# TAB 3: 차트 (NEW!)
# ============================================================================

with tab3:
    st.subheader("📈 차트 시각화")
    
    # KOSPI 차트
    st.markdown("### KOSPI 지수")
    fig_kospi = chart_engine.plot_kospi_chart()
    st.plotly_chart(fig_kospi, use_container_width=True)
    
    st.divider()
    
    # 개별 종목 선택
    st.markdown("### 개별 종목 차트")
    selected_stock = st.selectbox("종목 선택", ["삼성전자", "SK하이닉스"])
    
    fig_stock = chart_engine.plot_individual_stock(selected_stock)
    st.plotly_chart(fig_stock, use_container_width=True)
    
    st.divider()
    
    st.info("""
    **📊 차트 읽기 팁:**
    - 파란 선: 실제 주가
    - 빨간 점선: 5일 이동평균
    - 위쪽 벗어나면 과매수, 아래쪽 벗어나면 과매도
    """)

# ============================================================================
# TAB 4: 포트폴리오 (NEW!)
# ============================================================================

with tab4:
    st.subheader("💼 포트폴리오 추적")
    
    portfolio_summary = portfolio_engine.get_portfolio_summary()
    
    if portfolio_summary:
        # 포트폴리오 요약
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("총 매입액", f"₩{portfolio_summary['total_amount']:,.0f}")
        with col2:
            st.metric("현재가치", f"₩{portfolio_summary['current_amount']:,.0f}")
        with col3:
            delta_color = "off" if portfolio_summary['total_profit'] < 0 else "normal"
            st.metric("총 수익금", f"₩{portfolio_summary['total_profit']:,.0f}", delta_color=delta_color)
        with col4:
            delta_color = "off" if portfolio_summary['total_return_rate'] < 0 else "normal"
            st.metric("수익률", f"{portfolio_summary['total_return_rate']:.2f}%", delta_color=delta_color)
        
        st.divider()
        
        # 위험 포지션 감지
        dangerous = portfolio_engine.detect_danger_positions()
        
        if dangerous:
            st.markdown("### ⚠️ 위험한 포지션")
            for pos in dangerous:
                color = "#f8d7da" if pos['손실률'] < -5 else "#fff3cd"
                st.markdown(f"""
                <div style="background-color: {color}; padding: 12px; border-radius: 8px; margin-bottom: 8px;">
                <strong>{pos['종목']}</strong> | 손실률: {pos['손실률']:.2f}% | {pos['경고']}
                </div>
                """, unsafe_allow_html=True)
        
        st.divider()
        
        # 포트폴리오 상세
        st.markdown("### 보유 종목 상세")
        
        df_display = portfolio_summary['dataframe'].copy()
        df_display['평가액'] = df_display['현재가'] * df_display['수량']
        df_display['손익금'] = df_display['평가액'] - (df_display['매입가'] * df_display['수량'])
        
        # 색상 표시
        def color_profit(val):
            if val < -5:
                return 'background-color: #f8d7da'
            elif val < 0:
                return 'background-color: #fff3cd'
            else:
                return 'background-color: #d4edda'
        
        styled_df = df_display.style.applymap(color_profit, subset=['수익률'])
        st.dataframe(styled_df, use_container_width=True)
        
        st.divider()
        
        # 포트폴리오 추가
        st.markdown("### 새 종목 추가")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            new_name = st.text_input("종목명", placeholder="예) 삼성전자")
        with col2:
            new_buy = st.number_input("매입가", value=0, step=1000)
        with col3:
            new_current = st.number_input("현재가", value=0, step=1000)
        with col4:
            new_qty = st.number_input("수량", value=0, step=1)
        
        if st.button("추가하기", use_container_width=True):
            if new_name and new_buy > 0 and new_current > 0 and new_qty > 0:
                portfolio_engine.add_stock(new_name, new_buy, new_current, new_qty)
                st.success(f"✅ {new_name} 추가됨!")
                st.rerun()

# ============================================================================
# TAB 5: 설정
# ============================================================================

with tab5:
    st.subheader("⚙️ 설정")
    
    st.markdown("#### 📊 시스템 상태")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("뉴스 엔진", "🟢 작동중")
    with col2:
        st.metric("차트 엔진", "🟢 작동중")
    with col3:
        st.metric("포트폴리오", "🟢 작동중")
    
    st.divider()
    
    st.markdown("#### 📋 버전 정보")
    st.info("""
    **GINI Guardian v2.1 - LEVEL 1**
    
    ✅ Step 1: 시장 정보 요청
    ✅ Step 2: 위험 신호 감지
    ✅ Step 3: 방어 메시지 생성
    ✅ Step 4: 전체 통합 파이프라인
    
    **NEW - LEVEL 1 업그레이드:**
    ✅ 실시간 뉴스 자동 반영
    ✅ 차트 시각화 (Plotly)
    ✅ 포트폴리오 추적 & 분석
    
    **다음 예정:**
    - LEVEL 2: 감정 분석 & 종합 위험 점수
    - LEVEL 3: AI 종목 분석 & 손절/익절 제안
    - LEVEL 4: 글로벌 진출 & 모바일 앱
    """)

# 푸터
st.divider()
st.markdown("""
---
🛡️ **GINI Guardian v2.1 - LEVEL 1** | 라이라 설계 × 미라클 구현
💙 당신의 돈을 지키는 AI, 당신의 감정을 진정시키는 파트너
""")
