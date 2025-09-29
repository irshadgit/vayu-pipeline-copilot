#!/usr/bin/env python3
"""
Startup script for the Vayu Airflow Management Agent
"""
import os
import sys
from pathlib import Path

# Add the vayu_agent package to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from vayu_agent.agent import airflow_agent

def main():
    """Main entry point for the agent"""
    print("🚀 Starting Vayu Airflow Management Agent...")
    
    # Check if MCP server is expected to be running
    mcp_host = os.getenv("MCP_HOST", "localhost")
    mcp_port = os.getenv("MCP_PORT", "3000")
    
    print(f"📡 Expecting MCP server at {mcp_host}:{mcp_port}")
    print("💡 Make sure the Airflow MCP server is running before using the agent")
    print("   You can start it with: cd ../airflow-mcp && python server.py")
    print()
    
    # The agent is now ready to be used
    print("✅ Agent initialized and ready!")
    print("🔧 Available capabilities:")
    print("   - List and filter DAGs")
    print("   - Get DAG details and task information") 
    print("   - Retrieve Airflow variables")
    print("   - Health check the Airflow system")
    print()
    print("📝 Example usage:")
    print("   agent.run('Show me all active DAGs')")
    print("   agent.run('Get details for the data_pipeline_etl DAG')")
    print("   agent.run('What variables are configured?')")
    
    return airflow_agent

if __name__ == "__main__":
    agent = main()
    
    # Keep the script running for interactive use
    print("\n🎯 Agent is ready! You can now interact with it.")
    print("Press Ctrl+C to exit.")
    
    try:
        # Simple interactive loop
        while True:
            user_input = input("\n💬 Ask me about your Airflow setup: ")
            if user_input.lower() in ['quit', 'exit', 'bye']:
                break
            
            try:
                response = agent.run(user_input)
                print(f"\n🤖 {response}")
            except Exception as e:
                print(f"\n❌ Error: {e}")
                print("💡 Make sure the MCP server is running at ../airflow-mcp/server.py")
                
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
