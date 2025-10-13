#!/bin/bash
# Start Vayu Pipeline Copilot Complete System (A2A Architecture)

echo "🚁 Starting Vayu Pipeline Copilot Complete System (A2A Architecture)..."
echo "======================================================================"

# Set environment variables
export AIRFLOW_MCP_HOST=${AIRFLOW_MCP_HOST:-localhost}
export AIRFLOW_MCP_PORT=${AIRFLOW_MCP_PORT:-3000}
export GIT_PAT_TOKEN=${GIT_PAT_TOKEN}
export DAG_REPOSITORY=${DAG_REPOSITORY}
export A2A_HOST=${A2A_HOST:-localhost}
export A2A_PORT=${A2A_PORT:-8001}

echo "🔧 Starting A2A Host with All Remote Agents..."
echo "----------------------------------------------"

# Start A2A host with all remote agents in background
echo "Starting A2A Host on port $A2A_PORT with all remote agents..."
adk api_server --a2a --port $A2A_PORT vayu_agent/remote_agents &
A2A_HOST_PID=$!

# Wait a moment for A2A host to start
echo "⏳ Waiting for A2A host to initialize..."
sleep 5

echo ""
echo "✅ A2A Host started with all remote agents!"
echo "📡 A2A Host Endpoint: http://$A2A_HOST:$A2A_PORT"
echo "📡 Remote Agent Endpoints:"
echo "   - DAG Troubleshooter: http://$A2A_HOST:$A2A_PORT/a2a/dag_troubleshooter"
echo "   - Airflow Metadata: http://$A2A_HOST:$A2A_PORT/a2a/airflow_metadata"
echo "   - Pipeline Mechanic: http://$A2A_HOST:$A2A_PORT/a2a/pipeline_mechanic"
echo ""

echo "🚀 Starting Main Orchestrator Agent..."
echo "-------------------------------------"
echo "📡 Main Agent Endpoint: http://localhost:8000"
echo "💬 Ready to coordinate remote agents via A2A protocol!"
echo ""

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping all agents..."
    kill $A2A_HOST_PID 2>/dev/null
    echo "✅ All agents stopped successfully!"
    exit 0
}

# Set trap to cleanup on script exit
trap cleanup SIGINT SIGTERM

# Start the main orchestrator (this will block)
adk web vayu_agent
