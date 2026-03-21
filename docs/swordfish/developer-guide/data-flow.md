# Data Flow

A typical request follows this path:

1. The user types a question in the frontend
2. The frontend sends it to the backend
3. The backend forwards it to the external LLM with the available MCP tools in context
4. The LLM responds — either with a direct answer, or with one or more tool calls
5. Tool calls are routed to the MCP server, which reads from or writes to eMASS
6. Results are returned to the LLM to complete its response
7. The final answer is passed back through the backend to the frontend
