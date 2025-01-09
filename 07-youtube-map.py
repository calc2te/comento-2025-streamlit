import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re
import folium
from streamlit_folium import folium_static
import json
from typing import Optional

from comento_func import openai_response

# Streamlit 페이지 설정
st.set_page_config(page_title="YouTube 맛집 지도", page_icon="🍽️")
st.title("YouTube 맛집 지도 프로그램")


def extract_video_id(url: str) -> Optional[str]:
    video_id = None
    if 'youtu.be' in url:
        video_id = url.split('/')[-1]
    elif 'youtube.com' in url:
        match = re.search(r'v=([^&]*)', url)
        if match:
            video_id = match.group(1)
    return video_id


def get_transcript(video_id: str) -> Optional[str]:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
        return ' '.join([t['text'] for t in transcript])
    except Exception as e:
        return None


def extract_restaurant_info(text: str) -> list:
    prompt = f"""
    다음 텍스트에서 맛집 정보를 추출해서 JSON 형식으로 반환해주세요.
    각 맛집마다 다음 정보를 포함해주세요:
    - name: 가게 이름
    - address: 가능한 한 상세한 주소 (도로명 주소 또는 지번 주소)
    - description: 음식점 특징, 대표 메뉴 등 간단한 설명

    JSON 형식으로만 응답해주세요:
    [
        {{"name": "가게이름", "address": "상세주소", "description": "설명"}},
        ...
    ]

    텍스트:
    {text}
    """

    try:
        response = openai_response(prompt)
        print(response)
        # 응답에서 JSON 부분만 추출
        json_str = response[response.find('['):response.rfind(']') + 1]
        restaurants = json.loads(json_str)

        # 각 맛집의 좌표 정보 추가
        for restaurant in restaurants:
            coords = get_coordinates(restaurant['address'])
            restaurant['latitude'] = coords[0]
            restaurant['longitude'] = coords[1]

        return restaurants
    except Exception as e:
        st.error(f"맛집 정보 추출 중 오류 발생: {str(e)}")
        return []


def get_coordinates(address: str) -> tuple:
    prompt = f"""
    다음 주소의 위도와 경도를 알려주세요.
    정확한 좌표를 모르는 경우, 가장 근접한 위치의 좌표를 알려주세요.
    반드시 아래 형식으로만 답변해주세요.

    주소: {address}

    응답 형식:
    latitude: [위도]
    longitude: [경도]
    """

    try:
        response = openai_response(prompt)
        print(response)
        # 응답에서 위도와 경도 추출
        latitude = float(re.search(r'latitude: ([\d.]+)', response).group(1))
        longitude = float(re.search(r'longitude: ([\d.]+)', response).group(1))
        return (latitude, longitude)
    except Exception as e:
        st.warning(f"주소 변환 중 오류 발생: {str(e)}")
        # 오류 발생시 서울 중심 좌표 반환
        return (37.5665, 126.9780)


def create_map(restaurants: list) -> folium.Map:
    # 첫 번째 맛집 위치 또는 서울 중심을 기준으로 지도 생성
    if restaurants:
        center_lat = restaurants[0]['latitude']
        center_lng = restaurants[0]['longitude']
    else:
        center_lat, center_lng = 37.5665, 126.9780

    m = folium.Map(location=[center_lat, center_lng], zoom_start=12)

    for restaurant in restaurants:
        folium.Marker(
            [restaurant['latitude'], restaurant['longitude']],
            popup=folium.Popup(
                f"""
                <b>{restaurant['name']}</b><br>
                주소: {restaurant['address']}<br>
                설명: {restaurant['description']}
                """,
                max_width=300
            )
        ).add_to(m)

    return m


def main():
    st.write("YouTube 맛집 영상의 URL을 입력하면 영상에 나온 맛집들을 지도에 표시해드립니다.")

    url = st.text_input("YouTube URL을 입력하세요:")

    if url:
        try:
            video_id = extract_video_id(url)
            if video_id:
                st.video(url)

                transcript = get_transcript(video_id)

                if transcript:
                    with st.spinner('맛집 정보를 추출하고 있습니다...'):
                        # 맛집 정보 추출
                        restaurants = extract_restaurant_info(transcript)

                        if restaurants:
                            st.subheader("발견된 맛집 목록")
                            for restaurant in restaurants:
                                st.write(f"🏪 {restaurant['name']}")
                                st.write(f"📍 {restaurant['address']}")
                                st.write(f"ℹ️ {restaurant['description']}")
                                st.write("---")

                            st.subheader("맛집 지도")
                            m = create_map(restaurants)
                            folium_static(m)
                        else:
                            st.warning("영상에서 맛집 정보를 찾을 수 없습니다.")

                else:
                    st.error("자막을 가져올 수 없습니다. 영상에 자막이 있는지 확인해주세요.")
            else:
                st.error("올바른 YouTube URL을 입력해주세요.")

        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")


if __name__ == "__main__":
    main()
