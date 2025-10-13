#!/bin/bash
# Start Vayu Pipeline Copilot Main Orchestrator Agent using ADK Web Server

echo "🚁 Starting Vayu Pipeline Copilot Main Orchestrator Agent..."
echo "============================================================="

# Set environment variables
export DAG_TROUBLESHOOTER_ENDPOINT=${DAG_TROUBLESHOOTER_ENDPOINT:-http://localhost:8001}
export AIRFLOW_METADATA_ENDPOINT=${AIRFLOW_METADATA_ENDPOINT:-http://localhost:8002}
export PIPELINE_MECHANIC_ENDPOINT=${PIPELINE_MECHANIC_ENDPOINT:-http://localhost:8003}

echo "📡 Remote Agent Endpoints:"
echo "   - DAG Troubleshooter: $DAG_TROUBLESHOOTER_ENDPOINT"
echo "   - Airflow Metadata: $AIRFLOW_METADATA_ENDPOINT"
echo "   - Pipeline Mechanic: $PIPELINE_MECHANIC_ENDPOINT"
echo ""

# Start the main orchestrator using ADK web server
echo "🚀 Starting main orchestrator agent..."
adk web vayu_agent
