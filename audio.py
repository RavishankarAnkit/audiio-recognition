import streamlit as st
from audio_recorder_streamlit import audio_recorder
from acrcloud.recognizer import ACRCloudRecognizer
import tempfile
import json

# ACRCloud Credentials
host = "identify-ap-southeast-1.acrcloud.com"

access_key = "2c4514325ba5e950e2d927ddfa75523b"

access_secret = "YOUR_SECRET_KEY"


# ACRCloud Configuration
config = {
    'host': host,
    'access_key': access_key,
    'access_secret': access_secret,
    'timeout': 10
}

recognizer = ACRCloudRecognizer(config)

# Streamlit Page
st.set_page_config(page_title="PragyanAI Song Recognizer")

st.title("🎵 PragyanAI Song Recognizer")

st.write("Record any song to identify it")

# Audio Recorder
audio_bytes = audio_recorder(
    text="Click to Record Song",
    recording_color="#ff0000",
    neutral_color="#6aa36f",
    icon_name="microphone",
    icon_size="2x",
)

if audio_bytes:

    st.audio(audio_bytes, format="audio/wav")

    if st.button("Recognize Song"):

        with st.spinner("Recognizing song..."):

            try:

                # Save temporary audio
                with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as f:
                    f.write(audio_bytes)
                    temp_audio = f.name

                # Recognize Song
                result = recognizer.recognize_by_file(temp_audio, 0)

                data = json.loads(result)

                music = data['metadata']['music'][0]

                # Song Details
                song_name = music.get('title', 'Unknown')

                artist = music['artists'][0].get('name', 'Unknown')

                album = music.get('album', {}).get('name', 'Unknown')

                release_date = music.get('release_date', 'Unknown')

                st.success(f"🎵 Song Name: {song_name}")

                st.info(f"🎤 Singer: {artist}")

                st.info(f"💿 Album: {album}")

                st.info(f"📅 Release Date: {release_date}")

                # Genre
                if 'genres' in music:

                    genres = [g['name'] for g in music['genres']]

                    st.write("🎼 Genres:", ", ".join(genres))

                # Extra Metadata
                if 'external_metadata' in music:

                    metadata = music['external_metadata']

                    st.write("## Extra Information")

                    if 'spotify' in metadata:
                        st.success("Spotify metadata available")

                    if 'youtube' in metadata:
                        st.success("YouTube metadata available")

            except Exception as e:

                st.error(f"Song not recognized\n\n{e}")
