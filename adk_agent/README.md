# Vayu Airflow Management Agent

A Google ADK agent that connects to the Airflow MCP server to provide intelligent Airflow workflow management capabilities.

## Overview

This agent uses the Google ADK (Agent Development Kit) to create an LLM-powered assistant that can help manage Apache Airflow workflows. It connects to the Airflow MCP (Model Context Protocol) server in the `../airflow-mcp` directory to access Airflow data and operations.

## Features

The agent provides the following capabilities:

- **DAG Management**: List, filter, and get detailed information about DAGs
- **Task Analysis**: Examine task configurations and dependencies within DAGs  
- **Variable Access**: Retrieve and examine Airflow variables
- **Health Monitoring**: Check the status of the Airflow system
- **Intelligent Assistance**: Natural language interface for Airflow operations

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

This starts an interactive session where you can ask questions about your Airflow setup.

### Method 2: Direct Import
```python
from vayu_agent.agent import airflow_agent

# Ask about DAGs
response = airflow_agent.run("Show me all active DAGs")
print(response)

# Get specific DAG details  
response = airflow_agent.run("Get details for the data_pipeline_etl DAG")
print(response)

# Check variables
response = airflow_agent.run("What Airflow variables are configured?")
print(response)
```

## Example Interactions

- **"Show me all DAGs"** - Lists all available DAGs with their status
- **"Get details for example_python_operator"** - Shows detailed information about a specific DAG
- **"What tasks are in the data_pipeline_etl DAG?"** - Displays task information and dependencies
- **"Show me the email_config variable"** - Retrieves specific Airflow variable values
- **"Is the Airflow system healthy?"** - Performs a health check

## Architecture


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
│   └── agent.py          # Main agent implementation
├── run_agent.py          # Interactive startup script
├── requirements.txt      # Python dependencies
├── Dockerfile           # Container configuration
└── README.md           # This file
```

### Extending the Agent

To add new capabilities:

1. Add new tools to the MCP server (`../airflow-mcp/server.py`)
2. Update the `tool_filter` in `agent.py`
3. Enhance the agent's instruction prompt as needed

## License

This project is part of the Vayu Pipeline Copilot system.
```

</rewritten_file>