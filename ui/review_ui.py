#arquivo para interface de revisão do professor 

import streamlit as st


def review_page():

    st.title("📚 Revisão da aula")

    audio_path = st.session_state.get("audio_path")

    if not audio_path:
        st.info("Nenhuma aula disponível para revisão.")
        return

    st.subheader("🎧 Áudio")

    with open(audio_path, "rb") as arquivo:
        audio_data = arquivo.read()

    st.audio(audio_data)

    st.divider()

    st.subheader("📝 Transcrição")

    texto = st.session_state.get("texto")

    if texto:
        st.text_area(
            "Texto transcrito",
            value=texto,
            height=300
        )
    else:
        st.info("A aula ainda não foi transcrita.")

    st.divider()

    st.subheader("🤖 Informações extraídas")

    aula = st.session_state.get("aula")

    if aula:
        st.write("**Matéria:**", aula.materia)
        st.write("**Assunto:**", aula.assunto)
    else:
        st.info("A aula ainda não foi processada.")
