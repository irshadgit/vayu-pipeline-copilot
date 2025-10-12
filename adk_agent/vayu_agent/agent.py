import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset
from google.adk.tools.mcp_tool.mcp_toolset import SseConnectionParams, StreamableHTTPConnectionParams


# MCP server configuration
MCP_HOST = os.getenv("AIRFLOW_MCP_HOST", "localhost")
MCP_PORT = int(os.getenv("AIRFLOW_MCP_PORT", "3000"))
# Common MCP connection parameters
MCP_CONNECTION_PARAMS = SseConnectionParams(url=f"http://{MCP_HOST}:{MCP_PORT}/sse")

# GitHub MCP configuration
GITHUB_MCP_URL = "https://api.githubcopilot.com/mcp/"
GIT_PAT_TOKEN = os.getenv("GIT_PAT_TOKEN")
DAG_REPOSITORY = os.getenv("DAG_REPOSITORY")
# GitHub MCP connection parameters
GITHUB_MCP_CONNECTION_PARAMS = StreamableHTTPConnectionParams(
    url=GITHUB_MCP_URL,
    headers={"Authorization": f"Bearer {GIT_PAT_TOKEN}"} if GIT_PAT_TOKEN else {}
)

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

def create_pipeline_mechanic_agent() -> LlmAgent:
    """
    Creates the PipelineMechanic Agent - specializes in version control of DAG git repository.
    """
    # Create dynamic instruction with DAG repository only
    dag_repo = DAG_REPOSITORY or "your-org/your-repo"
    
    instruction = f"""You are the PipelineMechanic Agent, specialized in version control and git workflow management for DAG repositories.

📋 **TARGET REPOSITORY:**
- Repository: `{dag_repo}`

🔧 **TOOLS AVAILABLE:**
- `search_code`: Search for DAG files in the repository
- `create_branch`: Create a new branch for changes
- `create_or_update_file`: Create or update DAG file with current code
- `create_pull_request`: Create a pull request for DAG changes
- `get_dag_source`: Get DAG source code from Airflow (via DAG Manager Agent)
- `get_dag`: Get DAG information to identify the file

**VERSION CONTROL WORKFLOW:**
1. **DAG Discovery**: Use `get_dag` to get DAG information and identify the file_token
2. **Source Retrieval**: Use `get_dag_source` with file_token to get current DAG code
3. **Repository Search**: Use `search_code` to find the DAG file in the repository
   - Search pattern: `repo:{dag_repo} path:*.py` (or specific file pattern)
4. **Branch Creation**: Create a new branch for the changes
5. **File Update**: Use `create_or_update_file` to update the DAG file with current code
6. **Pull Request**: Create a PR with the updated DAG file and proper description

**SEARCH PATTERNS:**
- General DAG search: `repo:{dag_repo} path:*.py`
- Specific file search: `repo:{dag_repo} path:dag_file.py`
- Pattern examples:
  - `repo:irshadgit/dbt-spark-iceberg path:*.py`
  - `repo:{dag_repo} path:dag_file.py`

**GIT WORKFLOW CAPABILITIES:**
- Search and locate DAG files in the repository
- Create feature branches for DAG updates
- Generate pull requests with current DAG code
- Handle version control workflow
- Maintain proper git history and commit messages

**SIMPLIFIED WORKFLOW:**
1. Retrieve current DAG code from Airflow using `get_dag_source`
2. Search for the corresponding file in the repository using `search_code`
3. Create a new branch for the changes
4. Update the DAG file with current code using `create_or_update_file`
5. Create a pull request with the updated DAG file

**PR CREATION WORKFLOW:**
1. Create a descriptive branch name (e.g., `update-dag-my-dag-20241201`)
2. Generate a comprehensive PR title
3. Create detailed PR description including:
   - Summary of changes
   - DAG functionality description
   - Testing recommendations
   - Impact analysis
4. Set appropriate labels and reviewers
5. Link to related issues if applicable

**INTEGRATION WITH DAG MANAGER:**
- Use DAG Manager Agent tools to get current DAG source code
- Coordinate with other agents for comprehensive DAG management
- Directly create pull requests with current DAG code

Use these tools to maintain proper version control of DAG files and create pull requests with current DAG code from Airflow."""

    return LlmAgent(
        name="PipelineMechanicAgent",
        model="gemini-2.0-flash",
        instruction=instruction,
        tools=[
            MCPToolset(
                connection_params=GITHUB_MCP_CONNECTION_PARAMS,
                tool_filter=[
                    'search_code',
                    'create_branch',
                    'create_or_update_file',
                    'create_pull_request'
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
    pipeline_mechanic = create_pipeline_mechanic_agent()
    
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

**Delegate to PipelineMechanicAgent when:**
- User wants to manage version control of DAG files
- Keywords: "version control", "git", "repository", "commit", "pull request", "PR", "branch"
- Creating pull requests for DAG changes
- Managing DAG file updates in version control
- Git workflow management for DAG files
- **Keywords: "sync dag", "update repository", "commit changes", "create PR for dag"**
- **Keywords: "version control", "git workflow", "branch for dag", "merge dag changes"**
- **Keywords: "dag repository", "create pull request", "update DAG in git"**

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
- PipelineMechanicAgent: Expert in version control and git workflow management for DAG repositories

Use your sub-agents effectively to provide comprehensive Airflow management assistance.""",
        sub_agents=[
            dag_troubleshooter,
            metadata_agent,
            pipeline_mechanic
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
pipeline_mechanic_agent = None

# Extract sub-agents for direct access
for sub_agent in airflow_orchestrator.sub_agents:
    if sub_agent.name == "DagTroubleShooterAgent":
        dag_troubleshooter_agent = sub_agent
    elif sub_agent.name == "AirflowMetadataAgent":
        airflow_metadata_agent = sub_agent
    elif sub_agent.name == "PipelineMechanicAgent":
        pipeline_mechanic_agent = sub_agent

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
    print("🔧 **PIPELINE MECHANIC SUB-AGENT**")
    print("   - Manages version control of DAG git repository")
    print("   - Creates feature branches for DAG updates")
    print("   - Updates DAG files with current code from Airflow")
    print("   - Generates pull requests with updated DAG files")
    print("   - Handles complete git workflow for DAG file management")
    print("   - Uses Airflow get_dag_source for current DAG code")
    print()
    print("🔧 Available MCP Tools:")
    print("   Airflow Tools: get_dags, get_dag, get_dag_runs, get_dag_source, list_task_instances, get_task_instance, get_task_instance_tries, get_task_instance_try_details, get_task_instance_log, clear_task_instances, get_health, get_connections, get_connection, create_connection, update_connection, delete_connection, test_connection, get_configs, get_config, get_variables, get_variable, create_variable, update_variable, delete_variable")
    print("   GitHub Tools: search_code, create_branch, create_or_update_file, create_pull_request")
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
    print("   - 'Create a PR for my DAG changes' → Delegates to PipelineMechanic")
    print("   - 'Update repository with current DAG' → Delegates to PipelineMechanic")
    print("   - 'Create a branch for DAG updates' → Delegates to PipelineMechanic")
    print("   - 'Sync DAG with git repository' → Delegates to PipelineMechanic")
    print("   - 'Version control for DAG files' → Delegates to PipelineMechanic")
    print()
    print("🏗️  Agent Hierarchy:")
    print("   AirflowOrchestratorAgent (Parent)")
    print("   ├── DagTroubleShooterAgent (Sub-agent)")
    print("   ├── AirflowMetadataAgent (Sub-agent)")
    print("   └── PipelineMechanicAgent (Sub-agent)")
