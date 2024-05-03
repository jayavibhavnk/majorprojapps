import streamlit as st
import time
from youtube_transcript_api import YouTubeTranscriptApi
from streamlit_player import st_player

# Get the transcript of the YouTube video
transcript_list = YouTubeTranscriptApi.list_transcripts(video_id="L_JQOH1tEEA")
script1 = transcript_list.find_transcript(['en'])
script2 = script1.translate('de')
script1 = script1.fetch()
script2 = script2.fetch()
# Display the video
# st.video("https://www.youtube.com/watch?v=L_JQOH1tEEA", autoplay=True)
st_player("https://www.youtube.com/watch?v=L_JQOH1tEEA", controls = True)

# Display subtitles dynamically
subtitle_placeholder = st.empty()
sub2 = st.empty()
if st.button("transcripts"):
    for i in range(len(script1)):
        current_subtitle = script1[i]['text']
        cur1 = script2[i]['text']
        subtitle_placeholder.markdown(f"{current_subtitle}")
        sub2.markdown(f"{cur1}")
        time.sleep(script1[i]["duration"])
        subtitle_placeholder.empty()
        sub2.empty()
