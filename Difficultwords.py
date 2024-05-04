import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
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

def fetch_youtube_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = ' '.join([line['text'] for line in transcript])
        return text
    except Exception as e:
        st.error(f"Error fetching transcript: {e}")
        return None

def find_difficult_words(text):
    difficult_words = []
    words = text.split()
    for word in words:
        if word.lower() not in common_words:
            difficult_words.append(word)
    return difficult_words

def main():
    st.title('YouTube Transcript Difficult Word Finder')

    video_id = st.text_input('Enter YouTube Video ID:')

    if st.button('Fetch Transcript'):
        text = fetch_youtube_transcript(video_id)
        if text:
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

if __name__ == "__main__":
    main()
