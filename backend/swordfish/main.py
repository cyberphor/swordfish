# Standard library imports.
from os import getenv
from base64 import b64encode

# Third party imports.
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from agents.mcp import MCPServerStreamableHttp
from azure.identity import (
    AzureAuthorityHosts,
    DefaultAzureCredential,
    get_bearer_token_provider,
)
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from jwt import decode
from openai import AsyncAzureOpenAI

# Local imports.
from swordfish.memory.short_term import (
    create_chat_history_table,
    get_chat_history,
    save_chat_history,
)
from swordfish.profile.emu import (
    create_emu_config_profile_handler,
    create_emu_config_profile_table,
    get_emu_config_profiles_by_user,
)
from swordfish.profile.users import (
    create_user_table,
    get_or_create_user_handler,
)

# Get environment variables.
AZURE_OPENAI_API_VERSION = getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_ENDPOINT = getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = getenv("AZURE_OPENAI_DEPLOYMENT")
AZURE_TOKEN_SCOPES = getenv("AZURE_TOKEN_SCOPES")
MCP_SERVER_ENDPOINT = getenv("MCP_SERVER_ENDPOINT")

# Get an authorization token provider.
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT),
    AZURE_TOKEN_SCOPES,
)

# Authenticate with the Azure OpenAI service.
openai_client = AsyncAzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_ad_token_provider=token_provider,
)

# Disable tracing (i.e., text generation, tool call, handoff, and guardrail logs).
set_tracing_disabled(disabled=True)

# Init a FastAPI server.
api = FastAPI()

# Init databases.
create_user_table()
create_emu_config_profile_table()
create_chat_history_table()


def get_swordfish_mcp_server_connection(
    user_uid: str,
    api_key: str,
    public_key_bytes: bytes,
    private_key_bytes: bytes,
) -> MCPServerStreamableHttp:
    """Connect to the Swordfish MCP server."""
    return MCPServerStreamableHttp(
        name="Swordfish MCP Server",
        client_session_timeout_seconds=120,
        params={
            "url": MCP_SERVER_ENDPOINT,
            "headers": {
                "x-emass-user-uid": user_uid,
                "x-emass-api-key": api_key,
                "x-emass-public-cert": b64encode(public_key_bytes).decode("utf-8"),
                "x-emass-private-key": b64encode(private_key_bytes).decode("utf-8"),
            },
        },
        cache_tools_list=False,
    )


@api.get("/api/v1/users")
async def get_user_endpoint(request: Request):
    """Get or create a user based on the Authorization header of a given request."""

    # Get authorization header.
    authorization_header = request.headers.get("Authorization")
    if authorization_header is None:
        raise HTTPException(status_code=403, detail="Authorization header missing")

    # Get bearer token from authorization header.
    if not authorization_header.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Bearer token missing")
    bearer_token = authorization_header[7:]

    # Parse the claims in the bearer token.
    claims = decode(
        bearer_token, algorithms=["RS256"], options={"verify_signature": False}
    )

    # Get or create the user and then, return metadata about them.
    return get_or_create_user_handler(
        user_id=claims["x509"]["usercertificateIdentity"],
        last_name=claims["family_name"],
        first_name=claims["given_name"],
        email_address=claims["email"],
        user_name=claims["preferred_username"],
    )


@api.get("/api/v1/emu-config-profile")
async def get_emu_config_profile_endpoint(request: Request):
    """Get all EMU config profiles for the authenticated user."""

    # Get authorization header.
    authorization_header = request.headers.get("Authorization")
    if authorization_header is None:
        raise HTTPException(status_code=403, detail="Authorization header missing")

    # Get bearer token from authorization header.
    if not authorization_header.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Bearer token missing")
    bearer_token = authorization_header[7:]

    # Parse the claims in the bearer token.
    claims = decode(
        bearer_token, algorithms=["RS256"], options={"verify_signature": False}
    )

    # Get and return the user's EMU config profiles.
    return get_emu_config_profiles_by_user(
        user_id=claims["x509"]["usercertificateIdentity"],
    )


@api.post("/api/v1/emu-config-profile")
async def post_emu_config_profile_endpoint(
    request: Request,
    name: str = Form(...),
    user_uid: str = Form(...),
    public_key: UploadFile = File(...),
    private_key: UploadFile = File(...),
):
    """Create an EMU config profile."""

    # Get authorization header.
    authorization_header = request.headers.get("Authorization")
    if authorization_header is None:
        raise HTTPException(status_code=403, detail="Authorization header missing")

    # Get bearer token from authorization header.
    if not authorization_header.startswith("Bearer "):
        raise HTTPException(status_code=403, detail="Bearer token missing")
    bearer_token = authorization_header[7:]

    # Get the API key from the request header.
    api_key = request.headers.get("x-emass-api-key")
    if api_key is None:
        raise HTTPException(status_code=400, detail="x-emass-api-key header missing")

    # Parse the claims in the bearer token.
    claims = decode(
        bearer_token, algorithms=["RS256"], options={"verify_signature": False}
    )

    # Convert the public and private keys to bytes.
    public_key_bytes = await public_key.read()
    private_key_bytes = await private_key.read()

    # Create an EMU config profile.
    return create_emu_config_profile_handler(
        name=name,
        user_id=claims["x509"]["usercertificateIdentity"],
        user_uid=user_uid,
        api_key=api_key,
        public_key_name=public_key.filename,
        public_key=public_key_bytes,
        private_key_name=private_key.filename,
        private_key=private_key_bytes,
    )


@api.post("/api/v1/agent")
async def respond(
    session_id: str = Form(...),
    message: str = Form(...),
    user_uid: str = Form(...),
    api_key: str = Form(...),
    public_key: UploadFile = File(...),
    private_key: UploadFile = File(...),
):
    """Respond to a Swordfish requests."""

    # Convert the user's NPE certificates to bytes.
    public_key_bytes = await public_key.read()
    private_key_bytes = await private_key.read()

    # Connect to the Swordfish MCP server.
    swordfish_mcp_server_connection = get_swordfish_mcp_server_connection(
        user_uid=user_uid,
        api_key=api_key,
        public_key_bytes=public_key_bytes,
        private_key_bytes=private_key_bytes,
    )

    # Init a LLM.
    model = OpenAIChatCompletionsModel(
        model=AZURE_OPENAI_DEPLOYMENT,
        openai_client=openai_client,
    )

    # Process the user's request.
    async with swordfish_mcp_server_connection:
        # Create an agent.
        agent = Agent(
            name="swordfish",
            model=model,
            mcp_servers=[swordfish_mcp_server_connection],
        )

        # Run the agent.
        chat_history = get_chat_history(session_id=session_id)
        chat_history.append({"role": "user", "content": message})
        response = await Runner.run(
            starting_agent=agent,
            input=chat_history,
        )

        save_chat_history(
            session_id=session_id, query=message, response=response.final_output
        )
        return response.final_output
