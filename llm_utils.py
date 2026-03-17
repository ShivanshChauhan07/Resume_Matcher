from google import genai
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

def analyze_requirement_with_llm(prompt):
    api_key = st.secrets.get("GEMINI_API_KEY", os.getenv("GEMINI_API_KEY"))
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text