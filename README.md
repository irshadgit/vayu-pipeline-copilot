# Vayu: The Copilot for Your Data Pipelines 🚀
A conversational AI assistant for interacting with workflow orchestration tools. Currently supporting Apache Airflow, Vayu helps you manage and interact with your data pipelines through natural language conversations.

## Architecture

![Architecture Diagram](docs/vayu-architecture.png)
* Agent Development Kit (ADK) - AI agent framework for building conversational agents
* FastMCP-based Airflow MCP Server - Local implementation for Airflow integration
* Apache Airflow - https://airflow.apache.org/
* Model Context Protocol (MCP) - https://modelcontextprotocol.io/

## Project Structure

```
├── adk_agent/ # ADK (Agent Development Kit) application module for Copilot
│ ├── vayu_agent/ # Source code for the Vayu agent
│ │ ├── tools/ # MCP tool integrations
│ │ ├── prompts/ # Agent prompt templates
│ │ └── models/ # Data models and schemas
│ ├── requirements.txt # Python dependencies
│ ├── Dockerfile # Docker setup for containerizing the agent
│ └── README.md # Agent-specific documentation
├── airflow-mcp/ # FastMCP-based Airflow MCP server
│ ├── server.py # MCP server implementation
│ ├── requirements.txt # Server dependencies
│ ├── Dockerfile # Docker setup for MCP server
│ └── README.md # MCP server documentation
├── airflow_home/ # Airflow configuration and DAGs
│ ├── dags/ # Airflow DAG definitions
│ ├── plugins/ # Airflow plugins
│ └── logs/ # Airflow logs
├── docs/ # Project documentation & demo videos
├── docker-compose.yml # Multi-service Docker Compose setup
└── README.md # Project overview and usage guide
```


## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed:
- Docker and Docker Desktop
- Docker Compose
- Git client

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/irshadgit/vayu-pipeline-copilot.git
   cd vayu-pipeline-copilot
   ```

2. Configure the LLM:
   - Create a `.env` file in the root directory:
     ```bash
     cp .env.example .env
     ```
   - Add your Google AI API key:
     ```
     GOOGLE_API_KEY=your_api_key_here
     ```
   - The project uses Google's Gemini 2.0 Flash by default. You can change the LLM by modifying the ADK agent configuration.
   - To use a different LLM:
     1. Add the required provider package to `adk_agent/requirements.txt`. For example:
        - For OpenAI: `openai`
        - For Anthropic: `anthropic`
        - For Azure OpenAI: `azure-openai`
     2. Update the ADK agent configuration in the agent code or environment variables:
        ```
        # For OpenAI
        OPENAI_API_KEY=your_openai_key_here
        
        # For Anthropic
        ANTHROPIC_API_KEY=your_anthropic_key_here
        ```
     Note: Ensure the selected LLM supports tool calling functionality. The ADK framework supports multiple LLM providers through its extensible architecture.

3. Start the services using Docker Compose with build:
   ```bash
   # Build and start all services
   docker-compose up --build -d
   
   # Or if you want to see the logs in real-time
   docker-compose up --build
   ```
   
   The `--build` flag ensures that Docker builds the local images for:
   - `adk_agent` - Builds the ADK-based Vayu agent
   - `airflow-mcp-server` - Builds the FastMCP-based Airflow server

4. Wait for all services to be running (this may take a few minutes on first run).

5. Make sure services are accessible:
   - ADK Agent Server: http://localhost:8005
   - Airflow Web UI: http://localhost:8080 - Login with username: airflow & password: airflow
   - Airflow MCP Server: http://localhost:3000

### Connecting to the Agent

You can interact with the ADK-based Vayu agent through the web interface:

1. Open your browser and navigate to: http://localhost:8005
2. The ADK web interface will load, providing you with a chat interface
3. Start conversing with Vayu about your Airflow pipelines