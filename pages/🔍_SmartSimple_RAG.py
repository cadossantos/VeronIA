from dotenv import load_dotenv
load_dotenv()
import streamlit as st
from smartwiki.agents.app import main as smartwiki_main

if __name__ == '__main__':
    smartwiki_main()
