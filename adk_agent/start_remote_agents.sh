#!/bin/bash
# Start Vayu Pipeline Copilot Remote Agents using ADK API Server

echo "🚁 Starting Vayu Pipeline Copilot Remote Agents (A2A Architecture)..."
echo "=================================================================="

# Set environment variables
export AIRFLOW_MCP_HOST=${AIRFLOW_MCP_HOST:-localhost}
export AIRFLOW_MCP_PORT=${AIRFLOW_MCP_PORT:-3000}
export GITHUB_MCP_HOST=${GITHUB_MCP_HOST:-localhost}
export GITHUB_MCP_PORT=${GITHUB_MCP_PORT:-3001}
export GIT_PAT_TOKEN=${GIT_PAT_TOKEN}
export DAG_REPOSITORY=${DAG_REPOSITORY}

echo "🔧 Starting DAG Troubleshooter Remote Agent on port 8001..."
adk api_server --a2a --port 8001 vayu_agent/remote_agents/dag_troubleshooter &
DAG_TROUBLESHOOTER_PID=$!

echo "📊 Starting Airflow Metadata Remote Agent on port 8002..."
adk api_server --a2a --port 8002 vayu_agent/remote_agents/airflow_metadata &
AIRFLOW_METADATA_PID=$!

echo "🔧 Starting Pipeline Mechanic Remote Agent on port 8003..."
adk api_server --a2a --port 8003 vayu_agent/remote_agents/pipeline_mechanic &
PIPELINE_MECHANIC_PID=$!

echo ""
echo "✅ All remote agents started!"
echo "📡 Endpoints:"
echo "   - DAG Troubleshooter: http://localhost:8001"
echo "   - Airflow Metadata: http://localhost:8002"
echo "   - Pipeline Mechanic: http://localhost:8003"
echo ""
echo "🎯 Next step: Run 'adk web vayu_agent' in another terminal to start the main orchestrator"
echo ""
echo "🛑 Press Ctrl+C to stop all agents"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping all remote agents..."
    kill $DAG_TROUBLESHOOTER_PID 2>/dev/null
    kill $AIRFLOW_METADATA_PID 2>/dev/null
    kill $PIPELINE_MECHANIC_PID 2>/dev/null
    echo "✅ All agents stopped successfully!"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Wait for all background processes
wait
