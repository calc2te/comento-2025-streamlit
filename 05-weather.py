import streamlit as st
import requests
from bs4 import BeautifulSoup

from comento_func import openai_response


def get_clothing_recommendation(temperature):
    # AI에게 보낼 프롬프트 작성
    prompt = f"""현재 기온이 {temperature}입니다. 
    이런 날씨에 적합한 옷차림을 추천해주세요. 
    다음 포맷으로 답변해주세요:
    1. 추천 옷차림 (간단히 1-2문장)
    2. 필수 아이템 (2-3개)
    3. 주의사항 (날씨 관련 1개)
    """

    # AI 응답 받기
    recommendation = openai_response(prompt)
    return recommendation


def get_weather():
    # 네이버 날씨 페이지 URL (서울 기준)
    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=서울+날씨"

    # HTTP 요청
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    response = requests.get(url, headers=headers)

    # BeautifulSoup 객체 생성
    soup = BeautifulSoup(response.text, 'html.parser')

    # 현재 온도
    temperature = soup.select_one('.temperature_text').text.strip()[5:]  # '현재 온도' 텍스트 제거

    # 날씨 상태
    weather_status = soup.select_one('.weather_main').text.strip()

    # 체감 온도
    felt_temp = soup.select_one('.temperature_info .desc').text.strip()

    # 미세먼지 정보
    dust_info = soup.select('.report_card_wrap span.txt')
    dust = dust_info[0].text.strip()  # 미세먼지
    ultra_dust = dust_info[1].text.strip()  # 초미세먼지

    return {
        'temperature': temperature,
        'status': weather_status,
        'felt_temp': felt_temp,
        'dust': dust,
        'ultra_dust': ultra_dust
    }


def main():
    st.title('서울 날씨 정보 & 옷차림 추천')

    # 새로고침 버튼
    if st.button('날씨 새로고침'):
        st.experimental_rerun()

    try:
        weather_info = get_weather()

        # 날씨 정보 표시
        col1, col2 = st.columns(2)

        with col1:
            st.metric(label="현재 온도", value=weather_info['temperature'])
            st.write(f"체감 온도: {weather_info['felt_temp']}")

        with col2:
            st.write(f"날씨 상태: {weather_info['status']}")
            st.write(f"미세먼지: {weather_info['dust']}")
            st.write(f"초미세먼지: {weather_info['ultra_dust']}")

        # 구분선 추가
        st.markdown("---")

        # 옷차림 추천 섹션
        st.subheader("🎽 오늘의 옷차림 추천")

        # 현재 온도에서 숫자만 추출 (예: "18.9°" -> "18.9")
        temp_num = float(weather_info['temperature'].replace('°', ''))

        # AI 옷차림 추천 받기
        clothing_recommendation = get_clothing_recommendation(temp_num)

        # 추천 내용 표시
        st.markdown(clothing_recommendation)

        # 주의사항 표시 (미세먼지 관련)
        if '나쁨' in weather_info['dust'] or '나쁨' in weather_info['ultra_dust']:
            st.warning('⚠️ 미세먼지가 나쁨 수준이니 마스크 착용을 권장합니다.')

    except Exception as e:
        st.error(f"날씨 정보를 가져오는 중 오류가 발생했습니다: {str(e)}")


if __name__ == "__main__":
    main()
