import streamlit as st
import requests
import uuid

st.title("Swordfish")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

PROMPT_SUGGESTIONS = [
    "draft a poam entry for the latest finding",
    "summarize the risk posture of my oldest information system",
    "is this cyber tasking order applicable to any of my emass records?",
]

selected_prompt = None

if not st.session_state.messages:
    cols = st.columns(len(PROMPT_SUGGESTIONS))
    for col, chip in zip(cols, PROMPT_SUGGESTIONS):
        if col.button(chip, use_container_width=True):
            selected_prompt = chip

chat_input = st.chat_input("Ask Swordfish...")
prompt = chat_input or selected_prompt

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    response = requests.post(
        "http://swordfish-agent:8181/api/v1/",
        json={
            "message": prompt,
            "session_id": st.session_state.session_id
        },
        timeout=60,
    )

    response.raise_for_status()
    text = response.json()

    st.session_state.messages.append({"role": "assistant", "content": text})

    with st.chat_message("assistant"):
        st.markdown(text)
    
    if selected_prompt:
        st.rerun()
