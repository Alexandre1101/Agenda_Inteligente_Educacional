#arquivo central do projeto, vamos deixar o mvp.py de lado, ou para testes pontuais ... 

import streamlit as st
from ui.recording_ui import recording_page
from ui.processing_ui import processing_page


st.set_page_config(
    page_title="MVP Professor",
    page_icon="🎓"
)


st.title("🎓 AI Educacional")

recording_page()

st.divider()

processing_page()
