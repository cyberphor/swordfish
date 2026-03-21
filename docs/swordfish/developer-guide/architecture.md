# Architecture

Swordfish is composed of three components: a frontend, backend, and MCP server.

## Frontend

The frontend container serves the user-facing interface. It is the entry point for all user interaction — queries are composed here and results are rendered here. It communicates exclusively with the backend; it has no direct knowledge of the LLM or eMASS.

## Backend

The backend container is the core of the system. It receives requests from the frontend, manages sessions, and acts as the broker between the user and the external LLM. It is responsible for:

- Forwarding user queries to the configured LLM provider
- Passing LLM tool calls through to the MCP server
- Returning structured results back to the frontend

The backend does not query eMASS directly — all eMASS I/O is delegated to the MCP server.

## MCP Server

The MCP server exposes eMASS as a set of tools that the LLM can call. When the LLM determines that a user's request requires reading or writing data in eMASS, it issues a tool call which the backend routes to the MCP server. The MCP server translates that call into the appropriate eMASS API request, then returns the result back up the chain.

This design keeps eMASS credentials and API logic isolated in a single container and makes the tool surface independently testable.
