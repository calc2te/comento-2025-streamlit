import streamlit as st
from typing import List

from comento_func import openai_response

# Streamlit 페이지 설정
st.set_page_config(page_title="AI 요리 레시피 생성기", page_icon="🧑‍🍳")


def generate_recipe(ingredients: List[str], cuisine_type: str = None) -> str:
    """AI를 사용하여 레시피를 생성하는 함수"""

    # 요리 종류가 지정된 경우와 아닌 경우의 프롬프트 설정
    if cuisine_type:
        prompt = f"""다음 재료를 사용하여 {cuisine_type} 요리 레시피를 만들어주세요:
        재료: {', '.join(ingredients)}

        다음 형식으로 답변해주세요:

        [요리 이름]

        소요 시간: 
        난이도: 

        1. 필요한 재료
        - 주재료:
        - 양념:

        2. 상세 조리 순서
        (단계별로 자세히 설명)

        3. 조리 팁

        4. 영양 정보
        """
    else:
        prompt = f"""다음 재료를 활용해서 만들 수 있는 가장 적합한 요리의 레시피를 알려주세요:
        재료: {', '.join(ingredients)}

        다음 형식으로 답변해주세요:

        [요리 이름]

        소요 시간: 
        난이도: 

        1. 필요한 재료
        - 주재료:
        - 양념:

        2. 상세 조리 순서
        (단계별로 자세히 설명)

        3. 조리 팁

        4. 영양 정보
        """

    try:
        # openai_response 함수 사용
        response = openai_response(prompt)
        return response
    except Exception as e:
        return f"레시피 생성 중 오류가 발생했습니다: {str(e)}"


# 메인 앱 UI
st.title("🧑‍🍳 AI 요리 레시피 생성기")
st.write("가지고 있는 재료를 입력하면 AI가 레시피를 추천해드립니다!")

# 재료 입력
ingredients_input = st.text_area("재료를 쉼표(,)로 구분하여 입력해주세요", height=100)
cuisine_types = ["선택 안함", "한식", "중식", "일식", "양식", "기타"]
cuisine_type = st.selectbox("원하는 요리 종류를 선택하세요", cuisine_types)

# 버튼 생성
if st.button("레시피 생성"):
    if ingredients_input.strip():
        ingredients = [i.strip() for i in ingredients_input.split(',') if i.strip()]

        # 로딩 스피너 표시
        with st.spinner('AI가 레시피를 생성하고 있습니다...'):
            selected_cuisine = None if cuisine_type == "선택 안함" else cuisine_type
            recipe = generate_recipe(ingredients, selected_cuisine)

        # 결과 표시
        st.markdown("### 🍳 생성된 레시피")
        st.markdown(recipe)

        # 레시피 저장 버튼
        if st.button("레시피 저장하기"):
            try:
                with open("recipe.txt", "w", encoding="utf-8") as f:
                    f.write(recipe)
                st.success("레시피가 recipe.txt 파일로 저장되었습니다!")
            except Exception as e:
                st.error(f"저장 중 오류가 발생했습니다: {str(e)}")
    else:
        st.warning("재료를 입력해주세요!")

# 사이드바에 사용 방법 추가
with st.sidebar:
    st.header("사용 방법")
    st.markdown("""
    1. 가지고 있는 재료들을 입력창에 쉼표로 구분하여 입력하세요
    2. 원하는 요리 종류를 선택하세요 (선택사항)
    3. '레시피 생성' 버튼을 클릭하세요
    4. 생성된 레시피를 저장하고 싶다면 '레시피 저장하기' 버튼을 클릭하세요
    """)

    st.header("예시 재료")
    st.markdown("""
    감자, 양파, 당근, 돼지고기
    """)

# 주의사항 표시
st.markdown("---")
st.markdown("### ⚠️ 주의사항")
st.markdown("""
- 생성된 레시피는 참고용으로만 사용해주세요
- 알레르기가 있는 재료는 미리 확인해주세요
""")
