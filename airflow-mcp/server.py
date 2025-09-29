from fastmcp import FastMCP
import os
import json
from pathlib import Path
from typing import Optional, List
from datetime import datetime

transport = os.getenv("MCP_TRANSPORT", "sse")
mcp_host = os.getenv("MCP_HOST", "0.0.0.0")
mcp_port = int(os.getenv("MCP_PORT", "3000"))
log_level = os.getenv("LOG_LEVEL", "info").lower()

mcp = FastMCP("airflow-mcp-server 🚁")

# Register TOOLS using FastMCP 2.x decorators
@mcp.tool("get_dags")
async def get_dags_tool(
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    tags: Optional[List[str]] = None,
    only_active: bool = True,
    paused: Optional[bool] = None,
    dag_id_pattern: Optional[str] = None
) -> str:
    """
    Get all DAGs with optional filtering and pagination.
    
    Args:
        limit: The numbers of items to return (default: 100, max: 100)
        offset: The number of items to skip before starting to collect the result set (default: 0)
        order_by: The name of the field to order the results by. Prefix a field name with `-` to reverse the sort order
        tags: List of tags to filter DAGs by
        only_active: Only filter active DAGs (default: True)
        paused: Only filter paused/unpaused DAGs
        dag_id_pattern: If set, only return DAGs with dag_ids matching this pattern
    
    Returns:
        JSON response containing list of DAGs with their basic information
    """
    # Dummy response data
    dummy_dags = [
        {
            "dag_id": "example_python_operator",
            "root_dag_id": None,
            "is_paused": False,
            "is_active": True,
            "is_subdag": False,
            "last_parsed_time": "2024-01-15T10:30:00Z",
            "last_pickled": None,
            "last_expired": None,
            "scheduler_lock": None,
            "pickle_id": None,
            "default_view": "graph",
            "fileloc": "/opt/airflow/dags/example_python_operator.py",
            "file_token": "abc123",
            "owners": ["airflow"],
            "description": "Example DAG demonstrating Python operators",
            "schedule_interval": {"__type": "TimeDelta", "days": 1, "seconds": 0, "microseconds": 0},
            "timetable_description": "At 00:00",
            "tags": ["example", "tutorial"],
            "max_active_tasks": 16,
            "max_active_runs": 16,
            "has_task_concurrency_limits": False,
            "has_import_errors": False,
            "next_dagrun": "2024-01-16T00:00:00Z",
            "next_dagrun_data_interval_start": "2024-01-15T00:00:00Z",
            "next_dagrun_data_interval_end": "2024-01-16T00:00:00Z",
            "next_dagrun_create_after": "2024-01-16T00:00:00Z"
        },
        {
            "dag_id": "data_pipeline_etl",
            "root_dag_id": None,
            "is_paused": False,
            "is_active": True,
            "is_subdag": False,
            "last_parsed_time": "2024-01-15T09:45:00Z",
            "last_pickled": None,
            "last_expired": None,
            "scheduler_lock": None,
            "pickle_id": None,
            "default_view": "graph",
            "fileloc": "/opt/airflow/dags/data_pipeline_etl.py",
            "file_token": "def456",
            "owners": ["data-team"],
            "description": "ETL pipeline for processing customer data",
            "schedule_interval": {"__type": "CronExpression", "value": "0 2 * * *"},
            "timetable_description": "At 02:00",
            "tags": ["etl", "production"],
            "max_active_tasks": 8,
            "max_active_runs": 1,
            "has_task_concurrency_limits": True,
            "has_import_errors": False,
            "next_dagrun": "2024-01-16T02:00:00Z",
            "next_dagrun_data_interval_start": "2024-01-15T02:00:00Z",
            "next_dagrun_data_interval_end": "2024-01-16T02:00:00Z",
            "next_dagrun_create_after": "2024-01-16T02:00:00Z"
        },
        {
            "dag_id": "ml_training_pipeline",
            "root_dag_id": None,
            "is_paused": True,
            "is_active": True,
            "is_subdag": False,
            "last_parsed_time": "2024-01-15T08:20:00Z",
            "last_pickled": None,
            "last_expired": None,
            "scheduler_lock": None,
            "pickle_id": None,
            "default_view": "graph",
            "fileloc": "/opt/airflow/dags/ml_training_pipeline.py",
            "file_token": "ghi789",
            "owners": ["ml-team"],
            "description": "Machine learning model training pipeline",
            "schedule_interval": {"__type": "CronExpression", "value": "0 6 * * 0"},
            "timetable_description": "At 06:00 on Sunday",
            "tags": ["ml", "training", "weekly"],
            "max_active_tasks": 4,
            "max_active_runs": 1,
            "has_task_concurrency_limits": True,
            "has_import_errors": False,
            "next_dagrun": None,
            "next_dagrun_data_interval_start": None,
            "next_dagrun_data_interval_end": None,
            "next_dagrun_create_after": None
        }
    ]
    
    # Apply filtering based on parameters
    filtered_dags = dummy_dags.copy()
    
    if paused is not None:
        filtered_dags = [dag for dag in filtered_dags if dag["is_paused"] == paused]
    
    if not only_active:
        # In real implementation, this would include inactive DAGs
        pass
    
    if dag_id_pattern:
        filtered_dags = [dag for dag in filtered_dags if dag_id_pattern in dag["dag_id"]]
    
    if tags:
        filtered_dags = [dag for dag in filtered_dags if any(tag in dag["tags"] for tag in tags)]
    
    # Apply pagination
    start_idx = offset
    end_idx = offset + limit
    paginated_dags = filtered_dags[start_idx:end_idx]
    
    response = {
        "dags": paginated_dags,
        "total_entries": len(filtered_dags)
    }
    
    return json.dumps(response, indent=2)

@mcp.tool("get_dag")
async def get_dag_tool(dag_id: str) -> str:
    """
    Get a specific DAG by its ID.
    
    Args:
        dag_id: The DAG ID to retrieve
    
    Returns:
        JSON response containing the DAG information
    """
    # Dummy response data for specific DAGs
    dummy_dag_data = {
        "example_python_operator": {
            "dag_id": "example_python_operator",
            "root_dag_id": None,
            "is_paused": False,
            "is_active": True,
            "is_subdag": False,
            "last_parsed_time": "2024-01-15T10:30:00Z",
            "last_pickled": None,
            "last_expired": None,
            "scheduler_lock": None,
            "pickle_id": None,
            "default_view": "graph",
            "fileloc": "/opt/airflow/dags/example_python_operator.py",
            "file_token": "abc123",
            "owners": ["airflow"],
            "description": "Example DAG demonstrating Python operators",
            "schedule_interval": {"__type": "TimeDelta", "days": 1, "seconds": 0, "microseconds": 0},
            "timetable_description": "At 00:00",
            "tags": ["example", "tutorial"],
            "max_active_tasks": 16,
            "max_active_runs": 16,
            "has_task_concurrency_limits": False,
            "has_import_errors": False,
            "next_dagrun": "2024-01-16T00:00:00Z",
            "next_dagrun_data_interval_start": "2024-01-15T00:00:00Z",
            "next_dagrun_data_interval_end": "2024-01-16T00:00:00Z",
            "next_dagrun_create_after": "2024-01-16T00:00:00Z",
            "catchup": True,
            "orientation": "LR",
            "doc_md": "# Example Python Operator DAG\n\nThis DAG demonstrates basic Python operators.",
            "start_date": "2024-01-01T00:00:00Z",
            "end_date": None,
            "is_paused_upon_creation": False,
            "max_consecutive_failed_dag_runs": 0,
            "render_template_as_native_obj": False
        },
        "data_pipeline_etl": {
            "dag_id": "data_pipeline_etl",
            "root_dag_id": None,
            "is_paused": False,
            "is_active": True,
            "is_subdag": False,
            "last_parsed_time": "2024-01-15T09:45:00Z",
            "last_pickled": None,
            "last_expired": None,
            "scheduler_lock": None,
            "pickle_id": None,
            "default_view": "graph",
            "fileloc": "/opt/airflow/dags/data_pipeline_etl.py",
            "file_token": "def456",
            "owners": ["data-team"],
            "description": "ETL pipeline for processing customer data",
            "schedule_interval": {"__type": "CronExpression", "value": "0 2 * * *"},
            "timetable_description": "At 02:00",
            "tags": ["etl", "production"],
            "max_active_tasks": 8,
            "max_active_runs": 1,
            "has_task_concurrency_limits": True,
            "has_import_errors": False,
            "next_dagrun": "2024-01-16T02:00:00Z",
            "next_dagrun_data_interval_start": "2024-01-15T02:00:00Z",
            "next_dagrun_data_interval_end": "2024-01-16T02:00:00Z",
            "next_dagrun_create_after": "2024-01-16T02:00:00Z",
            "catchup": False,
            "orientation": "TB",
            "doc_md": "# Data Pipeline ETL\n\nProcesses customer data from various sources.",
            "start_date": "2024-01-01T02:00:00Z",
            "end_date": None,
            "is_paused_upon_creation": False,
            "max_consecutive_failed_dag_runs": 3,
            "render_template_as_native_obj": True
        }
    }
    
    if dag_id in dummy_dag_data:
        return json.dumps(dummy_dag_data[dag_id], indent=2)
    else:
        error_response = {
            "detail": f"DAG with dag_id: '{dag_id}' not found",
            "status": 404,
            "title": "DAG not found",
            "type": "about:blank"
        }
        return json.dumps(error_response, indent=2)

@mcp.tool("get_dag_details")
async def get_dag_details_tool(dag_id: str) -> str:
    """
    Get detailed information about a specific DAG including tasks.
    
    Args:
        dag_id: The DAG ID to get details for
    
    Returns:
        JSON response containing detailed DAG information including tasks
    """
    # Dummy detailed DAG data with tasks
    dummy_dag_details = {
        "example_python_operator": {
            "dag_id": "example_python_operator",
            "root_dag_id": None,
            "is_paused": False,
            "is_active": True,
            "is_subdag": False,
            "last_parsed_time": "2024-01-15T10:30:00Z",
            "last_pickled": None,
            "last_expired": None,
            "scheduler_lock": None,
            "pickle_id": None,
            "default_view": "graph",
            "fileloc": "/opt/airflow/dags/example_python_operator.py",
            "file_token": "abc123",
            "owners": ["airflow"],
            "description": "Example DAG demonstrating Python operators",
            "schedule_interval": {"__type": "TimeDelta", "days": 1, "seconds": 0, "microseconds": 0},
            "timetable_description": "At 00:00",
            "tags": ["example", "tutorial"],
            "max_active_tasks": 16,
            "max_active_runs": 16,
            "has_task_concurrency_limits": False,
            "has_import_errors": False,
            "next_dagrun": "2024-01-16T00:00:00Z",
            "next_dagrun_data_interval_start": "2024-01-15T00:00:00Z",
            "next_dagrun_data_interval_end": "2024-01-16T00:00:00Z",
            "next_dagrun_create_after": "2024-01-16T00:00:00Z",
            "catchup": True,
            "orientation": "LR",
            "doc_md": "# Example Python Operator DAG\n\nThis DAG demonstrates basic Python operators.",
            "start_date": "2024-01-01T00:00:00Z",
            "end_date": None,
            "is_paused_upon_creation": False,
            "max_consecutive_failed_dag_runs": 0,
            "render_template_as_native_obj": False,
            "tasks": [
                {
                    "task_id": "print_date",
                    "owner": "airflow",
                    "start_date": "2024-01-01T00:00:00Z",
                    "end_date": None,
                    "trigger_rule": "all_success",
                    "depends_on_past": False,
                    "wait_for_downstream": False,
                    "retries": 1,
                    "queue": "default",
                    "pool": "default_pool",
                    "pool_slots": 1,
                    "execution_timeout": None,
                    "retry_delay": {"__type": "TimeDelta", "days": 0, "seconds": 300, "microseconds": 0},
                    "retry_exponential_backoff": False,
                    "priority_weight": 1,
                    "weight_rule": "downstream",
                    "ui_color": "#fff",
                    "ui_fgcolor": "#000",
                    "template_fields": [],
                    "sub_dag": None,
                    "downstream_task_ids": ["sleep"],
                    "class_ref": {
                        "class_name": "PythonOperator",
                        "module_path": "airflow.operators.python"
                    }
                },
                {
                    "task_id": "sleep",
                    "owner": "airflow",
                    "start_date": "2024-01-01T00:00:00Z",
                    "end_date": None,
                    "trigger_rule": "all_success",
                    "depends_on_past": False,
                    "wait_for_downstream": False,
                    "retries": 1,
                    "queue": "default",
                    "pool": "default_pool",
                    "pool_slots": 1,
                    "execution_timeout": None,
                    "retry_delay": {"__type": "TimeDelta", "days": 0, "seconds": 300, "microseconds": 0},
                    "retry_exponential_backoff": False,
                    "priority_weight": 1,
                    "weight_rule": "downstream",
                    "ui_color": "#fff",
                    "ui_fgcolor": "#000",
                    "template_fields": [],
                    "sub_dag": None,
                    "downstream_task_ids": ["templated"],
                    "class_ref": {
                        "class_name": "BashOperator",
                        "module_path": "airflow.operators.bash"
                    }
                },
                {
                    "task_id": "templated",
                    "owner": "airflow",
                    "start_date": "2024-01-01T00:00:00Z",
                    "end_date": None,
                    "trigger_rule": "all_success",
                    "depends_on_past": False,
                    "wait_for_downstream": False,
                    "retries": 1,
                    "queue": "default",
                    "pool": "default_pool",
                    "pool_slots": 1,
                    "execution_timeout": None,
                    "retry_delay": {"__type": "TimeDelta", "days": 0, "seconds": 300, "microseconds": 0},
                    "retry_exponential_backoff": False,
                    "priority_weight": 1,
                    "weight_rule": "downstream",
                    "ui_color": "#fff",
                    "ui_fgcolor": "#000",
                    "template_fields": ["bash_command"],
                    "sub_dag": None,
                    "downstream_task_ids": [],
                    "class_ref": {
                        "class_name": "BashOperator",
                        "module_path": "airflow.operators.bash"
                    }
                }
            ]
        },
        "data_pipeline_etl": {
            "dag_id": "data_pipeline_etl",
            "root_dag_id": None,
            "is_paused": False,
            "is_active": True,
            "is_subdag": False,
            "last_parsed_time": "2024-01-15T09:45:00Z",
            "last_pickled": None,
            "last_expired": None,
            "scheduler_lock": None,
            "pickle_id": None,
            "default_view": "graph",
            "fileloc": "/opt/airflow/dags/data_pipeline_etl.py",
            "file_token": "def456",
            "owners": ["data-team"],
            "description": "ETL pipeline for processing customer data",
            "schedule_interval": {"__type": "CronExpression", "value": "0 2 * * *"},
            "timetable_description": "At 02:00",
            "tags": ["etl", "production"],
            "max_active_tasks": 8,
            "max_active_runs": 1,
            "has_task_concurrency_limits": True,
            "has_import_errors": False,
            "next_dagrun": "2024-01-16T02:00:00Z",
            "next_dagrun_data_interval_start": "2024-01-15T02:00:00Z",
            "next_dagrun_data_interval_end": "2024-01-16T02:00:00Z",
            "next_dagrun_create_after": "2024-01-16T02:00:00Z",
            "catchup": False,
            "orientation": "TB",
            "doc_md": "# Data Pipeline ETL\n\nProcesses customer data from various sources.",
            "start_date": "2024-01-01T02:00:00Z",
            "end_date": None,
            "is_paused_upon_creation": False,
            "max_consecutive_failed_dag_runs": 3,
            "render_template_as_native_obj": True,
            "tasks": [
                {
                    "task_id": "extract_data",
                    "owner": "data-team",
                    "start_date": "2024-01-01T02:00:00Z",
                    "end_date": None,
                    "trigger_rule": "all_success",
                    "depends_on_past": False,
                    "wait_for_downstream": False,
                    "retries": 3,
                    "queue": "data_queue",
                    "pool": "data_pool",
                    "pool_slots": 2,
                    "execution_timeout": {"__type": "TimeDelta", "days": 0, "seconds": 3600, "microseconds": 0},
                    "retry_delay": {"__type": "TimeDelta", "days": 0, "seconds": 600, "microseconds": 0},
                    "retry_exponential_backoff": True,
                    "priority_weight": 10,
                    "weight_rule": "downstream",
                    "ui_color": "#90EE90",
                    "ui_fgcolor": "#000",
                    "template_fields": ["sql"],
                    "sub_dag": None,
                    "downstream_task_ids": ["transform_data"],
                    "class_ref": {
                        "class_name": "SqlOperator",
                        "module_path": "airflow.operators.sql"
                    }
                },
                {
                    "task_id": "transform_data",
                    "owner": "data-team",
                    "start_date": "2024-01-01T02:00:00Z",
                    "end_date": None,
                    "trigger_rule": "all_success",
                    "depends_on_past": False,
                    "wait_for_downstream": False,
                    "retries": 2,
                    "queue": "data_queue",
                    "pool": "data_pool",
                    "pool_slots": 1,
                    "execution_timeout": {"__type": "TimeDelta", "days": 0, "seconds": 1800, "microseconds": 0},
                    "retry_delay": {"__type": "TimeDelta", "days": 0, "seconds": 300, "microseconds": 0},
                    "retry_exponential_backoff": False,
                    "priority_weight": 5,
                    "weight_rule": "downstream",
                    "ui_color": "#87CEEB",
                    "ui_fgcolor": "#000",
                    "template_fields": ["python_callable"],
                    "sub_dag": None,
                    "downstream_task_ids": ["load_data"],
                    "class_ref": {
                        "class_name": "PythonOperator",
                        "module_path": "airflow.operators.python"
                    }
                },
                {
                    "task_id": "load_data",
                    "owner": "data-team",
                    "start_date": "2024-01-01T02:00:00Z",
                    "end_date": None,
                    "trigger_rule": "all_success",
                    "depends_on_past": False,
                    "wait_for_downstream": False,
                    "retries": 3,
                    "queue": "data_queue",
                    "pool": "data_pool",
                    "pool_slots": 1,
                    "execution_timeout": {"__type": "TimeDelta", "days": 0, "seconds": 2400, "microseconds": 0},
                    "retry_delay": {"__type": "TimeDelta", "days": 0, "seconds": 600, "microseconds": 0},
                    "retry_exponential_backoff": True,
                    "priority_weight": 1,
                    "weight_rule": "downstream",
                    "ui_color": "#FFA07A",
                    "ui_fgcolor": "#000",
                    "template_fields": ["sql"],
                    "sub_dag": None,
                    "downstream_task_ids": [],
                    "class_ref": {
                        "class_name": "SqlOperator",
                        "module_path": "airflow.operators.sql"
                    }
                }
            ]
        }
    }
    
    if dag_id in dummy_dag_details:
        return json.dumps(dummy_dag_details[dag_id], indent=2)
    else:
        error_response = {
            "detail": f"DAG with dag_id: '{dag_id}' not found",
            "status": 404,
            "title": "DAG not found",
            "type": "about:blank"
        }
        return json.dumps(error_response, indent=2)

@mcp.tool("get_variable")
async def get_variable_tool(variable_key: str) -> str:
    """
    Get an Airflow variable by key.
    
    Args:
        variable_key: The key of the variable to retrieve
    
    Returns:
        JSON response containing the variable information
    """
    # Dummy variable data
    dummy_variables = {
        "email_config": {
            "key": "email_config",
            "value": json.dumps({
                "smtp_host": "smtp.company.com",
                "smtp_port": 587,
                "default_sender": "airflow@company.com"
            }),
            "description": "Email configuration for notifications"
        },
        "database_connection_timeout": {
            "key": "database_connection_timeout",
            "value": "30",
            "description": "Database connection timeout in seconds"
        },
        "data_retention_days": {
            "key": "data_retention_days",
            "value": "90",
            "description": "Number of days to retain processed data"
        },
        "ml_model_version": {
            "key": "ml_model_version",
            "value": "v2.1.3",
            "description": "Current ML model version in production"
        },
        "api_endpoints": {
            "key": "api_endpoints",
            "value": json.dumps({
                "customer_service": "https://api.company.com/customers",
                "payment_service": "https://api.company.com/payments",
                "notification_service": "https://api.company.com/notifications"
            }),
            "description": "External API endpoints configuration"
        }
    }
    
    if variable_key in dummy_variables:
        return json.dumps(dummy_variables[variable_key], indent=2)
    else:
        error_response = {
            "detail": f"Variable with key '{variable_key}' not found",
            "status": 404,
            "title": "Variable not found",
            "type": "about:blank"
        }
        return json.dumps(error_response, indent=2)

@mcp.tool("health")
async def health_check() -> str:
    """
    Health check endpoint for testing server connectivity.
    
    Returns:
        Simple string indicating server status
    """
    return "OK - Airflow MCP Server Running with Dummy Data"

if __name__ == "__main__":
    mcp.run(
        transport=transport,
        host=mcp_host,
        port=mcp_port,
        log_level=log_level
    )
