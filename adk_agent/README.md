# Vayu Airflow Copilot Multi-Agent System

A sophisticated Google ADK multi-agent system that provides comprehensive Airflow workflow management and troubleshooting capabilities through specialized AI agents.

## Overview

This system uses the Google ADK (Agent Development Kit) to create a hierarchical multi-agent architecture with specialized agents for different aspects of Airflow management. The system connects to the Airflow MCP (Model Context Protocol) server to access Airflow data and operations.

## Architecture

The system follows Google ADK's native agent hierarchy pattern with `sub_agents`:

```
AirflowOrchestratorAgent (Parent)
├── DagTroubleShooterAgent (Sub-agent)
└── AirflowMetadataAgent (Sub-agent)
```

## Agent Capabilities

### 🎯 Orchestrator Agent (Main Interface)
- **Intelligent Request Routing**: Analyzes user queries and delegates to appropriate sub-agents
- **Unified Experience**: Provides a single entry point for all Airflow operations
- **Context Management**: Coordinates responses from multiple specialized agents

### 🔧 DAG TroubleShooter Agent
- **Error Diagnosis**: Identifies DAG import errors, parsing failures, and runtime issues
- **Performance Analysis**: Analyzes task execution bottlenecks and timeout problems
- **Configuration Validation**: Validates DAG and task configurations against best practices
- **Solution Recommendations**: Provides specific, actionable troubleshooting steps

### 📊 Airflow Metadata Agent
- **Information Retrieval**: Comprehensive DAG, task, and variable information access
- **Data Presentation**: User-friendly formatting of complex Airflow configurations
- **System Monitoring**: Health checks and status reporting
- **Search & Filtering**: Advanced filtering and pattern matching for large datasets

## Prerequisites

1. **MCP Server**: The Airflow MCP server must be running
2. **Google ADK**: Properly configured ADK environment
3. **Python 3.8+**: Compatible Python version

## Setup

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the MCP Server**:
   ```bash
   cd ../airflow-mcp
   python server.py
   ```
   The server will start on `localhost:3000` by default.

3. **Configure Environment** (optional):
   ```bash
   export MCP_HOST=localhost
   export MCP_PORT=3000
   ```

## Usage

### Method 1: Interactive Script
```bash
python run_agent.py
```

This starts an interactive session where you can ask questions about your Airflow setup. The orchestrator will automatically route your requests to the appropriate sub-agent.

### Method 2: Direct Import (Recommended)
```python
from vayu_agent.agent import root_agent

# The orchestrator automatically delegates to the right sub-agent
response = root_agent.run("Show me all active DAGs")
print(response)

response = root_agent.run("My DAG is failing with import errors")
print(response)

response = root_agent.run("Get details for the data_pipeline_etl DAG")
print(response)
```

### Method 3: Direct Sub-Agent Access (Advanced)
```python
from vayu_agent.agent import dag_troubleshooter_agent, airflow_metadata_agent

# Direct troubleshooting
response = dag_troubleshooter_agent.run("Analyze performance issues in my DAG")
print(response)

# Direct metadata access
response = airflow_metadata_agent.run("List all DAGs with production tag")
print(response)
```

## Example Interactions

### Troubleshooting Queries (→ DagTroubleShooterAgent)
- **"My DAG is failing with import errors"** - Diagnoses parsing and import issues
- **"Why isn't my data_pipeline_etl DAG running?"** - Analyzes execution problems
- **"Fix performance issues in ml_training_pipeline"** - Identifies bottlenecks and optimization opportunities
- **"Troubleshoot timeout errors in my DAG"** - Analyzes timeout configurations and suggests fixes

### Information Queries (→ AirflowMetadataAgent)  
- **"Show me all active DAGs"** - Lists DAGs with current status
- **"Get details for example_python_operator"** - Shows comprehensive DAG information
- **"What tasks are in the data_pipeline_etl DAG?"** - Displays task hierarchy and dependencies
- **"Show me the email_config variable"** - Retrieves and formats variable values
- **"Is the Airflow system healthy?"** - Performs system health checks

## Agent Hierarchy Benefits

Using Google ADK's native `sub_agents` pattern provides:

- **🎯 Automatic Delegation**: The orchestrator intelligently routes requests to specialized sub-agents
- **🔄 Parent-Child Relationships**: ADK automatically manages agent relationships (`parent_agent` and `sub_agents`)
- **🧠 Specialized Expertise**: Each sub-agent has focused knowledge and capabilities
- **🚀 Scalable Architecture**: Easy to add new specialized agents as sub-agents
- **💡 Clean Code**: Leverages ADK's built-in agent coordination mechanisms

## Configuration

### Environment Variables

- `MCP_HOST`: MCP server hostname (default: `localhost`)
- `MCP_PORT`: MCP server port (default: `3000`)

### MCP Server Tools

The agent has access to these MCP tools:

- `get_dags`: List and filter DAGs
- `get_dag`: Get specific DAG information
- `get_dag_details`: Get detailed DAG info including tasks
- `get_variable`: Retrieve Airflow variables
- `health`: Health check the system

## Troubleshooting

### Common Issues

1. **Connection Error**: Ensure the MCP server is running
   ```bash
   cd ../airflow-mcp && python server.py
   ```

2. **Import Error**: Check that ADK is properly installed
   ```bash
   pip install google-adk==1.14.1
   ```

3. **Tool Not Found**: Verify the MCP server is exposing the expected tools

### Debug Mode

Set environment variable for verbose logging:
```bash
export LOG_LEVEL=debug
```

## Development

### Project Structure
```
adk_agent/
├── vayu_agent/
│   ├── __init__.py
│   └── agent.py          # Multi-agent system with ADK hierarchy
├── run_agent.py          # Interactive startup script
├── example_usage.py      # Usage examples and demonstrations
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container configuration
└── README.md           # This file
```

### Extending the Multi-Agent System

To add new capabilities:

1. **Add MCP Tools**: Add new tools to the MCP server (`../airflow-mcp/server.py`)
2. **Create New Sub-Agent**: Create a new specialized agent function in `agent.py`
3. **Update Orchestrator**: Add the new sub-agent to the orchestrator's `sub_agents` list
4. **Update Instructions**: Enhance delegation logic in the orchestrator's instruction prompt

Example of adding a new sub-agent:
```python
def create_new_specialist_agent() -> LlmAgent:
    return LlmAgent(
        name="NewSpecialistAgent",
        model="gemini-2.0-flash",
        instruction="Your specialized instruction...",
        tools=[MCPToolset(...)]
    )

# Add to orchestrator
orchestrator = LlmAgent(
    name="AirflowOrchestratorAgent",
    sub_agents=[
        dag_troubleshooter,
        metadata_agent,
        create_new_specialist_agent()  # Add here
    ]
)
```

## License

This project is part of the Vayu Pipeline Copilot system.
```

</rewritten_file>