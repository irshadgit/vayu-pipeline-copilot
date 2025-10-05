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
    TASK_INSTANCE_REFERENCE_COLLECTION_SCHEMA,
    list_task_instances_tool,
    get_task_instance_tool,
    get_task_instance_tries_tool,
    get_task_instance_try_details_tool,
    get_task_instance_log_tool,
    clear_task_instances_tool,
)
from tools.connection import (
    CONNECTION_COLLECTION_SCHEMA,
    CONNECTION_SCHEMA,
    get_connections_tool,
    get_connection_tool,
    create_connection_tool,
    update_connection_tool,
    delete_connection_tool,
    test_connection_tool,
)
from tools.config import (
    CONFIG_COLLECTION_SCHEMA,
    CONFIG_SCHEMA,
    get_configs_tool,
    get_config_tool,
)
from tools.variable import (
    VARIABLE_COLLECTION_SCHEMA,
    VARIABLE_SCHEMA,
    get_variables_tool,
    get_variable_tool,
    create_variable_tool,
    update_variable_tool,
    delete_variable_tool,
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
        {
            "name": "clear_task_instances",
            "description": "Clear a set of task instances associated with the DAG for a specified date range. Use this to recover from failures, retry tasks, reset task states, clear stuck tasks, and perform dry runs to see what would be cleared.",
            "output_schema": TASK_INSTANCE_REFERENCE_COLLECTION_SCHEMA,
            "handler": clear_task_instances_tool,
        },
        {
            "name": "get_connections",
            "description": "Get all connections with optional filtering and pagination. Use this to list available connections, check connection types, and get overview of connection configuration.",
            "output_schema": CONNECTION_COLLECTION_SCHEMA,
            "handler": get_connections_tool,
        },
        {
            "name": "get_connection",
            "description": "Get details of a specific connection by its connection_id. Use this to check connection configuration, debug connection issues, and verify connection settings.",
            "output_schema": CONNECTION_SCHEMA,
            "handler": get_connection_tool,
        },
        {
            "name": "create_connection",
            "description": "Create a new connection in Airflow. Use this to set up database connections, API connections, cloud storage connections, and configure authentication for external systems.",
            "output_schema": CONNECTION_SCHEMA,
            "handler": create_connection_tool,
        },
        {
            "name": "update_connection",
            "description": "Update an existing connection in Airflow. Use this to modify connection credentials, update parameters, change connection type, and fix connection configuration issues.",
            "output_schema": CONNECTION_SCHEMA,
            "handler": update_connection_tool,
        },
        {
            "name": "delete_connection",
            "description": "Delete a connection from Airflow. Use this to remove unused connections, clean up configurations, and delete obsolete connections.",
            "output_schema": CONNECTION_SCHEMA,
            "handler": delete_connection_tool,
        },
        {
            "name": "test_connection",
            "description": "Test a connection to verify it's working correctly. Use this to validate connection configuration, test connectivity, debug issues, and ensure connections work before using in DAGs.",
            "output_schema": CONNECTION_SCHEMA,
            "handler": test_connection_tool,
        },
        {
            "name": "get_configs",
            "description": "Get all configuration settings in Airflow. Use this to list available configuration settings, check current values, and get overview of Airflow system configuration.",
            "output_schema": CONFIG_COLLECTION_SCHEMA,
            "handler": get_configs_tool,
        },
        {
            "name": "get_config",
            "description": "Get a specific configuration value by section and option. Use this to check specific configuration values and debug configuration issues.",
            "output_schema": CONFIG_SCHEMA,
            "handler": get_config_tool,
        },
        {
            "name": "get_variables",
            "description": "Get all variables with optional filtering and pagination. Use this to list available variables, check variable types, and get overview of variable configuration.",
            "output_schema": VARIABLE_COLLECTION_SCHEMA,
            "handler": get_variables_tool,
        },
        {
            "name": "get_variable",
            "description": "Get details of a specific variable by its key. Use this to check variable configuration, debug variable issues, and verify variable settings.",
            "output_schema": VARIABLE_SCHEMA,
            "handler": get_variable_tool,
        },
        {
            "name": "create_variable",
            "description": "Create a new variable in Airflow. Use this to set up configuration variables, store secrets, create environment-specific values, and configure variables programmatically.",
            "output_schema": VARIABLE_SCHEMA,
            "handler": create_variable_tool,
        },
        {
            "name": "update_variable",
            "description": "Update an existing variable in Airflow. Use this to modify variable values, update descriptions, change configuration, and fix variable configuration issues.",
            "output_schema": VARIABLE_SCHEMA,
            "handler": update_variable_tool,
        },
        {
            "name": "delete_variable",
            "description": "Delete a variable from Airflow. Use this to remove unused variables, clean up configurations, and delete obsolete variables.",
            "output_schema": VARIABLE_SCHEMA,
            "handler": delete_variable_tool,
        },
    ]


def register_all(mcp) -> None:
    for spec in get_all_tool_specs():
        mcp.tool(
            name=spec["name"],
            description=spec["description"],
            output_schema=spec["output_schema"],
        )(spec["handler"]) 


