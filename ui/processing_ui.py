# tela de processamento do áudio 

import streamlit as st

from services.lesson_service import process_lesson


def processing_page():

    st.header("🤖 Processar aula")

    audio_path = st.session_state.get("audio_path")

    if not audio_path:
        st.info(
            "Nenhuma gravação disponível."
        )
        return

    st.success(
        f"Gravação disponível: `{audio_path}`"
    )

    if st.button(
        "🎙️ Transcrever áudio",
        type="primary"
    ):

        with st.spinner(
            "Transcrevendo áudio..."
        ):

            texto = process_lesson(
                audio_path
            )

        st.session_state.texto = texto

        st.success(
            "Transcrição concluída!"
        )

    texto = st.session_state.get("texto")

    if texto:

        st.subheader("📝 Transcrição")

        st.text_area(
            "Texto transcrito",
            value=texto,
            height=400
        )
