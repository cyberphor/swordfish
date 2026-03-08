# Standard-library imports.
from os import environ

# Third-party imports.
from fastapi import FastAPI, Request
from mcp.client.sse import sse_client
from strands import Agent
from strands.models.openai import OpenAIModel
from strands.tools.mcp import MCPClient

api = FastAPI()

# Connect to an MCP server using SSE transport.
sse_mcp_client = MCPClient(lambda: sse_client("http://swordfish-mcp-server:8282/sse"))

history = []

@api.post("/api/")
async def post(request: Request):
    global history
    request = await request.json()
    
    # Create an agent with MCP tools.
    with sse_mcp_client:

        model = OpenAIModel(
            client_args={
                "api_key": environ["OPENAI_API_KEY"],
            },
            model_id="gpt-4o",
            params={
                "max_tokens": 1000,
                "temperature": 0.7,
            },
        )

        # Get the tools from the MCP server
        tools = sse_mcp_client.list_tools_sync()
        print(tools)

        # Create an agent with these tools
        agent = Agent(model=model, tools=tools)

        # Inject the conversation history. 
        agent.messages = history

        response = agent(
            prompt=request["message"]
        )

        # Save the messages to conversation history. 
        history = agent.messages

        return response.message["content"][0]["text"]
