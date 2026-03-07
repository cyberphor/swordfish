# Third-party imports.
from mcp.server.fastmcp import FastMCP
from strands_tools import calculator

mcp = FastMCP(
    name="swordfish", host="0.0.0.0", port=8282, debug=True, log_level="DEBUG"
)

mcp.tool = [calculator]

if __name__ == "__main__":
    mcp.run(transport="sse")
