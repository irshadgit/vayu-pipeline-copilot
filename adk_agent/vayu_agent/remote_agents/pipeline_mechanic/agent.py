import os
from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from google.adk.tools.mcp_tool.mcp_toolset import SseConnectionParams, StreamableHTTPConnectionParams

# MCP server configuration
MCP_HOST = os.getenv("AIRFLOW_MCP_HOST", "localhost")
MCP_PORT = int(os.getenv("AIRFLOW_MCP_PORT", "3000"))

# GitHub MCP configuration
GITHUB_MCP_HOST = os.getenv("GITHUB_MCP_HOST", "localhost")
GITHUB_MCP_PORT = int(os.getenv("GITHUB_MCP_PORT", "3002"))
GITHUB_MCP_URL = "https://api.githubcopilot.com/mcp/"
GIT_PAT_TOKEN = os.getenv("GIT_PAT_TOKEN")
DAG_REPOSITORY = os.getenv("DAG_REPOSITORY")

# MCP connection parameters
MCP_CONNECTION_PARAMS = SseConnectionParams(url=f"http://{MCP_HOST}:{MCP_PORT}/sse")
# Local GitHub MCP server for get_file_contents
LOCAL_GITHUB_MCP_CONNECTION_PARAMS = SseConnectionParams(url=f"http://{GITHUB_MCP_HOST}:{GITHUB_MCP_PORT}/sse")
# Remote GitHub MCP server for other GitHub tools
REMOTE_GITHUB_MCP_CONNECTION_PARAMS = StreamableHTTPConnectionParams(
    url=GITHUB_MCP_URL,
    headers={"Authorization": f"Bearer {GIT_PAT_TOKEN}"} if GIT_PAT_TOKEN else {}
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
- `get_file_contents`: Get file contents from GitHub repository
- `search_code`: Search for DAG files in the repository 
- `create_branch`: Create a new branch for changes
- `create_or_update_file`: Create or update DAG file with current code
- `create_pull_request`: Create a pull request for DAG changes
- `get_dag_source`: Get DAG source code from Airflow (via DAG Manager Agent)
- `get_dag`: Get DAG information to identify the file (Airflow MCP)

**VERSION CONTROL WORKFLOW:**
1. **DAG Discovery**: Use `get_dag` to get DAG information and identify the file_token
2. **Source Retrieval**: Use `get_dag_source` with file_token to get current DAG code
3. **Repository Search**: Use `search_code` to find the DAG file in the repository
   - Search pattern: `repo:{dag_repo} path:*.py` (or specific file pattern)
4. **File Content Check**: Use `get_file_contents` to get current file information from repository. This also contains the sha value of the file. Use the value of repo and file path obtained from the previous step to get the file information.
5. **Branch Creation**: Create a new branch for the changes to the above file. Do not change the file name.
6. **File Update**: Use `create_or_update_file` to update the corresponding file in github with updated code in the branch created. For update operations use the SHA value of the file obtained from the previous step.
7. **Pull Request**: Create a PR with the above changes and proper description from the newly created branch to the main branch.

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
            # Local GitHub MCP server for get_file_contents
            McpToolset(
                connection_params=LOCAL_GITHUB_MCP_CONNECTION_PARAMS,
                tool_filter=[
                    'get_file_contents'
                ]
            ),
            # Remote GitHub MCP server for other GitHub tools
            McpToolset(
                connection_params=REMOTE_GITHUB_MCP_CONNECTION_PARAMS,
                tool_filter=[
                    'search_code',
                    'create_branch',
                    'create_or_update_file',
                    'create_pull_request'
                ]
            ),
            # Airflow MCP server
            McpToolset(
                connection_params=MCP_CONNECTION_PARAMS,
                tool_filter=[
                    'get_dag',
                    'get_dag_source'
                ]
            )
        ]
    )

# Create the agent instance
pipeline_mechanic_agent = create_pipeline_mechanic_agent()

# Expose root_agent for ADK API server
root_agent = pipeline_mechanic_agent

if __name__ == "__main__":
    print("🔧 PipelineMechanic Agent Initialized!")
    print(f"📡 Connecting to Airflow MCP server at {MCP_HOST}:{MCP_PORT}")
    print(f"📡 Connecting to Local GitHub MCP server at {GITHUB_MCP_HOST}:{GITHUB_MCP_PORT} (for get_file_contents)")
    print(f"📡 Connecting to Remote GitHub MCP server at {GITHUB_MCP_URL} (for other GitHub tools)")
    print(f"🎯 Target repository: {DAG_REPOSITORY or 'your-org/your-repo'}")
    print("💬 Ready to help manage version control of DAG files!")
    print("🚀 Use 'adk api_server --a2a --port 8003 vayu_agent/remote_agents/pipeline_mechanic' to start this agent")