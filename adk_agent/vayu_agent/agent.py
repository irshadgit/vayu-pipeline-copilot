import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_session_manager import SseServerParams


# MCP server configuration
MCP_HOST = os.getenv("MCP_HOST", "localhost")
MCP_PORT = int(os.getenv("MCP_PORT", "3000"))

# Common MCP connection parameters
MCP_CONNECTION_PARAMS = SseServerParams(url=f"http://{MCP_HOST}:{MCP_PORT}/sse")

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
- `get_dag_details`: Get detailed DAG info including tasks
- `get_variable`: Retrieve Airflow variables
- `get_dag_runs`: Get DAG run information
- `health`: Check system health

Use these tools to diagnose DAG import errors, runtime issues, performance problems, and configuration issues. Provide clear analysis and actionable solutions.""",
        tools=[
            MCPToolset(
                connection_params=MCP_CONNECTION_PARAMS,
                tool_filter=[
                    'get_dags',
                    'get_dag',
                    'get_dag_details', 
                    'get_variable',
                    'get_dag_runs',
                    'health'
                ]
            )
        ]
    )

def create_airflow_metadata_agent() -> LlmAgent:
    """
    Creates the Airflow Metadata Agent - specializes in retrieving and presenting Airflow information.
    """
    return LlmAgent(
        name="AirflowMetadataAgent",
        model="gemini-2.0-flash", 
        instruction="""You are the Airflow Metadata Agent, specialized in retrieving metadata about Airflow such as DAGs, variables, DAG runs, task instances, etc.

📊 **TOOLS AVAILABLE:**
- `get_dags`: List and filter DAGs
- `get_dag`: Get specific DAG information  
- `get_dag_details`: Get detailed DAG info including tasks
- `get_variable`: Retrieve Airflow variables
- `get_dag_runs`: Get DAG run information
- `health`: Check system health

Use these tools to retrieve and present Airflow information in a clear, user-friendly format.""",
        tools=[
            MCPToolset(
                connection_params=MCP_CONNECTION_PARAMS,
                tool_filter=[
                    'get_dags',
                    'get_dag',
                    'get_dag_details',
                    'get_variable',
                    'get_dag_runs',
                    'health'
                ]
            )
        ]
    )

def create_airflow_orchestrator_agent() -> LlmAgent:
    """
    Creates the main Airflow Orchestrator Agent with specialized sub-agents.
    """
    # Create specialized sub-agents
    dag_troubleshooter = create_dag_troubleshooter_agent()
    metadata_agent = create_airflow_metadata_agent()
    
    # Create the orchestrator with sub-agents
    orchestrator = LlmAgent(
        name="AirflowOrchestratorAgent",
        model="gemini-2.0-flash",
        instruction="""You are the Airflow Copilot Orchestrator Agent, the main entry point for all Airflow-related requests.

Your primary responsibility is to analyze incoming user requests and delegate them to the appropriate specialized sub-agent:

🎯 **DELEGATION STRATEGY:**

**Delegate to DagTroubleShooterAgent when:**
- User mentions errors, failures, or issues with DAGs
- Keywords: "error", "failed", "broken", "not working", "troubleshoot", "debug", "fix"
- DAG import errors, parsing issues, or runtime failures
- Task failures or stuck DAG runs
- Performance issues or timeout problems
- Questions about why a DAG isn't running as expected

**Delegate to AirflowMetadataAgent when:**
- User wants to retrieve information about DAGs, tasks, or variables
- Keywords: "show", "list", "get", "details", "information", "what is"
- General queries about DAG configurations, schedules, or metadata
- Variable retrieval or configuration queries
- Health checks and system status requests
- Basic informational requests about Airflow components

**DELEGATION RULES:**
1. Always analyze the user's intent before delegating
2. Choose the most appropriate sub-agent based on the request type
3. If a request spans multiple areas, start with the most relevant agent
4. Always explain to the user which sub-agent is handling their request
5. Present the sub-agent's response clearly and offer follow-up assistance

**RESPONSE FORMAT:**
- Start with: "🎯 Delegating your request to [Sub-Agent Name]..."
- Briefly explain why this sub-agent was chosen
- Present the sub-agent's response
- Offer follow-up assistance if needed

**AVAILABLE SUB-AGENTS:**
- DagTroubleShooterAgent: Expert in diagnosing and resolving DAG issues
- AirflowMetadataAgent: Specialist in retrieving and presenting Airflow information

Use your sub-agents effectively to provide comprehensive Airflow management assistance.""",
        sub_agents=[
            dag_troubleshooter,
            metadata_agent
        ]
    )
    
    return orchestrator

# Initialize the multi-agent system using ADK hierarchy
airflow_orchestrator = create_airflow_orchestrator_agent()

# Main agent (orchestrator is the primary interface)
root_agent = airflow_orchestrator

# Access to sub-agents for direct use if needed
dag_troubleshooter_agent = None
airflow_metadata_agent = None

# Extract sub-agents for direct access
for sub_agent in airflow_orchestrator.sub_agents:
    if sub_agent.name == "DagTroubleShooterAgent":
        dag_troubleshooter_agent = sub_agent
    elif sub_agent.name == "AirflowMetadataAgent":
        airflow_metadata_agent = sub_agent

# Legacy aliases for backward compatibility
troubleshooter_agent = dag_troubleshooter_agent
metadata_agent = airflow_metadata_agent

if __name__ == "__main__":
    print("🚁 Airflow Copilot Multi-Agent System Initialized!")
    print(f"📡 Connecting to MCP server at {MCP_HOST}:{MCP_PORT}")
    print("🎯 **ORCHESTRATOR AGENT** (Main Entry Point)")
    print("   - Analyzes requests and delegates to specialized sub-agents")
    print("   - Provides unified user experience")
    print("   - Coordinates responses from multiple agents")
    print()
    print("🔧 **DAG TROUBLESHOOTER SUB-AGENT**")
    print("   - Diagnoses DAG import and parsing errors")
    print("   - Resolves runtime execution issues")
    print("   - Analyzes performance and configuration problems")
    print("   - Provides actionable troubleshooting guidance")
    print()
    print("📊 **AIRFLOW METADATA SUB-AGENT**")
    print("   - Retrieves comprehensive DAG and task information")
    print("   - Manages Airflow variables and configurations")
    print("   - Performs system health checks and monitoring")
    print("   - Presents data in user-friendly formats")
    print()
    print("🔧 Available MCP Tools: get_dags, get_dag, get_dag_details, get_variable, health")
    print("💬 Ready to help manage and troubleshoot your Airflow workflows!")
    print()
    print("💡 Usage Examples:")
    print("   - 'My DAG is failing with import errors' → Delegates to TroubleShooter")
    print("   - 'Show me details of the data_pipeline_etl DAG' → Delegates to Metadata Agent")
    print("   - 'Why isn't my DAG running?' → Delegates to TroubleShooter")
    print("   - 'List all active DAGs' → Delegates to Metadata Agent")
    print()
    print("🏗️  Agent Hierarchy:")
    print("   AirflowOrchestratorAgent (Parent)")
    print("   ├── DagTroubleShooterAgent (Sub-agent)")
    print("   └── AirflowMetadataAgent (Sub-agent)")
