# tela de processamento do áudio 

import streamlit as st

from audio.transcriber import transcriber
from ai.extractor import extractor


def process_lesson(audio_path):

    texto = transcriber(audio_path)

    aula = extractor(texto)

    return texto, aula


def processing_page():

    st.header("⚙️ Processamento")

    audio_path = st.session_state.get("audio_path")

    if not audio_path:
        st.info("Nenhuma gravação disponível.")
        return

    st.write(f"Arquivo: `{audio_path}`")

    if st.button("🤖 Processar aula", type="primary"):

        with st.spinner("Processando aula..."):

            texto, aula = process_lesson(audio_path)

        st.session_state.texto = texto
        st.session_state.aula = aula

        st.success("Aula processada com sucesso!")