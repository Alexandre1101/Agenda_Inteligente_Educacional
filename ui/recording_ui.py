#arquivo para interface de gravação de áudio

import streamlit as st
from audio.recorder import save_audio


def recording_page():

    st.header("🎙️ Nova aula")

    audio = st.audio_input(
        "Gravar aula",
        sample_rate=16000,
        key="gravacao_aula"
    )

    if audio is not None:

        st.subheader("Prévia da gravação")

        st.audio(audio)

        st.write(
            f"Tamanho: {audio.size / 1024:.1f} KB"
        )

        if st.button(
            "✅ Salvar gravação",
            type="primary"
        ):

            audio_path = save_audio(
                audio.getvalue()
            )

            st.session_state.audio_path = str(
                audio_path
            )

            st.success(
                "Gravação salva com sucesso!"
            )

            st.write(
                f"Arquivo: `{audio_path}`"
            )
