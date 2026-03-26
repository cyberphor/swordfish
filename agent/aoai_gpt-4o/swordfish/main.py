from os import getenv
 
from agents import Agent, OpenAIChatCompletionsModel, Runner, set_tracing_disabled
from agents.mcp import MCPServerStreamableHttp
from azure.identity import (
    AzureAuthorityHosts,
    DefaultAzureCredential,
    get_bearer_token_provider,
)
from openai import AsyncAzureOpenAI
from fastapi import FastAPI, Request
 
AZURE_TOKEN_SCOPES = getenv("AZURE_TOKEN_SCOPES")
AZURE_OPENAI_ENDPOINT = getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_VERSION = getenv("AZURE_OPENAI_API_VERSION")
MCP_SERVER_ENDPOINT = getenv("MCP_SERVER_ENDPOINT")
AZURE_OPENAI_DEPLOYMENT = getenv("AZURE_OPENAI_DEPLOYMENT")
 
token_provider = get_bearer_token_provider(
    DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT),
    AZURE_TOKEN_SCOPES
)
 
client = AsyncAzureOpenAI(
    azure_endpoint=AZURE_OPENAI_ENDPOINT,
    api_version=AZURE_OPENAI_API_VERSION,
    azure_ad_token_provider=token_provider
)
set_tracing_disabled(disabled=True)
 
api = FastAPI()
history = []

@api.post("/api/v1/")
async def respond(request: Request):
    global history
    request = await request.json()
    async with MCPServerStreamableHttp(name="Swordfish Tools", params={"url": MCP_SERVER_ENDPOINT}, cache_tools_list=True) as mcp_server:
        model = OpenAIChatCompletionsModel(
            model=AZURE_OPENAI_DEPLOYMENT,
            openai_client=client,
        )
        agent = Agent(
            name="swordfish",
            model=model,
            mcp_servers=[mcp_server],
        )
        result = await Runner.run(starting_agent=agent, input=request["message"])
        return result.final_output
