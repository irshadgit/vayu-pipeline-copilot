from typing import Callable, Dict, Any, List, TypedDict

# Import tool handlers and schemas from modules
from tools.dag import (
    DAG_COLLECTION_SCHEMA,
    DAG_SCHEMA,
    DAG_RUN_COLLECTION_SCHEMA,
    DAG_SOURCE_SCHEMA,
    get_dags_tool,
    get_dag_tool,
    get_dag_runs_tool,
    get_dag_source_tool,
)
from tools.monitor import (
    HEALTH_SCHEMA,
    get_health,
)
from tools.task_instance import (
    TASK_INSTANCE_COLLECTION_SCHEMA,
    TASK_INSTANCE_SCHEMA,
    TASK_INSTANCE_TRIES_SCHEMA,
    TASK_INSTANCE_TRY_DETAILS_SCHEMA,
    TASK_INSTANCE_LOG_SCHEMA,
    list_task_instances_tool,
    get_task_instance_tool,
    get_task_instance_tries_tool,
    get_task_instance_try_details_tool,
    get_task_instance_log_tool,
)


class ToolSpec(TypedDict):
    name: str
    description: str
    output_schema: Dict[str, Any]
    handler: Callable[..., Any]


def get_all_tool_specs() -> List[ToolSpec]:
    return [
        {
            "name": "get_dags",
            "description": "Get all DAGs with optional filtering and pagination.",
            "output_schema": DAG_COLLECTION_SCHEMA,
            "handler": get_dags_tool,
        },
        {
            "name": "get_dag",
            "description": "Get a specific DAG by its dag_id.",
            "output_schema": DAG_SCHEMA,
            "handler": get_dag_tool,
        },
        {
            "name": "get_dag_runs",
            "description": "Get DAG runs for a specific DAG or all DAGs. Use '~' as dag_id to retrieve runs for all DAGs.",
            "output_schema": DAG_RUN_COLLECTION_SCHEMA,
            "handler": get_dag_runs_tool,
        },
        {
            "name": "get_dag_source",
            "description": "Get the source code of a DAG using its file token. The file_token is obtained from get_dag_details response file_token attribute.",
            "output_schema": DAG_SOURCE_SCHEMA,
            "handler": get_dag_source_tool,
        },
        {
            "name": "get_health",
            "description": "Get Airflow health (metadatabase, scheduler, triggerer, version) from /health. This will be called to check airflow health, status of components",
            "output_schema": HEALTH_SCHEMA,
            "handler": get_health,
        },
        {
            "name": "list_task_instances",
            "description": "List all task instances for a specific DAG run. Use this to monitor task status, analyze performance, debug failures, and get detailed execution information within a DAG run.",
            "output_schema": TASK_INSTANCE_COLLECTION_SCHEMA,
            "handler": list_task_instances_tool,
        },
        {
            "name": "get_task_instance",
            "description": "Get details of a specific task instance. Use this to debug individual tasks, analyze execution details, check status and configuration of a single task within a DAG run.",
            "output_schema": TASK_INSTANCE_SCHEMA,
            "handler": get_task_instance_tool,
        },
        {
            "name": "get_task_instance_tries",
            "description": "Get all tries for a specific task instance. Use this to analyze retry history, debug repeated failures, monitor execution attempts, and get detailed information about each retry attempt.",
            "output_schema": TASK_INSTANCE_TRIES_SCHEMA,
            "handler": get_task_instance_tries_tool,
        },
        {
            "name": "get_task_instance_try_details",
            "description": "Get detailed information about a specific try of a task instance. Use this to debug particular executions, analyze configuration, get logs, and investigate exact conditions of a specific attempt.",
            "output_schema": TASK_INSTANCE_TRY_DETAILS_SCHEMA,
            "handler": get_task_instance_try_details_tool,
        },
        {
            "name": "get_task_instance_log",
            "description": "Get logs for a specific task instance try. Use this to debug task failures, monitor execution progress, analyze error messages, and review task output and debugging information.",
            "output_schema": TASK_INSTANCE_LOG_SCHEMA,
            "handler": get_task_instance_log_tool,
        },
    ]


def register_all(mcp) -> None:
    for spec in get_all_tool_specs():
        mcp.tool(
            name=spec["name"],
            description=spec["description"],
            output_schema=spec["output_schema"],
        )(spec["handler"]) 


