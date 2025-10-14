import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_toolset import SseConnectionParams

# MCP server configuration
MCP_HOST = os.getenv("AIRFLOW_MCP_HOST", "localhost")
MCP_PORT = int(os.getenv("AIRFLOW_MCP_PORT", "3000"))

# Common MCP connection parameters
MCP_CONNECTION_PARAMS = SseConnectionParams(url=f"http://{MCP_HOST}:{MCP_PORT}/sse")

def create_dag_troubleshooter_agent() -> LlmAgent:
    """
    Creates the DAG TroubleShooter Agent - specializes in diagnosing and resolving DAG issues.
    """
    return LlmAgent(
        name="DagTroubleShooterAgent",
        model="gemini-2.0-flash",
        instruction="""You are the DAG TroubleShooter Agent, specialized in diagnosing and resolving Apache Airflow DAG issues.



🔧 **TOOLS AVAILABLE:**
- `get_dags`: List and filter DAGs
- `get_dag`: Get specific DAG information
- `get_dag_runs`: Get DAG run information
- `get_dag_source`: Get DAG source code for analysis and debugging
- `list_task_instances`: List task instances for a specific DAG run
- `get_task_instance`: Get details of a specific task instance
- `get_task_instance_tries`: Get all tries for a specific task instance
- `get_task_instance_try_details`: Get detailed information about a specific try
- `get_task_instance_log`: Get logs for a specific task instance try
- `clear_task_instances`: Clear a set of task instances for retry or reset. When clearing failed tasks always clear downstream tasks and reset dag run as well
- `get_health`: Check system health. This also give status of different airflow components
- `get_connections`: List and filter connections
- `get_connection`: Get specific connection details
- `create_connection`: Create new connections
- `update_connection`: Update existing connections
- `delete_connection`: Delete connections
- `test_connection`: Test connection connectivity
- `get_configs`: Get all configuration settings
- `get_config`: Get specific configuration value by section and option
- `get_variables`: List and filter variables
- `get_variable`: Get specific variable details
- `create_variable`: Create new variables
- `update_variable`: Update existing variables (value and description)
- `delete_variable`: Delete variables

**DAG SOURCE ANALYSIS CAPABILITIES:**
- Inspect DAG source code to understand logic and structure
- Analyze task dependencies and workflow patterns
- Identify potential issues in DAG implementation
- Explain what a DAG does and how it works
- Debug DAG logic problems and suggest improvements
- Review task configurations and scheduling logic

**WORKFLOW FOR DAG ANALYSIS:**
1. First, get DAG details using `get_dag` to obtain the file_token
2. Use `get_dag_source` with the file_token to retrieve the source code
3. Analyze the source code to understand the DAG's purpose and logic
4. Cross-reference with runtime data (DAG runs, task instances) if needed
5. Provide comprehensive analysis and recommendations

**TASK INSTANCE MANAGEMENT CAPABILITIES:**
- Clear failed tasks to allow them to be retried
- Reset the state of specific tasks in a DAG run
- Clear running tasks that are stuck or problematic
- Reset multiple tasks across different DAG runs
- Perform dry runs to see what tasks would be cleared
- Clear tasks with specific execution date ranges
- Clear tasks in subdags or parent DAGs

Use these tools to diagnose DAG import errors, runtime issues, performance problems, configuration issues, analyze DAG logic, and manage task instance states. Provide clear analysis and actionable solutions.""",
        tools=[
            McpToolset(
                connection_params=MCP_CONNECTION_PARAMS,
                tool_filter=[
                    'get_dags',
                    'get_dag',
                    'get_dag_runs',
                    'get_dag_source',
                    'list_task_instances',
                    'get_task_instance',
                    'get_task_instance_tries',
                    'get_task_instance_try_details',
                    'get_task_instance_log',
                    'clear_task_instances',
                    'get_health',
                    'get_connections',
                    'get_connection',
                    'create_connection',
                    'update_connection',
                    'delete_connection',
                    'test_connection',
                    'get_configs',
                    'get_config',
                    'get_variables',
                    'get_variable',
                    'create_variable',
                    'update_variable',
                    'delete_variable'
                ]
            )
        ]
    )

# Create the agent instance
dag_troubleshooter_agent = create_dag_troubleshooter_agent()

# Expose root_agent for ADK API server
root_agent = dag_troubleshooter_agent

if __name__ == "__main__":
    print("🔧 DAG TroubleShooter Agent Initialized!")
    print(f"📡 Connecting to MCP server at {MCP_HOST}:{MCP_PORT}")
    print("💬 Ready to help diagnose and resolve DAG issues!")
    print("🚀 Use 'adk api_server --a2a --port 8001 vayu_agent/remote_agents/dag_troubleshooter' to start this agent")