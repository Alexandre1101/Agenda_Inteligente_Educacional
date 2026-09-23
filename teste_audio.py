import streamlit as st

st.title("🎙️ Teste de áudio")

audio = st.audio_input(
    "Gravar teste",
    sample_rate=16000,
    key="teste_microfone"
)

if audio is not None:
    st.success("Áudio recebido!")
    st.write(f"Tamanho: {audio.size / 1024:.1f} KB")
    st.audio(audio)
