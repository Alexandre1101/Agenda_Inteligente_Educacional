#arquivo para interface de gravação de áudio

import streamlit as st
from pathlib import Path

from audio.recorder import save_audio


def recording_page():

    st.title("🎙️ Nova aula")

    audio = st.audio_input("Gravar aula")

    if audio is None:
        return

    st.subheader("Prévia da gravação")
    st.audio(audio)

    st.write(f"Tamanho do arquivo: {audio.size / 1024:.1f} KB")

    col1, col2 = st.columns(2)

    with col1:
        confirmar = st.button(
            "✅ Confirmar gravação",
            type="primary"
        )

    with col2:
        cancelar = st.button("❌ Descartar")

    if confirmar:

        audio_path = save_audio(
            audio.getvalue(),
            "data/audio/aula.wav"
        )

        st.success(f"Gravação salva: {audio_path}")

    if cancelar:
        st.info("Gravação descartada.")
