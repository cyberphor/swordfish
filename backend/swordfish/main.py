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
from fastapi import FastAPI, File, Form, Request, UploadFile
from openai import AsyncAzureOpenAI

# Local imports.
from swordfish.memory.short_term import (
    create_chat_history_table,
    get_chat_history,
    save_chat_history,
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

create_chat_history_table()


# Connects to the Swordfish MCP server.
def get_swordfish_mcp_server_connection(
    user_uid: str,
    api_key: str,
    public_key_bytes: bytes,
    private_key_bytes: bytes,
) -> MCPServerStreamableHttp:
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


# Responds to Swordfish agent requests.
@api.get("/api/v1/users")
async def get_users(request: Request):
    return request.headers.get("Authorization")


# Responds to Swordfish agent requests.
@api.post("/api/v1/agent")
async def respond(
    session_id: str = Form(...),
    message: str = Form(...),
    user_uid: str = Form(...),
    api_key: str = Form(...),
    public_key: UploadFile = File(...),
    private_key: UploadFile = File(...),
):
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
