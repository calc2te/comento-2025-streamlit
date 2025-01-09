# 필요한 라이브러리 임포트
import streamlit as st  # 웹 애플리케이션 생성을 위한 라이브러리
import pandas as pd    # 데이터 처리를 위한 라이브러리
import numpy as np     # 수치 계산을 위한 라이브러리

# 랜덤 데이터 생성 함수 정의
# @st.cache_data: 함수의 결과를 캐시하여 동일한 입력에 대해 재계산하지 않도록 함
# 이를 통해 페이지가 다시 로드되거나 상호작용이 발생해도 데이터가 유지됨
@st.cache_data
def generate_random_data():
    # 20행 3열의 랜덤 데이터 생성
    # np.random.randn(): 표준 정규 분포를 따르는 난수 생성
    # columns: 데이터프레임의 열 이름을 A, B, C로 지정
    return pd.DataFrame(
        np.random.randn(20, 3),
        columns=['A', 'B', 'C']
    )

# 웹 페이지의 메인 타이틀 설정
# st.title(): 큰 글씨로 페이지 제목을 표시
st.title('간단한 Streamlit 예시')

# ===== 섹션 1: 텍스트 입력 예시 =====
st.header('1. 텍스트 입력 예시')
# st.text_input(): 사용자로부터 텍스트 입력을 받는 입력 필드 생성
name = st.text_input('이름을 입력하세요')
# 입력된 이름이 있을 경우에만 환영 메시지 출력
if name:
    st.write(f'안녕하세요, {name}님!')

# ===== 섹션 2: 슬라이더 예시 =====
st.header('2. 슬라이더 예시')
# st.slider(): 슬라이더 위젯 생성
# 매개변수: 레이블, 최소값, 최대값, 기본값
age = st.slider('나이를 선택하세요', 0, 100, 25)
# 선택된 나이 값 출력
st.write(f'선택한 나이: {age}세')

# ===== 섹션 3: 차트 예시 =====
st.header('3. 차트 예시')
# 캐시된 함수를 호출하여 차트 데이터 생성
chart_data = generate_random_data()
# st.line_chart(): 라인 차트 생성
# 데이터프레임의 각 열이 하나의 선으로 표시됨
st.line_chart(chart_data)

# ===== 섹션 4: 체크박스 예시 =====
st.header('4. 체크박스 예시')
# st.checkbox(): 체크박스 위젯 생성
# 체크박스가 선택되면 데이터프레임을 표시
if st.checkbox('데이터 보기'):
    st.write(chart_data)  # 원본 데이터를 테이블 형태로 표시

# ===== 섹션 5: 선택박스 예시 =====
st.header('5. 선택박스 예시')
# st.selectbox(): 드롭다운 선택 메뉴 생성
# 매개변수: 레이블, 선택 옵션 리스트
option = st.selectbox(
    '좋아하는 색상을 선택하세요',
    ['빨강', '파랑', '초록', '노랑']
)
# 선택된 옵션 출력
st.write(f'당신이 선택한 색상: {option}')

# ===== 데이터 새로고침 기능 =====
# st.button(): 클릭 가능한 버튼 생성
if st.button('새로운 차트 데이터 생성'):
    # st.cache_data.clear(): 캐시된 데이터를 모두 삭제
    st.cache_data.clear()
    # 새로운 데이터 생성 및 차트 업데이트
    chart_data = generate_random_data()
    st.line_chart(chart_data)

"""
실행 방법:
1. 위 코드를 .py 파일로 저장 (예: app.py)
2. 터미널에서 다음 명령어 실행:
   streamlit run app.py

주요 특징:
- Streamlit은 파이썬 스크립트를 위에서 아래로 실행하며 웹 앱을 구성
- 모든 위젯(@st.cache_data로 장식된 것 제외)은 사용자 상호작용 시 스크립트를 재실행
- 캐시를 사용하여 데이터 재계산을 방지하고 성능을 최적화
"""
