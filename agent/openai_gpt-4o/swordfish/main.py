# Standard-library imports.
from os import environ

# Third-party imports.
from fastapi import FastAPI, Request
from mcp.client.sse import sse_client
from strands import Agent
from strands.models.openai import OpenAIModel
from strands.tools.mcp import MCPClient

api = FastAPI()
sse_mcp_client = MCPClient(lambda: sse_client("http://swordfish-tools:8282/sse"))
history = []

@api.post("/api/v1/")
async def respond(request: Request):
    global history
    request = await request.json()
    with sse_mcp_client:
        model = OpenAIModel(
            client_args={
                "api_key": environ["OPENAI_API_KEY"],
            },
            model_id=request.get("model", "gpt-4o"),
            params={
                "max_tokens": 1000,
                "temperature": 0.7,
            },
        )

        tools = sse_mcp_client.list_tools_sync()
        agent = Agent(model=model, tools=tools)
        agent.messages = history
        response = agent(prompt=request["message"])
        history = agent.messages
        return response.message["content"][0]["text"]
