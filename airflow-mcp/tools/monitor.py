from typing import Dict, Any
from schema import load_schema, http_utils


HEALTH_SCHEMA = load_schema("monitor/health")


async def get_health() -> Dict[str, Any]:
    """
    Fetch Airflow health information from /health. 
    Get the status of Airflow's metadatabase, triggerer and scheduler. It includes info about metadatabase and last heartbeat of scheduler and triggerer.
    Use this tool to check the health and status of Airflow components.
    Returns:
        JSON response containing Airflow health information
    """
    endpoint = "health"
    response = http_utils.get_json_response(endpoint)
    return response


