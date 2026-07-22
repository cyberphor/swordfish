# Standard library imports.
from os import environ
from requests import get, post
from pathlib import Path
from urllib.parse import quote
from uuid import uuid4

# Third party imports.
import streamlit as st


# Define a Profile class.
class Profile:
    def __init__(self, name, user_uid, api_key, public_key, private_key):
        self.name = name
        self.user_uid = user_uid
        self.api_key = api_key
        self.public_key_name = public_key.name
        self.public_key_bytes = public_key.getvalue()
        self.private_key_name = private_key.name
        self.private_key_bytes = private_key.getvalue()


# Set environment variables.
BACKEND_ENDPOINT = environ["BACKEND_ENDPOINT"]
BACKEND_ENDPOINT = environ["BACKEND_ENDPOINT"]

# Set constants.
PROMPT_SUGGESTIONS = [
    "test connectivity to eMASS",
    "get data about a system",
    "is this cyber tasking order applicable to any of my emass records?",
]


def get_token_from_headers() -> str | None:
    """Extract the bearer token from the current Authorization header in context."""
    headers = st.context.headers
    authorization_header = headers.get("Authorization")
    if authorization_header and authorization_header.startswith("Bearer "):
        return authorization_header[len("Bearer ") :].strip()
    return None


def get_or_create_user() -> dict | None:
    """Get or create a user based on the current Authorization header in context."""
    bearer_token = get_token_from_headers()
    if bearer_token:
        headers = {"Authorization": f"Bearer {bearer_token}"}
        response = get(
            url=f"{BACKEND_ENDPOINT}/users",
            headers=headers,
        )
        response.raise_for_status()
        return response.json()
    print("Authorization header is missing")
    return None


def get_emu_config_profiles() -> list:
    """Get all the EMU config profiles using the current Authorization header in context."""
    bearer_token = get_token_from_headers()
    response = get(
        url=f"{BACKEND_ENDPOINT}/emu-config-profile",
        headers={"Authorization": f"Bearer {bearer_token}"},
    )
    # TODO: Implement a way to test auth without needing Keycloak.
    try:
        response.raise_for_status()
        return response.json()
    except:
        return ""


def create_emu_config_profile(profile: dict) -> any:
    """Create an EMU config profile."""
    bearer_token = get_token_from_headers()
    response = post(
        url=f"{BACKEND_ENDPOINT}/emu-config-profile",
        headers={
            "Authorization": f"Bearer {bearer_token}",
            "x-emass-api-key": profile["api_key"],
        },
        data={
            "name": profile["name"],
            "user_uid": profile["user_uid"],
        },
        files={
            "public_key": (
                profile["public_key_name"],
                profile["public_key_bytes"],
                "application/x-pem-file",
            ),
            "private_key": (
                profile["private_key_name"],
                profile["private_key_bytes"],
                "application/x-pem-file",
            ),
        },
    )
    response.raise_for_status()
    return response.json()


# Set session ID.
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid4())

# Set user.
if "user" not in st.session_state:
    st.session_state.user = get_or_create_user()
user = st.session_state.user

# Set profiles.
if "profiles" not in st.session_state:
    st.session_state.profiles = get_emu_config_profiles()
profiles = st.session_state.profiles

# Set selected profile.
if "selected_profile_name" not in st.session_state:
    st.session_state.selected_profile_name = None

# Set messages.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Set page metadata.
st.set_page_config(page_title="Swordfish")
if user:
    username = user[2]
else:
    username = "world"
st.title(f"Hello {username}!")

# Set the logo.
svg_content = (Path(__file__).parent / "logo.svg").read_text()
svg_encoded = quote(svg_content)
st.markdown(
    f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/svg+xml,{svg_encoded}");
        background-repeat: no-repeat;
        background-position: bottom 140px right 20px;
        background-size: 180px;
        background-attachment: fixed;
    }}
    </style>
""",
    unsafe_allow_html=True,
)

# Create a sidebar.
with st.sidebar:
    with st.form("profile_form", clear_on_submit=True):
        st.header("Configuration Profile")
        name = st.text_input("Profile Name")
        user_uid = st.text_input("User UID", type="password")
        api_key = st.text_input("API Key", type="password")
        public_key = st.file_uploader("Public Key", type=["cer", "crt", "pem"])
        private_key = st.file_uploader("Private Key", type=["key", "pem", "txt"])
        submitted = st.form_submit_button("Create")
        if submitted:
            if (
                not name
                or not user_uid
                or not api_key
                or not public_key
                or not private_key
            ):
                st.error("All fields are required.")
            elif any(profile["name"] == name for profile in profiles):
                st.error("Profile name already exists.")
            else:
                profile = {
                    "name": name,
                    "user_uid": user_uid,
                    "api_key": api_key,
                    "public_key_name": public_key.name,
                    "public_key_bytes": public_key.getvalue(),
                    "private_key_name": private_key.name,
                    "private_key_bytes": private_key.getvalue(),
                }
                try:
                    create_emu_config_profile(profile)
                    profiles.append(profile)
                    st.session_state.selected_profile_name = name
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to save profile: {e}")

    profile_names = [profile["name"] for profile in profiles]
    if profile_names:
        current_index = 0
        if st.session_state.selected_profile_name in profile_names:
            current_index = profile_names.index(st.session_state.selected_profile_name)
        st.session_state.selected_profile_name = st.radio(
            "Choose profile",
            options=profile_names,
            index=current_index,
        )

    for index, profile in enumerate(profiles):
        with st.expander(profile["name"]):
            st.write(f"User UID: {profile['user_uid']}")
            st.write(f"API Key: {'*' * len(profile['api_key'])}")
            st.write(f"Public Key: {profile['public_key_name']}")
            st.write(f"Private Key: {profile['private_key_name']}")
            if st.button("Delete", key=f"delete_{index}"):
                deleted_name = profile["name"]
                profiles.pop(index)
                if st.session_state.selected_profile_name == deleted_name:
                    st.session_state.selected_profile_name = (
                        profiles[0]["name"] if profiles else None
                    )
                st.rerun()

selected_profile = next(
    (
        profile
        for profile in profiles
        if profile["name"] == st.session_state.selected_profile_name
    ),
    None,
)

if selected_profile:
    st.caption(f"Using profile: {selected_profile['name']}")
else:
    st.caption("No profile selected")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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

    if not selected_profile:
        text = "No profile selected."
    else:
        response = post(
            f"{BACKEND_ENDPOINT}/agent",
            data={
                "message": prompt,
                "session_id": st.session_state.session_id,
                "user_uid": selected_profile["user_uid"],
                "api_key": selected_profile["api_key"],
            },
            files={
                "public_key": (
                    selected_profile["public_key_name"],
                    selected_profile["public_key_bytes"],
                    "application/x-pem-file",
                ),
                "private_key": (
                    selected_profile["private_key_name"],
                    selected_profile["private_key_bytes"],
                    "application/x-pem-file",
                ),
            },
            timeout=120,
        )
        response.raise_for_status()
        text = response.json()

    st.session_state.messages.append({"role": "assistant", "content": text})

    with st.chat_message("assistant"):
        st.markdown(text)

    if selected_prompt:
        st.rerun()
