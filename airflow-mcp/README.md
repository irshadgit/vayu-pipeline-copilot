# Airflow MCP Server 🚁

A Model Context Protocol (MCP) server for Apache Airflow that provides tools to interact with Airflow's REST API.

## Features

This MCP server provides the following tools with dummy data for testing:

### Available Tools

1. **get_dags** - Get all DAGs with filtering and pagination
   - Supports all parameters from the Airflow REST API
   - Parameters: `limit`, `offset`, `order_by`, `tags`, `only_active`, `paused`, `dag_id_pattern`

2. **get_dag** - Get a specific DAG by ID
   - Parameters: `dag_id`

3. **get_dag_details** - Get detailed DAG information including tasks
   - Parameters: `dag_id`

4. **get_variable** - Get Airflow variables by key
   - Parameters: `variable_key`

5. **health** - Health check endpoint

## Installation

1. Ensure you have Python 3.8+ installed
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Server

You can run the server in multiple ways:

#### Method 1: Using Docker (Recommended for Production)

**Build and run with Docker:**
```bash
# Build the Docker image
docker build -t airflow-mcp .

# Run the container
docker run -d \
  --name airflow-mcp-server \
  -p 3000:3000 \
  -e MCP_TRANSPORT=sse \
  -e MCP_HOST=0.0.0.0 \
  -e MCP_PORT=3000 \
  -e LOG_LEVEL=info \
  airflow-mcp
```

**Using Docker Compose:**
```bash
# Start both MCP server and inspector services
docker-compose up -d

# View logs for all services
docker-compose logs -f

# View logs for specific service
docker-compose logs -f airflow-mcp
docker-compose logs -f mcp-inspector

# Stop all services
docker-compose down
```

The Docker Compose setup includes:
- **Airflow MCP Server** on port `3000`
- **MCP Inspector** on ports `6274` (web interface) and `6277` (proxy server)

Access the MCP Inspector web interface at: `http://localhost:6274`

Note: The MCP Inspector runs with default configuration and will be accessible once both services are running. The inspector uses authentication tokens for security.

#### Method 2: Using the startup script
```bash
python run_server.py
```

#### Method 3: Direct execution
```bash
python server.py
```

#### Method 4: With custom environment variables
```bash
export MCP_TRANSPORT=sse
export MCP_HOST=0.0.0.0
export MCP_PORT=3000
export LOG_LEVEL=info
python server.py
```

### Environment Variables

- `MCP_TRANSPORT`: Transport protocol (default: "sse")
- `MCP_HOST`: Host to bind to (default: "0.0.0.0")
- `MCP_PORT`: Port to listen on (default: "3000")
- `LOG_LEVEL`: Logging level (default: "info")

## Testing with MCP Inspector

The [MCP Inspector](https://modelcontextprotocol.io/docs/tools/inspector) is an interactive developer tool for testing and debugging MCP servers. Follow these steps to test your Airflow MCP server:

### Prerequisites: Install Node.js with nvm

First, you need Node.js installed. We recommend using [nvm (Node Version Manager)](https://heynode.com/tutorial/install-nodejs-locally-nvm/) to manage Node.js versions:

#### 1. Install nvm

**For Linux/macOS:**
```bash
# Download and install nvm
curl -sL https://raw.githubusercontent.com/nvm-sh/nvm/v0.35.0/install.sh -o install_nvm.sh
bash install_nvm.sh

# Restart your terminal or source your profile
source ~/.bash_profile  # or ~/.zshrc depending on your shell

# Verify installation
command -v nvm
```

**For Windows:**
Use the [Windows-specific version of nvm](https://github.com/coreybutler/nvm-windows).

#### 2. Install Node.js

```bash
# Install the latest LTS version of Node.js
nvm install --lts

# Verify installation
node --version
npm --version
```

### Using MCP Inspector

#### 1. Start your MCP server
First, make sure your Airflow MCP server is running:

```bash
python run_server.py
```

#### 2. Launch MCP Inspector
In a new terminal, run the MCP Inspector to test your server:

```bash
npx @modelcontextprotocol/inspector python /path/to/your/airflow-mcp/server.py
```

Or if you're in the project directory:

```bash
npx @modelcontextprotocol/inspector python server.py
```

#### 3. Test the Tools
The MCP Inspector provides a web interface where you can:

- **View Resources**: Check available resources and their metadata
- **Test Tools**: Execute tools with custom parameters
- **View Prompts**: Test any available prompt templates
- **Monitor Logs**: See real-time server logs and notifications

### Manual Testing Examples

If you prefer to test manually, here are examples of tool calls:

#### Get all DAGs
```json
{
  "tool": "get_dags",
  "parameters": {
    "limit": 10,
    "only_active": true
  }
}
```

#### Get specific DAG
```json
{
  "tool": "get_dag",
  "parameters": {
    "dag_id": "example_python_operator"
  }
}
```

#### Get DAG details
```json
{
  "tool": "get_dag_details",
  "parameters": {
    "dag_id": "data_pipeline_etl"
  }
}
```

#### Get variable
```json
{
  "tool": "get_variable",
  "parameters": {
    "variable_key": "email_config"
  }
}
```

#### Health check
```json
{
  "tool": "health",
  "parameters": {}
}
```

### Inspector Features

The MCP Inspector provides several useful features for development:

- **Interactive Testing**: Test tools with custom inputs through a web interface
- **Real-time Logs**: Monitor server logs and debug issues
- **Schema Validation**: Verify tool schemas and parameters
- **Error Handling**: Test edge cases and error responses
- **Resource Inspection**: View available resources and their content

## Dummy Data

The server includes comprehensive dummy data for testing:

### DAGs
- `example_python_operator` - Basic Python operator example
- `data_pipeline_etl` - ETL pipeline with multiple tasks
- `ml_training_pipeline` - ML training pipeline (paused)

### Variables
- `email_config` - Email configuration JSON
- `database_connection_timeout` - Database timeout setting
- `data_retention_days` - Data retention policy
- `ml_model_version` - Current ML model version
- `api_endpoints` - External API endpoints JSON

## Next Steps

To connect this MCP server to a real Airflow instance:

1. Install the Airflow Python SDK
2. Replace dummy data with actual Airflow REST API calls
3. Add authentication and connection configuration
4. Implement error handling for real API responses

## Docker Deployment

For deployment in a larger system, you can use the provided Docker files:

### For Top-Level Repository Integration

If you want to include this MCP server in a larger docker-compose setup at the repository root, you can reference the services like this:

```yaml
# In your top-level docker-compose.yml
version: '3.8'

services:
  airflow-mcp:
    build:
      context: ./airflow-mcp
      dockerfile: Dockerfile
    container_name: airflow-mcp-server
    ports:
      - "3000:3000"
    environment:
      - MCP_TRANSPORT=sse
      - MCP_HOST=0.0.0.0
      - MCP_PORT=3000
      - LOG_LEVEL=info
    restart: unless-stopped
    networks:
      - your-network

  mcp-inspector:
    image: node:18-alpine
    container_name: mcp-inspector
    ports:
      - "6274:6274"  # MCP Inspector web interface
      - "6277:6277"  # MCP Inspector proxy server
    working_dir: /app
    command: >
      sh -c "
        npm install -g @modelcontextprotocol/inspector &&
        npx @modelcontextprotocol/inspector
      "
    restart: unless-stopped
    depends_on:
      - airflow-mcp
    networks:
      - your-network

  # Your other services...

networks:
  your-network:
    driver: bridge
```

## File Structure

```
airflow-mcp/
├── server.py                    # Main MCP server implementation
├── run_server.py               # Startup script
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Docker image definition
├── .dockerignore              # Docker ignore file
├── docker-compose.example.yml # Example Docker Compose configuration
└── README.md                  # This file
```

## Contributing

Feel free to extend this server with additional Airflow REST API endpoints and functionality.
