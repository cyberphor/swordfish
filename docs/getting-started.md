# Getting Started

This guide walks you through running swordfish locally. You will need Docker, an eMASS API key, and credentials for a supported LLM provider.

## Prerequisites

- Docker and Docker Compose
- An eMASS API key and base URL
- An API key for your LLM provider (OpenAI, Anthropic, etc.)

## Installation

Clone the repository:

```
git clone https://github.com/deathlabs/swordfish
cd swordfish
```

Copy the example environment file and fill in your credentials:

```
cp .env.example .env
```

## Configuration

Open `.env` and set the following values:

```
# LLM provider
LLM_PROVIDER=anthropic
LLM_API_KEY=your-api-key-here
LLM_MODEL=claude-sonnet-4-6

# eMASS
EMASS_BASE_URL=https://your-emass-instance/api
EMASS_API_KEY=your-emass-api-key
EMASS_USER_UID=your-user-uid
```

`LLM_PROVIDER` controls which external LLM the backend connects to. Supported values are `anthropic` and `openai`.

## Running

Start all three containers with:

```
docker compose up
```

The frontend will be available at `http://localhost:3000`. The backend runs on port `8000` and the MCP server on port `8001` — both are internal to the compose network and not exposed directly in production.

## Verify the setup

Once the containers are up, open the frontend and try a simple query:

```
show me all open POA&Ms
```

If swordfish returns results, your eMASS connection is working. If you see a tool call error, double-check your `EMASS_BASE_URL` and `EMASS_API_KEY` values in `.env`.

## Stopping

```
docker compose down
```

To also remove volumes:

```
docker compose down -v
```

## Next steps

- Read the [Architecture](architecture.md) doc to understand how the containers interact
- See the [Configuration](configuration.md) reference for all available environment variables
- Check [Contributing](contributing.md) if you want to add a new eMASS tool
