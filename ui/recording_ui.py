#arquivo para interface de gravação de áudio

import streamlit as st

from audio.recorder import save_audio
from services.lesson_service import process_lesson


def recording_page():

    st.title("🎙️ Nova aula")

    # -----------------------------
    # Estado inicial
    # -----------------------------

    if "audio_path" not in st.session_state:
        st.session_state.audio_path = None

    if "recording_confirmed" not in st.session_state:
        st.session_state.recording_confirmed = False

    if "texto" not in st.session_state:
        st.session_state.texto = None

    if "aula" not in st.session_state:
        st.session_state.aula = None

    # -----------------------------
    # Captura do áudio
    # -----------------------------

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
                "✅ Confirmar e processar",
                type="primary"
            )

        with col2:

            cancelar = st.button(
                "❌ Descartar"
            )

        # -----------------------------
        # Confirmar
        # -----------------------------

        if confirmar:

            with st.spinner(
                "Salvando, transcrevendo e extraindo..."
            ):

                # 1. Salvar áudio

                audio_path = save_audio(
                    audio.getvalue()
                )

                st.session_state.audio_path = str(
                    audio_path
                )

                st.session_state.recording_confirmed = True

                # 2. Transcrever + extrair

                texto, aula = process_lesson(
                    audio_path
                )

                # 3. Guardar no estado

                st.session_state.texto = texto
                st.session_state.aula = aula

            st.success(
                "Aula processada com sucesso!"
            )

        # -----------------------------
        # Cancelar
        # -----------------------------

        if cancelar:

            st.session_state.audio_path = None
            st.session_state.recording_confirmed = False
            st.session_state.texto = None
            st.session_state.aula = None

            st.rerun()

    # -----------------------------
    # Resultado
    # -----------------------------

    if st.session_state.recording_confirmed:

        st.divider()

        st.success(
            f"Áudio salvo em: "
            f"{st.session_state.audio_path}"
        )

        if st.session_state.texto:

            st.subheader("📝 Transcrição")

            st.text_area(
                "Texto",
                st.session_state.texto,
                height=300
            )

        if st.session_state.aula:

            st.subheader("🤖 Dados extraídos")

            st.write(
                "Matéria:",
                st.session_state.aula.materia
            )

            st.write(
                "Assunto:",
                st.session_state.aula.assunto
            )
