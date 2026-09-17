#arquivo para interface de revisão do professor 

import streamlit as st


def review_page(texto, aula, audio_path):

    st.title("📚 Revisão da aula")

    st.subheader("🎧 Áudio")

    with open(audio_path, "rb") as arquivo:
        audio_data = arquivo.read()

    st.audio(audio_data)

    st.divider()

    st.subheader("📝 Transcrição")

    st.text_area(
        "Texto transcrito",
        value=texto,
        height=300
    )

    st.divider()

    st.subheader("🤖 Informações extraídas")

    st.write("**Matéria:**", aula.materia or "Não identificada")
    st.write("**Assunto:**", aula.assunto or "Não identificado")

    st.divider()

    st.subheader("📝 Provas")

    if aula.provas:
        for prova in aula.provas:
            st.write(
                f"- {prova.materia or 'Matéria não informada'} "
                f"— {prova.data or 'Data não informada'}"
            )
    else:
        st.write("Nenhuma prova mencionada.")

    st.subheader("❓ Dúvidas")

    if aula.duvidas:
        for duvida in aula.duvidas:
            aluno = duvida.aluno or "Aluno não identificado"

            st.write(
                f"**{aluno}:** {duvida.descricao}"
            )
    else:
        st.write("Nenhuma dúvida mencionada.")

    st.subheader("⚠️ Advertências")

    if aula.advertencias:
        for advertencia in aula.advertencias:
            aluno = advertencia.aluno or "Aluno não identificado"

            st.write(
                f"**{aluno}:** {advertencia.motivo}"
            )
    else:
        st.write("Nenhuma advertência mencionada.")
