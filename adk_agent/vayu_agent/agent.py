"""
Vayu Pipeline Copilot - Main Orchestrator Agent
Uses A2A protocol to delegate to specialized remote agents
"""

import os
from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent, AGENT_CARD_WELL_KNOWN_PATH

# A2A Host configuration
A2A_HOST = os.getenv("A2A_HOST", "localhost")
A2A_PORT = os.getenv("A2A_PORT", "8000")

def create_vayu_orchestrator_agent() -> LlmAgent:
    """
    Creates the main Vayu Pipeline Copilot Orchestrator Agent using A2A protocol.
    """
    
    # Create RemoteA2aAgent instances for each specialized agent
    dag_troubleshooter_agent = RemoteA2aAgent(
        name="dag_troubleshooter_agent",
        description="Expert in diagnosing and resolving DAG issues, DAG source analysis, and task instance management",
        agent_card=f"http://{A2A_HOST}:{A2A_PORT}/a2a/dag_troubleshooter{AGENT_CARD_WELL_KNOWN_PATH}"
    )

    airflow_metadata_agent = RemoteA2aAgent(
        name="airflow_metadata_agent", 
        description="Specialist in retrieving and presenting Airflow information, metadata, and system monitoring",
        agent_card=f"http://{A2A_HOST}:{A2A_PORT}/a2a/airflow_metadata{AGENT_CARD_WELL_KNOWN_PATH}"
    )

    pipeline_mechanic_agent = RemoteA2aAgent(
        name="pipeline_mechanic_agent",
        description="Expert in version control and git workflow management for DAG repositories",
        agent_card=f"http://{A2A_HOST}:{A2A_PORT}/a2a/pipeline_mechanic{AGENT_CARD_WELL_KNOWN_PATH}"
    )

    # Create the orchestrator with RemoteA2A sub-agents
    orchestrator = LlmAgent(
        name="VayuPipelineCopilotAgent",
        model="gemini-2.0-flash",
        instruction="""You are the Vayu Pipeline Copilot Orchestrator Agent, the main entry point for all Airflow-related requests.

Your primary responsibility is to analyze incoming user requests and delegate them to the appropriate specialized remote sub-agent using A2A (Agent-to-Agent) protocol:

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

**AVAILABLE REMOTE AGENTS:**
- DagTroubleShooterAgent: Expert in diagnosing and resolving DAG issues
- AirflowMetadataAgent: Specialist in retrieving and presenting Airflow information
- PipelineMechanicAgent: Expert in version control and git workflow management for DAG repositories

**IMPORTANT:** You are the main orchestrator agent. When users ask questions, you should:
1. Analyze their request
2. Determine which remote agent would be best suited to handle it
3. Delegate to the appropriate sub-agent using A2A protocol
4. Present the sub-agent's response clearly

The remote agents are running on the A2A host at {A2A_HOST}:{A2A_PORT} and can be accessed through the A2A protocol.""".format(
            A2A_HOST=A2A_HOST,
            A2A_PORT=A2A_PORT
        ),
        sub_agents=[
            dag_troubleshooter_agent,
            airflow_metadata_agent, 
            pipeline_mechanic_agent
        ]
    )
    
    return orchestrator

# Create the orchestrator agent instance
vayu_orchestrator = create_vayu_orchestrator_agent()

# Expose root_agent for ADK web server
root_agent = vayu_orchestrator

if __name__ == "__main__":
    print("🚁 Vayu Pipeline Copilot Multi-Agent System Initialized!")
    print("🎯 **MAIN ORCHESTRATOR AGENT** (A2A Protocol)")
    print("   - Uses RemoteA2AAgent to connect to specialized remote agents")
    print("   - Provides unified user experience")
    print("   - Coordinates responses from multiple remote agents")
    print()
    print("🔧 **DAG TROUBLESHOOTER REMOTE AGENT**")
    print(f"   - A2A Endpoint: http://{A2A_HOST}:{A2A_PORT}/a2a/dag_troubleshooter")
    print("   - Diagnoses DAG import and parsing errors")
    print("   - Resolves runtime execution issues")
    print("   - Analyzes performance and configuration problems")
    print()
    print("📊 **AIRFLOW METADATA REMOTE AGENT**")
    print(f"   - A2A Endpoint: http://{A2A_HOST}:{A2A_PORT}/a2a/airflow_metadata")
    print("   - Retrieves comprehensive DAG and task information")
    print("   - Manages Airflow variables and configurations")
    print("   - Performs system health checks and monitoring")
    print()
    print("🔧 **PIPELINE MECHANIC REMOTE AGENT**")
    print(f"   - A2A Endpoint: http://{A2A_HOST}:{A2A_PORT}/a2a/pipeline_mechanic")
    print("   - Manages version control of DAG git repository")
    print("   - Creates feature branches for DAG updates")
    print("   - Generates pull requests with updated DAG files")
    print()
    print("💬 Ready to help manage and troubleshoot your Airflow workflows!")
    print()
    print("🏗️  Agent Hierarchy (A2A):")
    print("   VayuPipelineCopilotAgent (Root)")
    print("   ├── DagTroubleShooterAgent (RemoteA2A)")
    print("   ├── AirflowMetadataAgent (RemoteA2A)")
    print("   └── PipelineMechanicAgent (RemoteA2A)")
    print()
    print(f"🌐 A2A Host: {A2A_HOST}:{A2A_PORT}")
    print("🚀 Use 'adk web vayu_agent' to start the main orchestrator")
