import json
from os import environ
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from mcp.client.sse import sse_client
from psycopg_pool import AsyncConnectionPool

from strands import Agent
from strands.models.openai import OpenAIModel
from strands.tools.mcp import MCPClient

from .history import HistoryStore, InMemoryStore


class PostgresStore(HistoryStore):
    def __init__(self, pool: AsyncConnectionPool):
        self.pool = pool

    async def get(self, session_id: str) -> list:
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT messages FROM chat_sessions WHERE session_id = %s", (session_id,))
                result = await cur.fetchone()
                return result[0] if result else []

    async def save(self, session_id: str, messages: list):
        async with self.pool.connection() as conn:
            async with conn.cursor() as cur:
                await cur.execute("""
                    INSERT INTO chat_sessions (session_id, messages)
                    VALUES (%s, %s)
                    ON CONFLICT (session_id) DO UPDATE SET messages = EXCLUDED.messages
                """, (session_id, json.dumps(messages)))

@asynccontextmanager
async def lifespan(app: FastAPI):
    store_type = environ.get("STORE_TYPE", "memory").lower()
    
    match store_type:
        case "postgres":
            db_url = environ["DATABASE_URL"]
            pool = AsyncConnectionPool(conninfo=db_url, open=False)
            await pool.open()
            app.state.history = PostgresStore(pool)
            yield
            await pool.close()
        case _:
            app.state.history = InMemoryStore()
            yield

api = FastAPI(lifespan=lifespan)
sse_mcp_client = MCPClient(lambda: sse_client("http://swordfish-tools:8282/sse"))

@api.post("/api/v1/")
async def respond(request: Request):
    store: HistoryStore = request.app.state.history
    
    body = await request.json()
    session_id = body.get("session_id", "default_session")
    user_message = body.get("message")

    current_history = await store.get(session_id)

    with sse_mcp_client:
        model = OpenAIModel(
            client_args={"api_key": environ["OPENAI_API_KEY"]},
            model_id=body.get("model", "gpt-4o"),
            params={"max_tokens": 1000, "temperature": 0.7},
        )

        tools = sse_mcp_client.list_tools_sync()

        agent = Agent(model=model, tools=tools)
        agent.messages = current_history
        response = agent(prompt=user_message)
        
        await store.save(session_id, agent.messages)
        
        return response.message["content"][0]["text"]
