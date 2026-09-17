#arquivo para interface de gravação de áudio

import streamlit as st
from pathlib import Path


def recording_page():
    st.title("Gravar aula")

    audio = st.audio_input("Clique para gravar")

    if audio is not None:
        st.audio(audio)

        audio_dir = Path("data/audio")
        audio_dir.mkdir(parents=True, exist_ok=True)

        audio_path = audio_dir / "aula.wav"

        with open(audio_path, "wb") as arquivo:
            arquivo.write(audio.getvalue())

        st.success(f"Áudio salvo em: {audio_path}")
