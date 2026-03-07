# streamlit_app.py
import streamlit as st
import requests

st.title("Swordfish")
API = st.text_input("API base", "http://localhost:8181")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Say something"):
    st.session_state.messages.append({"role": "user", "content": prompt})


    with st.chat_message("user"): 
        st.markdown(prompt)

    response = requests.post(f"{API}/api", json={"message": prompt}, timeout=60)
    response.raise_for_status()
    text = response.json()["choices"][0]["text"]

    st.session_state.messages.append({"role": "assistant", "content": text})


    with st.chat_message("assistant"): 
        st.markdown(text)
