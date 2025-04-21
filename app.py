# pip install streamlit openai-whisper ffmpeg-python

import streamlit as st
import whisper
import tempfile
import os

st.title("🎙️ Speech to Text Converter")

# Upload audio file
audio_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a"])

if audio_file is not None:
    st.audio(audio_file, format="audio/wav")

    with st.spinner("Transcribing..."):
        # Save uploaded file to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_audio:
            temp_audio.write(audio_file.read())
            temp_audio_path = temp_audio.name

        # Load Whisper model
        model = whisper.load_model("base")  # You can use "tiny", "base", "small", "medium", "large"

        # Transcribe audio
        result = model.transcribe(temp_audio_path)

        # Clean up
        os.remove(temp_audio_path)

        # Show the result
        st.subheader("📝 Transcription:")
        st.write(result["text"])

        # Download button
        st.download_button("Download Transcription", result["text"], file_name="transcription.txt")

