import streamlit as st
from spleeter.separator import Separator
import os
import tempfile
from pydub import AudioSegment

def convert_to_wav(input_audio_path):
    audio = AudioSegment.from_file(input_audio_path)
    wav_path = os.path.splitext(input_audio_path)[0] + "_converted.wav"
    audio.export(wav_path, format="wav")
    return wav_path

def separate_audio(input_audio_path):
    if not input_audio_path.endswith('.wav'):
        input_audio_path = convert_to_wav(input_audio_path)

    temp_dir = tempfile.mkdtemp()
    separator = Separator('spleeter:2stems')
    separator.separate_to_file(input_audio_path, temp_dir)

    output_folder = os.path.join(temp_dir, os.path.splitext(os.path.basename(input_audio_path))[0])
    vocals_path = os.path.join(output_folder, 'vocals.wav')
    accompaniment_path = os.path.join(output_folder, 'accompaniment.wav')

    return vocals_path, accompaniment_path

st.set_page_config(page_title="Audio Separator")
st.title("🎵 Audio Vocal & Instrument Splitter")

uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "m4a", "flac"])
if uploaded_file:
    with open(uploaded_file.name, "wb") as f:
        f.write(uploaded_file.read())

    with st.spinner("Separating..."):
        vocals, instr = separate_audio(uploaded_file.name)

    st.audio(vocals)
    st.download_button("Download Vocals", open(vocals, "rb"), "vocals.wav")

    st.audio(instr)
    st.download_button("Download Instrumental", open(instr, "rb"), "instrumental.wav")
