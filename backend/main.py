# backend/main.py

import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import mcp_server_tools
from autogen_ext.tools.mcp import SseServerParams


async def main():
    server_params = SseServerParams(url="http://mcp-server:8000/sse")
    tools = await mcp_server_tools(server_params)

    model_client = OpenAIChatCompletionClient(
        model="gemma-3-1b-pt-q4_0",
        api_key="none",
        base_url="http://llama-server:8080",
        model_capabilities={
            "json_output": False,
            "vision": False, 
            "function_calling": True
        },
    )

    agent = AssistantAgent(
        name="skynet",
        model_client=model_client,
        tools=tools,
        reflect_on_tool_use=True,
        system_message=(
            "You are an intelligent assistant. Be as succinct as possible when answering my questions. Just return the answer, nothing else."
        ),
    )

    await Console(
        agent.run_stream(
            task="what is 100 plus 100?", cancellation_token=CancellationToken()
        )
    )

if __name__ == "__main__":
    asyncio.run(main())
