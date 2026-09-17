#arquivo para interface de revisão do professor 

import streamlit as st
from audio.recorder import save_audio


def recording_page():

    st.title("🎙️ Nova aula")

    # Estado inicial
    if "audio_path" not in st.session_state:
        st.session_state.audio_path = None

    if "recording_confirmed" not in st.session_state:
        st.session_state.recording_confirmed = False

    # Captura do áudio
    audio = st.audio_input("Gravar aula")

    if audio is not None:

        st.subheader("Prévia da gravação")

        st.audio(audio)

        st.write(
            f"Tamanho: {audio.size / 1024:.1f} KB"
        )

        col1, col2 = st.columns(2)

        with col1:

            confirmar = st.button(
                "✅ Confirmar gravação",
                type="primary"
            )

        with col2:

            cancelar = st.button(
                "❌ Descartar"
            )

        # Confirmar
        if confirmar:

            audio_path = save_audio(
                audio.getvalue()
            )

            st.session_state.audio_path = str(audio_path)
            st.session_state.recording_confirmed = True

            st.success("Gravação salva com sucesso!")

        # Cancelar
        if cancelar:

            st.session_state.audio_path = None
            st.session_state.recording_confirmed = False

            st.rerun()

    # Mostrar estado depois da confirmação
    if st.session_state.recording_confirmed:

        st.divider()

        st.success(
            f"Áudio salvo em: "
            f"{st.session_state.audio_path}"
        )

        st.info(
            "A gravação está pronta para ser processada."
        )
