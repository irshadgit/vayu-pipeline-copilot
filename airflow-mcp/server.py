import os
from fastmcp import FastMCP

from tools.dag import DAG_COLLECTION_SCHEMA, DAG_SCHEMA, get_dags_tool, get_dag_tool


transport = os.getenv("MCP_TRANSPORT", "sse")
mcp_host = os.getenv("MCP_HOST", "0.0.0.0")
mcp_port = int(os.getenv("MCP_PORT", "3000"))
log_level = os.getenv("LOG_LEVEL", "info").lower()

mcp = FastMCP("airflow-mcp-server 🚁")


mcp.tool(
    name="get_dags",
    description="Get all DAGs with optional filtering and pagination.",
    output_schema=DAG_COLLECTION_SCHEMA
)(get_dags_tool)

mcp.tool(
    name="get_dag",
    description="Get a specific DAG by its dag_id.",
    output_schema=DAG_SCHEMA
)(get_dag_tool)

# ============================================================================
# Health Check Schema
# ============================================================================

HEALTH_RESPONSE_SCHEMA = {
    "type": "object",
    "description": "Health check response",
    "properties": {
        "status": {
            "type": "string",
            "description": "Server health status",
            "enum": ["OK", "ERROR", "DEGRADED"]
        },
        "message": {
            "type": "string",
            "description": "Status message"
        }
    },
    "required": ["status", "message"]
}

@mcp.tool(
    "health",
    description="Health check endpoint for testing server connectivity.",
    output_schema=HEALTH_RESPONSE_SCHEMA
)
async def health_check() -> str:
    """
    Health check endpoint for testing server connectivity.
    
    Returns:
        Simple string indicating server status
    """
    return "OK - Airflow MCP Server Running with Dummy Data"

if __name__ == "__main__":
    mcp.run(
        transport=transport,
        host=mcp_host,
        port=mcp_port,
        log_level=log_level
    )
