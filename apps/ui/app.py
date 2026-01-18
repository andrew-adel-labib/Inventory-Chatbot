import os
import streamlit as st
import requests

API_URL = os.getenv("API_URL", "http://localhost:8000/api/chat")

st.title("📦 Inventory Analytics Chatbot")

role = st.selectbox("Role", ["viewer", "finance", "admin"])
question = st.text_area("Ask a question")

if st.button("Submit"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        payload = {
            "session_id": "streamlit",
            "message": question,
            "context": {"role": role}
        }

        try:
            res = requests.post(API_URL, json=payload, timeout=10)
            if res.status_code != 200:
                st.error(f"API error ({res.status_code}): {res.text}")
            else:
                st.json(res.json())
        except requests.RequestException as e:
            st.error(f"Failed to connect to API: {e}")