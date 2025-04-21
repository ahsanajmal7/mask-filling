# pip install streamlit whisper pydub ffmpeg-python

import streamlit as st
from whisper import load_model
import ffmpeg
import tempfile
import os

# Load Whisper model
model = load_model("base")

# Title for the Streamlit app
st.title("🎤 Speech to Text")

# Upload audio file
uploaded_audio = st.file_uploader("Upload an audio file", type=["mp3", "m4a", "wav", "flac"])

def convert_audio(input_path, output_path):
    """
    Converts audio files to wav format using ffmpeg-python.
    """
    ffmpeg.input(input_path).output(output_path).run()
    return output_path

# When the user uploads a file
if uploaded_audio is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_audio_file:
        # Save uploaded file to temporary location
        tmp_audio_file.write(uploaded_audio.read())
        temp_path = tmp_audio_file.name

        # Convert the audio file to .wav if it's not already in .wav format
        if not temp_path.endswith(".wav"):
            wav_path = temp_path.replace(os.path.splitext(temp_path)[1], ".wav")
            convert_audio(temp_path, wav_path)
            audio_path = wav_path
        else:
            audio_path = temp_path

        # Transcribe the audio to text using Whisper
        result = model.transcribe(audio_path)
        
        # Display the transcribed text
        st.subheader("Transcribed Text:")
        st.write(result["text"])

        # Optionally, clean up the temporary files after use
        os.remove(temp_path)
        if audio_path != temp_path:
            os.remove(audio_path)
