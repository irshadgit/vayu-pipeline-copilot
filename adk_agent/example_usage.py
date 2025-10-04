#!/usr/bin/env python3
"""
Simple Example Usage of Airflow Copilot Multi-Agent System

This example demonstrates how to use the clean ADK hierarchy-based
multi-agent system for Airflow management.
"""

import sys
import os
from pathlib import Path

# Add the vayu_agent package to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from vayu_agent.agent import (
    root_agent,                    # Main orchestrator agent
    dag_troubleshooter_agent,      # Direct access to troubleshooter
    airflow_metadata_agent         # Direct access to metadata agent
)

def main():
    """Demonstrate the multi-agent system usage."""
    print("🚁 Airflow Copilot Multi-Agent System Example")
    print("=" * 50)
    
    # Check MCP server connection
    mcp_host = os.getenv("MCP_HOST", "localhost")
    mcp_port = os.getenv("MCP_PORT", "3000")
    print(f"📡 MCP Server: {mcp_host}:{mcp_port}")
    print("💡 Make sure the Airflow MCP server is running")
    print()
    
    # Example 1: Using the orchestrator (recommended approach)
    print("🎯 Example 1: Using the Orchestrator Agent")
    print("-" * 30)
    print("The orchestrator automatically delegates to the right sub-agent:")
    print()
    
    example_queries = [
        "Show me all active DAGs",
        "My data_pipeline_etl DAG is failing with import errors",
        "Get details of the ml_training_pipeline DAG",
        "Why isn't my DAG running as expected?"
    ]
    
    for query in example_queries:
        print(f"Query: '{query}'")
        print("→ Orchestrator will delegate to appropriate sub-agent")
        print()
    
    # Example 2: Direct sub-agent access
    print("🔧 Example 2: Direct Sub-Agent Access")
    print("-" * 30)
    print("For advanced users who want to bypass orchestration:")
    print()
    
    print("DagTroubleShooterAgent - for troubleshooting:")
    print("  dag_troubleshooter_agent.run('Analyze performance issues in my DAG')")
    print()
    
    print("AirflowMetadataAgent - for information retrieval:")
    print("  airflow_metadata_agent.run('List all DAGs with production tag')")
    print()
    
    # Example 3: Agent hierarchy information
    print("🏗️  Example 3: Agent Hierarchy")
    print("-" * 30)
    print("ADK automatically manages the parent-child relationships:")
    print()
    print("AirflowOrchestratorAgent (Parent)")
    print("├── DagTroubleShooterAgent (Sub-agent)")
    print("└── AirflowMetadataAgent (Sub-agent)")
    print()
    
    # Show sub-agent relationships
    if root_agent.sub_agents:
        print("✅ Sub-agents properly configured:")
        for sub_agent in root_agent.sub_agents:
            print(f"   - {sub_agent.name}")
            print(f"     Parent: {sub_agent.parent_agent.name if sub_agent.parent_agent else 'None'}")
    else:
        print("❌ No sub-agents found")
    
    print()
    print("🚀 Ready to use! Try running queries with root_agent.run('your query')")

if __name__ == "__main__":
    main()

