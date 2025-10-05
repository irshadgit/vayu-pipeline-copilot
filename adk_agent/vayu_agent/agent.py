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
- `get_dag_runs`: Get DAG run information
- `get_dag_source`: Get DAG source code for analysis and debugging
- `list_task_instances`: List task instances for a specific DAG run
- `get_task_instance`: Get details of a specific task instance
- `get_task_instance_tries`: Get all tries for a specific task instance
- `get_task_instance_try_details`: Get detailed information about a specific try
- `get_task_instance_log`: Get logs for a specific task instance try
- `clear_task_instances`: Clear a set of task instances for retry or reset
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
            MCPToolset(
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
- `get_dag_runs`: Get DAG run information
- `list_task_instances`: List task instances for a specific DAG run
- `get_task_instance`: Get details of a specific task instance
- `get_task_instance_tries`: Get all tries for a specific task instance
- `get_task_instance_try_details`: Get detailed information about a specific try
- `get_task_instance_log`: Get logs for a specific task instance try
- `clear_task_instances`: Clear a set of task instances for retry or reset
- `get_health`: Check system health. This also gives the status of different airflow components
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

**TASK INSTANCE MANAGEMENT CAPABILITIES:**
- Clear failed tasks to allow them to be retried
- Reset the state of specific tasks in a DAG run
- Clear running tasks that are stuck or problematic
- Reset multiple tasks across different DAG runs
- Perform dry runs to see what tasks would be cleared
- Clear tasks with specific execution date ranges
- Clear tasks in subdags or parent DAGs

Use these tools to retrieve and present Airflow information in a clear, user-friendly format, and manage task instance states when needed.""",
        tools=[
            MCPToolset(
                connection_params=MCP_CONNECTION_PARAMS,
                tool_filter=[
                    'get_dags',
                    'get_dag',
                    'get_dag_runs',
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
- Task instance failures or execution issues
- Analysis of task-level problems within DAG runs
- Debugging specific task instances that are failing or stuck
- Analyzing retry history and repeated failures
- Investigating specific execution attempts and their details
- Debugging task failures by examining log output
- Analyzing error messages and stack traces from logs
- **DAG source code analysis and logic inspection**
- **Questions about what a DAG does or how it works**
- **Keywords: "source code", "logic", "what does", "how does", "explain", "analyze", "inspect"**
- **Understanding DAG structure, task dependencies, and workflow patterns**
- **Connection-related troubleshooting and debugging**
- **Keywords: "connection failed", "connection error", "database connection", "connection test"**
- **Creating, updating, or deleting connections**
- **Testing connection connectivity and configuration**
- **Configuration troubleshooting and information retrieval**
- **Keywords: "config", "configuration", "settings", "config error"**
- **Getting configuration information and details**
- **Variable management and troubleshooting**
- **Keywords: "variable", "variables", "variable error", "variable not found"**
- **Creating, updating, or deleting variables**
- **Variable configuration and value management**
- **Task instance clearing and reset operations**
- **Keywords: "clear", "reset", "retry", "clear tasks", "clear failed tasks", "clear running tasks"**
- **Clearing specific tasks or task instances for retry**
- **Resetting task states to allow re-execution**

**Delegate to AirflowMetadataAgent when:**
- User wants to retrieve information about DAGs, tasks, or variables
- Keywords: "show", "list", "get", "details", "information", "what is"
- General queries about DAG configurations, schedules, or metadata
- Variable retrieval or configuration queries
- Health checks and system status requests
- Basic informational requests about Airflow components
- Task instance monitoring and status queries
- Detailed task execution information and history
- Getting specific details about individual task instances
- Retrieving retry history and execution attempts
- Getting detailed information about specific tries
- Retrieving and presenting log content from task executions
- **Connection information retrieval and listing**
- **Keywords: "show connections", "list connections", "connection details", "connection info"**
- **Getting specific connection configuration details**
- **Configuration information retrieval and listing**
- **Keywords: "show config", "list config", "config details", "configuration info"**
- **Getting specific configuration settings**
- **Variable information retrieval and listing**
- **Keywords: "show variables", "list variables", "variable details", "variable info"**
- **Getting specific variable values and configurations**
- **Task instance clearing and reset operations (when informational)**
- **Keywords: "clear tasks", "reset tasks", "dry run clear", "show what would be cleared"**
- **Performing dry runs to see what tasks would be cleared**
- **Clearing tasks when requested as an informational operation**

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
    print("   - Troubleshoots task instance failures and execution issues")
    print("   - Clears and resets task instances for retry")
    print("   - Provides actionable troubleshooting guidance")
    print()
    print("📊 **AIRFLOW METADATA SUB-AGENT**")
    print("   - Retrieves comprehensive DAG and task information")
    print("   - Manages Airflow variables and configurations")
    print("   - Lists and retrieves variable information")
    print("   - Performs system health checks and monitoring")
    print("   - Monitors task instances and execution details")
    print("   - Clears task instances for informational purposes")
    print("   - Presents data in user-friendly formats")
    print()
    print("🔧 Available MCP Tools: get_dags, get_dag, get_dag_runs, get_dag_source, list_task_instances, get_task_instance, get_task_instance_tries, get_task_instance_try_details, get_task_instance_log, clear_task_instances, get_health, get_connections, get_connection, create_connection, update_connection, delete_connection, test_connection, get_configs, get_config, get_variables, get_variable, create_variable, update_variable, delete_variable")
    print("💬 Ready to help manage and troubleshoot your Airflow workflows!")
    print()
    print("💡 Usage Examples:")
    print("   - 'My DAG is failing with import errors' → Delegates to TroubleShooter")
    print("   - 'Show me details of the data_pipeline_etl DAG' → Delegates to Metadata Agent")
    print("   - 'Why isn't my DAG running?' → Delegates to TroubleShooter")
    print("   - 'List all active DAGs' → Delegates to Metadata Agent")
    print("   - 'Show me task instances for DAG run X' → Delegates to Metadata Agent")
    print("   - 'Why is task Y failing in my DAG?' → Delegates to TroubleShooter")
    print("   - 'Get details of task Z in DAG run W' → Delegates to Metadata Agent")
    print("   - 'Debug the python_task in sample_dag run' → Delegates to TroubleShooter")
    print("   - 'Show me all tries for task X' → Delegates to Metadata Agent")
    print("   - 'Why is my task failing repeatedly?' → Delegates to TroubleShooter")
    print("   - 'Get details of try 3 for task Y' → Delegates to Metadata Agent")
    print("   - 'Show me logs for task Z try 2' → Delegates to Metadata Agent")
    print("   - 'What error is in the logs for my failed task?' → Delegates to TroubleShooter")
    print("   - 'What does the data_processing DAG do?' → Delegates to TroubleShooter")
    print("   - 'Show me the source code of my DAG' → Delegates to TroubleShooter")
    print("   - 'Explain the logic of the ETL pipeline DAG' → Delegates to TroubleShooter")
    print("   - 'Analyze the task dependencies in my DAG' → Delegates to TroubleShooter")
    print("   - 'How does the scheduling work in this DAG?' → Delegates to TroubleShooter")
    print("   - 'List all connections' → Delegates to Metadata Agent")
    print("   - 'Show me connection details for postgres_db' → Delegates to Metadata Agent")
    print("   - 'Create a new database connection' → Delegates to TroubleShooter")
    print("   - 'Test my database connection' → Delegates to TroubleShooter")
    print("   - 'My connection is failing' → Delegates to TroubleShooter")
    print("   - 'List all configuration settings' → Delegates to Metadata Agent")
    print("   - 'Show me database configuration details' → Delegates to Metadata Agent")
    print("   - 'My configuration is causing errors' → Delegates to TroubleShooter")
    print("   - 'List all variables' → Delegates to Metadata Agent")
    print("   - 'Show me variable details for API_KEY' → Delegates to Metadata Agent")
    print("   - 'Create a new variable for database URL' → Delegates to TroubleShooter")
    print("   - 'Update my API key variable' → Delegates to TroubleShooter")
    print("   - 'Delete an unused variable' → Delegates to TroubleShooter")
    print("   - 'My variable is not being found' → Delegates to TroubleShooter")
    print("   - 'Clear all failed tasks in my DAG' → Delegates to TroubleShooter")
    print("   - 'Reset the python_task to retry it' → Delegates to TroubleShooter")
    print("   - 'Clear stuck running tasks' → Delegates to TroubleShooter")
    print("   - 'Show me what tasks would be cleared' → Delegates to Metadata Agent")
    print("   - 'Clear tasks in DAG run X' → Delegates to TroubleShooter")
    print()
    print("🏗️  Agent Hierarchy:")
    print("   AirflowOrchestratorAgent (Parent)")
    print("   ├── DagTroubleShooterAgent (Sub-agent)")
    print("   └── AirflowMetadataAgent (Sub-agent)")
