# Design Principles

**Separation of concerns.**  
Each container has a single, well-defined responsibility. The frontend knows about the user. The backend knows about the LLM. The MCP server knows about eMASS.

**LLM-agnostic backend.**  
The backend is not coupled to a specific LLM provider. The external LLM is a configuration concern, not an architectural one.

**eMASS as a tool surface.**  
Rather than building bespoke query logic, swordfish exposes eMASS operations as MCP tools. This means the LLM drives what gets read or written based on user intent, without the backend needing to anticipate every possible query shape.
