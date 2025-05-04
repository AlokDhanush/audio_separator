import streamlit as st
from spleeter.separator import Separator
from pydub import AudioSegment
import os
import tempfile

def convert_to_wav(audio_path):
    audio = AudioSegment.from_file(audio_path)
    wav_path = os.path.splitext(audio_path)[0] + ".wav"
    audio.export(wav_path, format="wav")
    return wav_path

def separate_audio(audio_path):
    if not audio_path.endswith(".wav"):
        audio_path = convert_to_wav(audio_path)

    output_dir = tempfile.mkdtemp()
    separator = Separator('spleeter:2stems')  # Vocal + accompaniment
    separator.separate_to_file(audio_path, output_dir)
    
    basename = os.path.splitext(os.path.basename(audio_path))[0]
    vocals_path = os.path.join(output_dir, basename, "vocals.wav")
    accomp_path = os.path.join(output_dir, basename, "accompaniment.wav")
    
    return vocals_path, accomp_path

st.title("🎵 Audio Vocal & Instrument Separator")
uploaded = st.file_uploader("Upload an audio file", type=["mp3", "wav", "flac", "m4a"])

if uploaded:
    with open(uploaded.name, "wb") as f:
        f.write(uploaded.read())

    st.audio(uploaded.name)

    with st.spinner("Separating audio..."):
        vocals, instrumental = separate_audio(uploaded.name)

    st.success("Separation complete!")
    st.subheader("🎤 Vocals")
    st.audio(vocals)
    st.download_button("Download Vocals", open(vocals, "rb"), "vocals.wav")

    st.subheader("🎶 Instrumental")
    st.audio(instrumental)
    st.download_button("Download Instrumental", open(instrumental, "rb"), "instrumental.wav")
