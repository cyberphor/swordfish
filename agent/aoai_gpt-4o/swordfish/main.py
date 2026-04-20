from os import getenv
from base64 import b64encode

from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from agents.mcp import MCPServerStreamableHttp
from azure.identity import (
    AzureAuthorityHosts,
    DefaultAzureCredential,
    get_bearer_token_provider,
)
from fastapi import FastAPI, File, Form, UploadFile
from openai import AsyncAzureOpenAI

AZURE_TOKEN_SCOPES = getenv("AZURE_TOKEN_SCOPES")
AZURE_OPENAI_ENDPOINT = getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = getenv("AZURE_OPENAI_API_VERSION")
MCP_SERVER_ENDPOINT = getenv("MCP_SERVER_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = getenv("AZURE_OPENAI_DEPLOYMENT")

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT),
    AZURE_TOKEN_SCOPES,
)

client = AsyncAzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_ad_token_provider=token_provider,
)

set_tracing_disabled(disabled=True)

api = FastAPI()


def build_mcp_server(
    user_uid: str,
    api_key: str,
    public_key_bytes: bytes,
    private_key_bytes: bytes,
) -> MCPServerStreamableHttp:
    return MCPServerStreamableHttp(
        name="Swordfish Tools",
        params={
            "url": MCP_SERVER_ENDPOINT,
            "timeout": 300,
            "headers": {
                "x-emass-user-uid": user_uid,
                "x-emass-api-key": api_key,
                "x-emass-public-cert": b64encode(public_key_bytes).decode("utf-8"),
                "x-emass-private-key": b64encode(private_key_bytes).decode("utf-8"),
            },
        },
        cache_tools_list=False,
    )


@api.post("/api/v1/")
async def respond(
    message: str = Form(...),
    session_id: str = Form(...),
    user_uid: str = Form(...),
    api_key: str = Form(...),
    public_key: UploadFile = File(...),
    private_key: UploadFile = File(...),
):
    public_key_bytes = await public_key.read()
    private_key_bytes = await private_key.read()

    model = OpenAIChatCompletionsModel(
        model=AZURE_OPENAI_DEPLOYMENT,
        openai_client=client,
    )

    mcp_server = build_mcp_server(
        user_uid=user_uid,
        api_key=api_key,
        public_key_bytes=public_key_bytes,
        private_key_bytes=private_key_bytes,
    )

    async with mcp_server:
        agent = Agent(
            name="swordfish",
            model=model,
            mcp_servers=[mcp_server],
        )
        result = await Runner.run(
            starting_agent=agent,
            input=message,
        )

    return result.final_output
