import streamlit as st
from audio_recorder_streamlit import audio_recorder
from acrcloud.recognizer import ACRCloudRecognizer
import tempfile
import json
import urllib.parse

# =========================
# ACRCloud Credentials
# =========================

host = "identify-ap-southeast-1.acrcloud.com"

access_key = "2c4514325ba5e950e2d927ddfa75523b"

access_secret = "i1kb8fjnv4xFe4x63YkXC0AGa6jFoJuODBWxmZSB"

# =========================
# ACRCloud Configuration
# =========================

config = {
    'host': host,
    'access_key': access_key,
    'access_secret': access_secret,
    'timeout': 10
}

recognizer = ACRCloudRecognizer(config)

# =========================
# Streamlit UI
# =========================

st.set_page_config(
    page_title="PragyanAI Song Recognizer",
    layout="centered"
)

st.title("🎵 PragyanAI Song Recognizer")

st.write(
    "Recognize songs by recording audio "
    "or uploading audio files"
)

# =========================
# Input Method
# =========================

option = st.radio(
    "Choose Audio Input Method",
    ["🎤 Record Audio", "📂 Upload Audio File"]
)

audio_data = None
file_extension = ".wav"

# =========================
# Record Audio
# =========================

if option == "🎤 Record Audio":

    audio_bytes = audio_recorder(
        text="Click to Record Song",
        recording_color="#ff0000",
        neutral_color="#6aa36f",
        icon_name="microphone",
        icon_size="2x",
    )

    if audio_bytes:

        st.audio(audio_bytes, format="audio/wav")

        audio_data = audio_bytes

        file_extension = ".wav"

# =========================
# Upload Audio File
# =========================

else:

    uploaded_file = st.file_uploader(
        "Upload Audio File",
        type=["mp3", "wav", "m4a"]
    )

    if uploaded_file is not None:

        audio_data = uploaded_file.read()

        file_extension = "." + uploaded_file.name.split(".")[-1]

        st.audio(audio_data)

# =========================
# Song Recognition
# =========================

if audio_data:

    if st.button("🎵 Recognize Song"):

        with st.spinner("Recognizing song..."):

            try:

                # Save temporary audio file
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=file_extension
                ) as f:

                    f.write(audio_data)

                    temp_audio = f.name

                # Recognize Song
                result = recognizer.recognize_by_file(
                    temp_audio,
                    0
                )

                # Convert response
                data = json.loads(result)

                # Debug API Response
                st.write("## API Response")
                st.write(data)

                # =========================
                # Check Recognition
                # =========================

                if (
                    'metadata' in data and
                    'music' in data['metadata']
                ):

                    music = data['metadata']['music'][0]

                    # =========================
                    # Song Details
                    # =========================

                    song_name = music.get(
                        'title',
                        'Unknown'
                    )

                    artist = music['artists'][0].get(
                        'name',
                        'Unknown'
                    )

                    album = music.get(
                        'album',
                        {}
                    ).get(
                        'name',
                        'Unknown'
                    )

                    release_date = music.get(
                        'release_date',
                        'Unknown'
                    )

                    # =========================
                    # Display Results
                    # =========================

                    st.success(
                        f"🎵 Song Name: {song_name}"
                    )

                    st.info(
                        f"🎤 Singer: {artist}"
                    )

                    st.info(
                        f"💿 Album: {album}"
                    )

                    st.info(
                        f"📅 Release Date: {release_date}"
                    )

                    # =========================
                    # Genres
                    # =========================

                    if 'genres' in music:

                        genres = [
                            g['name']
                            for g in music['genres']
                        ]

                        st.write(
                            "🎼 Genres:",
                            ", ".join(genres)
                        )

                    # =========================
                    # Album Artwork
                    # =========================

                    if 'external_metadata' in music:

                        metadata = music['external_metadata']

                        if 'spotify' in metadata:

                            spotify_data = metadata['spotify']

                            if 'album' in spotify_data:

                                album_data = spotify_data['album']

                                if 'images' in album_data:

                                    images = album_data['images']

                                    if len(images) > 0:

                                        image_url = images[0]['url']

                                        st.image(
                                            image_url,
                                            width=300
                                        )

                    # =========================
                    # YouTube Search
                    # =========================

                    search_query = (
                        f"{song_name} {artist}"
                    )

                    youtube_search_url = (
                        "https://www.youtube.com/results?search_query="
                        + urllib.parse.quote(search_query)
                    )

                    st.markdown("## ▶ Play on YouTube")

                    st.markdown(
                        f"""
                        <a href="{youtube_search_url}" target="_blank">
                            <button style="
                                background-color:red;
                                color:white;
                                border:none;
                                padding:10px 20px;
                                border-radius:10px;
                                font-size:18px;
                                cursor:pointer;
                            ">
                                ▶ Open on YouTube
                            </button>
                        </a>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.error(
                        "❌ Song could not be recognized"
                    )

                    st.warning(
                        "Try using clearer audio "
                        "or longer music clips."
                    )

            except Exception as e:

                st.error(f"Error:\n\n{e}")
