import streamlit as st
import time
from youtube_transcript_api import YouTubeTranscriptApi
from streamlit_player import st_player
import requests
import re

# Fetching common English words from GitHub
english_most_common_10k = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-usa-no-swears.txt'
response = requests.get(english_most_common_10k)
common_words = set(response.text.strip().split('\n'))

def preprocess_text(text):
    # Remove punctuation except for hyphens and apostrophes
    text = re.sub(r'[^\w\s-]', '', text)
    return text

def fetch_youtube_transcript(video_id, language='en'):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        transcript = transcript_list.find_transcript([language]).fetch()
        text = ' '.join([line['text'] for line in transcript])
        return transcript, text
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None, None

def find_difficult_words(text):
    difficult_words = []
    words = text.split()
    for word in words:
        if word.lower() not in common_words:
            difficult_words.append(word)
    return difficult_words

def main():
    st.title('YouTube Transcript and Analysis Tool')

    # User inputs
    video_url = st.text_input("Enter a YouTube video URL:")
    target_language = st.selectbox('Select target language for translation:', ('en', 'kn'))

    if video_url:
        video_id = video_url.split("v=")[-1]

        # Fetch and display transcripts
        if st.button('Fetch Transcript'):
            transcript, text = fetch_youtube_transcript(video_id, 'en')
            if transcript:
                st.write('Transcript fetched successfully.')
                st.text_area('Transcript:', value=text, height=200)
                text = preprocess_text(text)
                difficult_words = find_difficult_words(text)
                if difficult_words:
                    st.write('Difficult words found:')
                    for word in difficult_words:
                        st.write(word)
                else:
                    st.write('No difficult words found.')
            else:
                st.error('Failed to fetch transcript. Please check the video ID.')

        # Display video
        st_player(video_url, controls=True)

        # Display subtitles dynamically
        subtitle_placeholder = st.empty()
        translated_placeholder = st.empty()

        if st.button("Show Transcripts"):
            try:
                transcript_en, _ = fetch_youtube_transcript(video_id, 'en')
                transcript_target, _ = fetch_youtube_transcript(video_id, target_language)

                if transcript_en and transcript_target:
                    for i in range(len(transcript_en)):
                        original_subtitle = transcript_en[i]['text']
                        translated_subtitle = transcript_target[i]['text']
                        subtitle_placeholder.markdown(f"**Original (EN):** {original_subtitle}")
                        translated_placeholder.markdown(f"**Translated ({target_language.upper()}):** {translated_subtitle}")
                        time.sleep(transcript_en[i]["duration"])
                        subtitle_placeholder.empty()
                        translated_placeholder.empty()
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
