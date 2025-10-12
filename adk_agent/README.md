# Vayu Pipeline Copilot - A2A Multi-Agent System

This project implements a modular multi-agent system using Google ADK's Agent-to-Agent (A2A) protocol for comprehensive Airflow management, following the [official ADK A2A sample structure](https://github.com/google/adk-python/tree/main/contributing/samples/a2a_basic).

## 🏗️ Architecture Overview

The system consists of a main orchestrator agent that delegates tasks to specialized remote agents using A2A protocol:

```
VayuPipelineCopilotAgent (Root - Port 8000)
├── DagTroubleShooterAgent (RemoteA2A - Port 8001)
├── AirflowMetadataAgent (RemoteA2A - Port 8002)
└── PipelineMechanicAgent (RemoteA2A - Port 8003)
```

## 📁 Project Structure

```
adk_agent/
├── vayu_agent/                          # Main orchestrator package
│   ├── main.py                          # Main entry point
│   ├── orchestrator.py                  # Orchestrator agent with A2A
│   ├── agent.py                         # Legacy agent (can be removed)
│   └── remote_agents/                   # Remote agent implementations
│       ├── dag_troubleshooter/
│       │   ├── agent.py                 # DAG troubleshooting agent
│       │   └── agent.json               # Agent metadata
│       ├── airflow_metadata/
│       │   ├── agent.py                 # Metadata retrieval agent
│       │   └── agent.json               # Agent metadata
│       └── pipeline_mechanic/
│           ├── agent.py                 # Version control agent
│           └── agent.json               # Agent metadata
├── start_all_vayu.sh                    # Complete system startup
├── start_remote_agents.sh               # Remote agents only
├── start_main_agent.sh                  # Main orchestrator only
├── docker-compose.yml                   # Docker Compose for A2A
└── README.md                            # This file
```

## 🤖 Agent Descriptions

### 1. VayuPipelineCopilotAgent (Main Orchestrator - Port 8000)
**Purpose**: Main entry point that delegates to remote agents using A2A protocol
**Capabilities**:
- Request analysis and delegation
- A2A communication with remote agents
- Response coordination and presentation
- Unified user experience

### 2. DagTroubleShooterAgent (RemoteA2A - Port 8001)
**Purpose**: Diagnose and resolve DAG issues
**Capabilities**:
- DAG source code analysis
- Task instance management
- Connection troubleshooting
- Configuration management
- Variable management
- DAG debugging and diagnostics

### 3. AirflowMetadataAgent (RemoteA2A - Port 8002)
**Purpose**: Retrieve and present Airflow information
**Capabilities**:
- DAG information retrieval
- Task instance monitoring
- Connection management
- Configuration management
- Variable management
- System health monitoring

### 4. PipelineMechanicAgent (RemoteA2A - Port 8003)
**Purpose**: Version control and git workflow management
**Capabilities**:
- DAG version control
- Git workflow management
- Repository file operations
- Pull request creation
- Branch management
- DAG synchronization

## 🚀 Quick Start

### Option 1: Start All Agents (Recommended)

```bash
cd /home/irshad/my-repo/vayu-pipeline-copilot/adk_agent
source .venv/bin/activate
./start_all_vayu.sh
```

This will:
1. Start all remote agents using `adk api_server --a2a` (ports 8001, 8002, 8003)
2. Start the main orchestrator agent using `adk web` (port 8000)
3. Set up A2A communication between them

### Option 2: Start Remote Agents Only

```bash
cd /home/irshad/my-repo/vayu-pipeline-copilot/adk_agent
source .venv/bin/activate
./start_remote_agents.sh
```

Then in another terminal:
```bash
cd /home/irshad/my-repo/vayu-pipeline-copilot/adk_agent
source .venv/bin/activate
./start_main_agent.sh
```

### Option 3: Start Individual Remote Agents

```bash
# DAG Troubleshooter
adk api_server --a2a --port 8001 vayu_agent/remote_agents/dag_troubleshooter

# Airflow Metadata
adk api_server --a2a --port 8002 vayu_agent/remote_agents/airflow_metadata

# Pipeline Mechanic
adk api_server --a2a --port 8003 vayu_agent/remote_agents/pipeline_mechanic

# Main Orchestrator
adk web vayu_agent
```

### Option 4: Docker Compose

```bash
# Set environment variables
export GIT_PAT_TOKEN=your_github_token
export DAG_REPOSITORY=your-org/your-repo
export AIRFLOW_API_URL=your_airflow_api_url

# Start with Docker Compose
docker-compose up
```

## 📡 Endpoints

- **Main Orchestrator**: http://localhost:8000
- **DAG Troubleshooter**: http://localhost:8001
- **Airflow Metadata**: http://localhost:8002
- **Pipeline Mechanic**: http://localhost:8003

## 💡 Usage Examples

### DAG Troubleshooting
```
"My DAG is failing with import errors" → Delegates to DagTroubleShooterAgent
"Why isn't my DAG running?" → Delegates to DagTroubleShooterAgent
"Debug the python_task in sample_dag run" → Delegates to DagTroubleShooterAgent
```

### Metadata Retrieval
```
"Show me details of the data_pipeline_etl DAG" → Delegates to AirflowMetadataAgent
"List all active DAGs" → Delegates to AirflowMetadataAgent
"Show me task instances for DAG run X" → Delegates to AirflowMetadataAgent
```

### Version Control
```
"Create a PR for my DAG changes" → Delegates to PipelineMechanicAgent
"Update repository with current DAG" → Delegates to PipelineMechanicAgent
"Version control for DAG files" → Delegates to PipelineMechanicAgent
```

## 🔄 A2A Protocol Benefits

1. **True Decoupling**: Remote agents run as independent services
2. **Scalability**: Each agent can be scaled independently
3. **Fault Tolerance**: If one agent fails, others continue to work
4. **Network Distribution**: Agents can run on different machines
5. **Service Discovery**: Easy to add/remove agents dynamically
6. **Load Balancing**: Multiple instances of the same agent type

## 🛠️ Development

### Adding a New Remote Agent

1. Create a new folder in `vayu_agent/remote_agents/`
2. Implement the agent with `agent.py`
3. Create `agent.json` with metadata
4. Add RemoteA2AAgent to `vayu_agent/orchestrator.py`
5. Update Docker Compose if needed

### Modifying Existing Agents

1. Edit the agent's `agent.py` file
2. Update `agent.json` if capabilities change
3. Restart the specific agent
4. The orchestrator will automatically use the updated agent

## 🔍 Monitoring

Each agent exposes health endpoints and can be monitored independently. The main orchestrator provides a unified interface while delegating to the appropriate specialized remote agents.

## 📚 Documentation

- [Google ADK A2A Documentation](https://google.github.io/adk-docs/a2a/quickstart-consuming/)
- [Agent-to-Agent Protocol](https://google.github.io/adk-docs/a2a/)
- [ADK A2A Sample](https://github.com/google/adk-python/tree/main/contributing/samples/a2a_basic)

## 🎯 Key Differences from Previous Version

1. **True A2A Protocol**: Uses `RemoteA2aAgent` for communication
2. **Service Architecture**: Each agent runs as an independent service using `adk api_server --a2a`
3. **Network Communication**: Agents communicate over HTTP using A2A protocol
4. **Scalability**: Can run agents on different machines
5. **Official Structure**: Follows Google ADK A2A sample patterns
6. **Agent Cards**: Uses JSON agent cards for remote agent configuration
7. **ADK Native**: Uses `adk web` and `adk api_server` commands instead of uvicorn
