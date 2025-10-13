"""
Vayu Pipeline Copilot - Main Entry Point
Starts the orchestrator agent with A2A protocol
"""

from orchestrator import vayu_orchestrator

if __name__ == "__main__":
    print("🚁 Vayu Pipeline Copilot Orchestrator Agent Initialized!")
    print("📡 Main Agent Endpoint: http://localhost:8000")
    print("💬 Ready to coordinate remote agents!")
    print("🚀 Use 'adk web vayu_agent' to start the web server")
    print("\n🏗️  Agent Hierarchy (A2A):")
    print("   VayuPipelineCopilotAgent (Root)")
    print("   ├── DagTroubleShooterAgent (RemoteA2A) - http://localhost:8001")
    print("   ├── AirflowMetadataAgent (RemoteA2A) - http://localhost:8002")
    print("   └── PipelineMechanicAgent (RemoteA2A) - http://localhost:8003")
