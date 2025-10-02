import os
from fastmcp import FastMCP

from tools.registry import register_all


transport = os.getenv("MCP_TRANSPORT", "sse")
mcp_host = os.getenv("MCP_HOST", "0.0.0.0")
mcp_port = int(os.getenv("MCP_PORT", "3000"))
log_level = os.getenv("LOG_LEVEL", "info").lower()

mcp = FastMCP("airflow-mcp-server 🚁")

register_all(mcp)

if __name__ == "__main__":
    mcp.run(
        transport=transport,
        host=mcp_host,
        port=mcp_port,
        log_level=log_level
    )
