#arquivo central do projeto, vamos deixar o mvp.py de lado, ou para testes pontuais ... 
import streamlit as st

from ui.recording_ui import recording_page
from ui.review_ui import review_page



st.set_page_config(
    page_title="MVP Professor",
    page_icon="🎓"
)

recording_page()
