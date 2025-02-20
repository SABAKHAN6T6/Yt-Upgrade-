import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from textblob import TextBlob  # For sentiment analysis

API_KEY = "AIzaSyBrzgzfBoSm6vpamvNXqVh5wTbvae-CXqQ"
BASE_URL = "https://www.googleapis.com/youtube/v3/"

def main():
    st.title("🔍 YT Viral Prospector Pro")
    st.markdown("### Advanced YouTube Content Opportunity Finder")
    
    with st.sidebar:
        st.header("Settings")
        days_back = st.slider("Analysis Period (days)", 1, 30, 7)
        max_subs =
