import streamlit as st
from app import interface_chat

st.set_page_config(
    page_title="JibóIA - Chat Geral",
    page_icon="🔮",
    layout="wide"
)

interface_chat()