#arquivo central do projeto, vamos deixar o mvp.py de lado, ou para testes pontuais ... 

import streamlit as st
from ui.recording_ui import recording_page
from ui.processing_ui import processing_page


st.set_page_config(
    page_title="MVP Professor",
    page_icon="🎓"
)


tab1, tab2 = st.tabs([
    "🎙️ Nova aula",
    "🤖 Processar aula"
])


with tab1:
    recording_page()


with tab2:
    processing_page()

