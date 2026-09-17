#arquivo central do projeto, vamos deixar o mvp.py de lado, ou para testes pontuais ... 
import streamlit as st
from audio.transcriber import transcriber
from ai.extractor import extractor
from ui.recording_ui import recording_page
from audio.recorder import save_audio
from ui.review_ui import review_page



st.set_page_config(
    page_title="MVP Professor",
    page_icon="🎓"
)


pagina = st.sidebar.radio(
    "Navegação",
    [
        "🎙️ Gravar aula",
        "📚 Revisar aula"
    ]
)


if pagina == "🎙️ Gravar aula":
    recording_page()

elif pagina == "📚 Revisar aula":
    review_page()