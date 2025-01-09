import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
import re
import openai
from typing import Optional

from comento_func import openai_response

# Streamlit 페이지 설정
st.set_page_config(page_title="YouTube 영상 요약", page_icon="🎥")
st.title("YouTube 영상 요약 프로그램")

# YouTube URL에서 영상 ID를 추출하는 함수
def extract_video_id(url: str) -> Optional[str]:
    video_id = None
    if 'youtu.be' in url:
        video_id = url.split('/')[-1]
    elif 'youtube.com' in url:
        match = re.search(r'v=([^&]*)', url)
        if match:
            video_id = match.group(1)
    return video_id


# 자막을 텍스트로 변환하는 함수
def get_transcript(video_id: str) -> Optional[str]:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['ko'])
        return ' '.join([t['text'] for t in transcript])
    except Exception as e:
        return None

# 텍스트 청크로 나누기
def split_text(text: str, max_length: int = 4000) -> list:
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0

    for word in words:
        if current_length + len(word) + 1 > max_length:
            chunks.append(' '.join(current_chunk))
            current_chunk = [word]
            current_length = len(word)
        else:
            current_chunk.append(word)
            current_length += len(word) + 1

    if current_chunk:
        chunks.append(' '.join(current_chunk))

    return chunks


# 메인 애플리케이션
def main():
    st.write("YouTube 영상의 URL을 입력하면 내용을 요약해드립니다.")

    # URL 입력 받기
    url = st.text_input("YouTube URL을 입력하세요:")

    if url:
        try:
            # 영상 ID 추출
            video_id = extract_video_id(url)
            if video_id:
                # 영상 임베딩 표시
                st.video(url)

                # 자막 가져오기
                transcript = get_transcript(video_id)

                if transcript:
                    st.subheader("영상 요약")
                    with st.spinner('영상을 요약하고 있습니다...'):
                        # 긴 텍스트 처리를 위해 청크로 나누기
                        chunks = split_text(transcript)

                        # 각 청크에 대해 요약 수행
                        all_summaries = []
                        for chunk in chunks:
                            summary = openai_response(chunk)
                            all_summaries.append(summary)

                        # 전체 요약 표시
                        final_summary = "\n\n".join(all_summaries)
                        st.markdown(final_summary)

                else:
                    st.error("자막을 가져올 수 없습니다. 영상에 자막이 있는지 확인해주세요.")
            else:
                st.error("올바른 YouTube URL을 입력해주세요.")

        except Exception as e:
            st.error(f"오류가 발생했습니다: {str(e)}")


if __name__ == "__main__":
    main()
