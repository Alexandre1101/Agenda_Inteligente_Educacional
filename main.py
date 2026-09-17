#arquivo central do projeto, vamos deixar o mvp.py de lado, ou para testes pontuais ... 
import streamlit as st
from audio.transcriber import transcriber
from ai.extractor import extractor
from ui.recording_ui import recording_page
from audio.recorder import save_audio




recording_page()