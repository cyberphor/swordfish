# Architecture

Swordfish is composed of three containers that work together to provide a natural language interface over eMASS.

## Components

### Frontend

The frontend container serves the user-facing interface. It is the entry point for all user interaction — queries are composed here and results are rendered here. It communicates exclusively with the backend; it has no direct knowledge of the LLM or eMASS.

### Backend

The backend container is the core of the system. It receives requests from the frontend, manages sessions, and acts as the broker between the user and the external LLM. It is responsible for:

- Forwarding user queries to the configured LLM provider
- Passing LLM tool calls through to the MCP server
- Returning structured results back to the frontend

The backend does not query eMASS directly — all eMASS I/O is delegated to the MCP server.

### MCP Server

The MCP server exposes eMASS as a set of tools that the LLM can call. When the LLM determines that a user's request requires reading or writing data in eMASS, it issues a tool call which the backend routes to the MCP server. The MCP server translates that call into the appropriate eMASS API request, then returns the result back up the chain.

This design keeps eMASS credentials and API logic isolated in a single container and makes the tool surface independently testable.

## Data Flow

A typical request follows this path:

1. The user types a question in the frontend
2. The frontend sends it to the backend
3. The backend forwards it to the external LLM with the available MCP tools in context
4. The LLM responds — either with a direct answer, or with one or more tool calls
5. Tool calls are routed to the MCP server, which reads from or writes to eMASS
6. Results are returned to the LLM to complete its response
7. The final answer is passed back through the backend to the frontend

## Design Principles

**Separation of concerns.** Each container has a single, well-defined responsibility. The frontend knows about the user. The backend knows about the LLM. The MCP server knows about eMASS.

**LLM-agnostic backend.** The backend is not coupled to a specific LLM provider. The external LLM is a configuration concern, not an architectural one.

**eMASS as a tool surface.** Rather than building bespoke query logic, swordfish exposes eMASS operations as MCP tools. This means the LLM drives what gets read or written based on user intent, without the backend needing to anticipate every possible query shape.
