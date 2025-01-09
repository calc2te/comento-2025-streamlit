import streamlit as st
import pandas as pd
import plotly.express as px

from comento_func import claude_response

# 페이지 설정
st.set_page_config(page_title="데이터 시각화 및 AI 분석", layout="wide")

# 제목
st.title("CSV 데이터 시각화 및 AI 분석")

# 파일 업로더
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=['csv'])

if uploaded_file is not None:
    # 데이터 읽기
    df = pd.read_csv(uploaded_file)

    # 데이터 미리보기
    st.subheader("데이터 미리보기")
    st.dataframe(df)

    # 차트 생성 (두 개의 열로 나누어 표시)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("선 그래프")
        fig_line = px.line(
            df,
            x=df.columns[0],
            y=df.columns[1],
            title="시계열 트렌드"
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with col2:
        st.subheader("막대 그래프")
        fig_bar = px.bar(
            df,
            x=df.columns[0],
            y=df.columns[1],
            title="월별 데이터 분포"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # 기본 통계 정보
    st.subheader("기본 통계 정보")
    st.write(df.describe())

    # AI 분석
    st.subheader("AI 분석")

    # 데이터 특성 추출
    latest_value = df.iloc[-1][df.columns[1]]
    max_value = df[df.columns[1]].max()
    min_value = df[df.columns[1]].min()
    avg_value = df[df.columns[1]].mean()

    # AI 프롬프트 생성
    start_date = str(df.iloc[0][df.columns[0]])
    end_date = str(df.iloc[-1][df.columns[0]])
    latest = str(latest_value)
    maximum = str(max_value)
    minimum = str(min_value)
    average = f"{avg_value:.2f}"

    prompt = f"""
    다음 데이터를 분석하고 향후 트렌드를 예측해주세요:

    기간: {start_date} 부터 {end_date} 까지
    최근 값: {latest}
    최대값: {maximum}
    최소값: {minimum}
    평균값: {average}

    다음 내용을 포함해서 분석해주세요:
    1. 현재까지의 트렌드 분석
    2. 주요 변동 시점과 가능한 원인
    3. 향후 3개월간의 예상 트렌드
    4. 데이터 기반 제안사항
    """

    # AI 응답 받기
    ai_response = claude_response(prompt)

    # AI 분석 결과 표시
    with st.expander("AI 분석 결과 보기", expanded=True):
        st.write(ai_response)

        # 주요 지표 표시
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("최근 값", f"{latest_value:,.0f}")
        with col2:
            st.metric("최대값", f"{max_value:,.0f}")
        with col3:
            st.metric("최소값", f"{min_value:,.0f}")
        with col4:
            st.metric("평균값", f"{avg_value:,.0f}")

else:
    st.info("CSV 파일을 업로드해주세요.")
