# Standard-library imports.
from os import environ

# Third-party imports.
from mcp.client.sse import sse_client
from strands import Agent
from strands.models.openai import OpenAIModel
from strands.tools.mcp import MCPClient


# Connect to an MCP server using SSE transport.
sse_mcp_client = MCPClient(lambda: sse_client("http://localhost:8282/sse"))

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

    # Create an agent with these tools
    agent = Agent(model=model, tools=tools)

    response = agent(
        prompt="Today is 2025-10-13. I was born today, but in 1990. How many days has it been since then?"
    )

    print(response)
