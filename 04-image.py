import streamlit as st
import base64
from PIL import Image
import io

from comento_func import stable_large, stable_core, openai_response


def main():
    st.title("AI 이미지 생성기")

    # 프롬프트 입력 받기
    prompt = st.text_area("이미지 생성을 위한 프롬프트를 입력하세요:", height=100)

    if st.button("이미지 생성"):
        if prompt:
            try:
                # 로딩 표시
                with st.spinner('프롬프트 번역 및 이미지 생성중...'):
                    # 한글 프롬프트를 영어로 변환하는 요청 생성
                    translation_prompt = f"다음 텍스트를 이미지 생성에 적합한 영어 프롬프트로 번역해주세요: {prompt}"
                    english_prompt = openai_response(translation_prompt)

                    # 번역된 프롬프트 표시 (선택사항)
                    st.write("번역된 프롬프트:", english_prompt)

                    # stable_large 함수를 통해 이미지 생성 (영문 프롬프트 사용)
                    image_base64 = stable_core(english_prompt)

                    # base64 디코딩 및 이미지 표시
                    image_data = base64.b64decode(image_base64)
                    image = Image.open(io.BytesIO(image_data))

                    # 이미지 표시
                    st.image(image, caption=f"생성된 이미지: {prompt}")

                    # 다운로드 버튼 추가
                    st.download_button(
                        label="이미지 다운로드",
                        data=image_data,
                        file_name="generated_image.png",
                        mime="image/png"
                    )

            except Exception as e:
                st.error(f"이미지 생성 중 오류가 발생했습니다: {str(e)}")
        else:
            st.warning("프롬프트를 입력해주세요!")


if __name__ == "__main__":
    main()
