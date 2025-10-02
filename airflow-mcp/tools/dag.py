from http_utils import HTTPUtils
from urllib.parse import urljoin
import os
from typing import Optional, List, Dict, Union



AIRFLOW_BASE_URL = urljoin(os.getenv("AIRFLOW_HOST", "http://localhost:8080"), "/api/v1")
SSL_VERIFY = os.getenv("SSL_VERIFY", "True").lower() == "true"
AIRFLOW_USERNAME = os.getenv("AIRFLOW_USERNAME", "airflow")
AIRFLOW_PASSWORD = os.getenv("AIRFLOW_PASSWORD", "airflow")
http_utils = HTTPUtils(base_url=AIRFLOW_BASE_URL, verify_ssl=SSL_VERIFY, auth=(AIRFLOW_USERNAME, AIRFLOW_PASSWORD))

TIME_DELTA_SCHEMA = {
    "type": "object",
    "description": "Represents a duration/time interval",
    "properties": {
        "__type": {
            "type": "string",
            "const": "TimeDelta",
            "description": "Type identifier for TimeDelta objects"
        },
        "days": {
            "type": "integer",
            "description": "Number of days in the interval"
        },
        "seconds": {
            "type": "integer",
            "description": "Number of seconds in the interval (0-86399)",
            "minimum": 0,
            "maximum": 86399
        },
        "microseconds": {
            "type": "integer",
            "description": "Number of microseconds in the interval (0-999999)",
            "minimum": 0,
            "maximum": 999999
        }
    },
    "required": ["__type"]
}

CRON_EXPRESSION_SCHEMA = {
    "type": "object",
    "description": "Represents a cron-based schedule",
    "properties": {
        "__type": {
            "type": "string",
            "const": "CronExpression",
            "description": "Type identifier for CronExpression objects"
        },
        "value": {
            "type": "string",
            "description": "Cron expression string (e.g., '0 0 * * *' for daily at midnight)"
        }
    },
    "required": ["__type", "value"]
}

SCHEDULE_INTERVAL_SCHEMA = {
    "oneOf": [
        TIME_DELTA_SCHEMA,
        CRON_EXPRESSION_SCHEMA,
        {
            "type": "null",
            "description": "No schedule (manually triggered only)"
        }
    ],
    "description": "Schedule interval: TimeDelta for fixed intervals, CronExpression for cron schedules, or null for manual triggering"
}

TAG_SCHEMA = {
    "type": "object",
    "description": "A tag for DAG categorization and filtering",
    "properties": {
        "name": {
            "type": "string",
            "description": "Tag name/label",
            "minLength": 1,
            "maxLength": 100
        }
    },
    "required": ["name"]
}

PARAMS_SCHEMA = {
    "type": "object",
    "description": "Default parameters for the DAG (can be overridden at runtime)",
    "additionalProperties": {
        "oneOf": [
            {"type": "string"},
            {"type": "number"},
            {"type": "boolean"},
            {"type": "object"},
            {"type": "array"},
            {"type": "null"}
        ]
    }
}

# ============================================================================
# DAG Schema
# ============================================================================

DAG_SCHEMA = {
    "type": "object",
    "description": "Complete DAG (Directed Acyclic Graph) object representing an Airflow workflow",
    "properties": {
        # Identity
        "dag_id": {
            "type": "string",
            "description": "Unique identifier for the DAG",
            "minLength": 1,
            "maxLength": 250
        },
        "root_dag_id": {
            "type": ["string", "null"],
            "description": "Root DAG ID if this is a sub-DAG"
        },
        "is_subdag": {
            "type": "boolean",
            "description": "Whether this is a sub-DAG"
        },
        
        # Status
        "is_paused": {
            "type": ["boolean", "null"],
            "description": "Whether the DAG is currently paused"
        },
        "is_active": {
            "type": ["boolean", "null"],
            "description": "Whether the DAG is active"
        },
        "has_import_errors": {
            "type": ["boolean", "null"],
            "description": "Whether the DAG has import errors"
        },
        
        # Timestamps
        "last_parsed_time": {
            "type": ["string", "null"],
            "format": "date-time",
            "description": "Last time the DAG was parsed"
        },
        "last_pickled": {
            "type": ["string", "null"],
            "format": "date-time",
            "description": "Last time the DAG was pickled"
        },
        "last_expired": {
            "type": ["string", "null"],
            "format": "date-time",
            "description": "Last time the DAG expired"
        },
        "start_date": {
            "type": ["string", "null"],
            "format": "date-time",
            "description": "DAG start date"
        },
        "end_date": {
            "type": ["string", "null"],
            "format": "date-time",
            "description": "DAG end date"
        },
        
        # Scheduling
        "schedule_interval": SCHEDULE_INTERVAL_SCHEMA,
        "timetable_description": {
            "type": ["string", "null"],
            "description": "Human-readable schedule description"
        },
        "next_dagrun": {
            "type": ["string", "null"],
            "format": "date-time",
            "description": "Next scheduled DAG run time"
        },
        "next_dagrun_data_interval_start": {
            "type": ["string", "null"],
            "format": "date-time",
            "description": "Start of next run's data interval"
        },
        "next_dagrun_data_interval_end": {
            "type": ["string", "null"],
            "format": "date-time",
            "description": "End of next run's data interval"
        },
        "next_dagrun_create_after": {
            "type": ["string", "null"],
            "format": "date-time",
            "description": "Time after which next run will be created"
        },
        
        # Configuration
        "max_active_tasks": {
            "type": ["integer", "null"],
            "description": "Maximum number of active tasks",
            "minimum": 1
        },
        "max_active_runs": {
            "type": ["integer", "null"],
            "description": "Maximum number of active DAG runs",
            "minimum": 1
        },
        "max_consecutive_failed_dag_runs": {
            "type": ["integer", "null"],
            "description": "Max consecutive failures before auto-pause",
            "minimum": 0
        },
        "concurrency": {
            "type": ["integer", "null"],
            "description": "Max running tasks (deprecated, use max_active_tasks)",
            "minimum": 1
        },
        "has_task_concurrency_limits": {
            "type": ["boolean", "null"],
            "description": "Whether tasks have concurrency limits"
        },
        "catchup": {
            "type": ["boolean", "null"],
            "description": "Whether to backfill past runs"
        },
        "is_paused_upon_creation": {
            "type": ["boolean", "null"],
            "description": "Whether DAG is paused when created"
        },
        "dagrun_timeout": TIME_DELTA_SCHEMA,
        "render_template_as_native_obj": {
            "type": ["boolean", "null"],
            "description": "Whether to render templates as native objects"
        },
        
        # Metadata
        "fileloc": {
            "type": "string",
            "description": "File path of DAG definition"
        },
        "file_token": {
            "type": ["string", "null"],
            "description": "Unique file token"
        },
        "owners": {
            "type": ["array", "null"],
            "items": {"type": "string"},
            "description": "List of DAG owner usernames"
        },
        "description": {
            "type": ["string", "null"],
            "description": "DAG description",
            "maxLength": 5000
        },
        "doc_md": {
            "type": ["string", "null"],
            "description": "Extended documentation in Markdown"
        },
        "tags": {
            "type": ["array", "null"],
            "items": TAG_SCHEMA,
            "description": "List of tags"
        },
        "params": PARAMS_SCHEMA,
        
        # UI
        "default_view": {
            "type": ["string", "null"],
            "description": "Default view in UI",
            "enum": ["tree", "graph", "duration", "gantt", "landing_times", "grid"]
        },
        "orientation": {
            "type": ["string", "null"],
            "description": "Graph orientation",
            "enum": ["LR", "TB", "RL", "BT", None]
        },
        
        # Internal
        "scheduler_lock": {
            "type": ["boolean", "null"],
            "description": "Whether scheduler has a lock"
        },
        "pickle_id": {
            "type": ["string", "null"],
            "description": "Pickle ID in database"
        }
    },
    "required": ["dag_id", "fileloc"]
}

# ============================================================================
# DAG Collection Schema
# ============================================================================

DAG_COLLECTION_SCHEMA = {
    "type": "object",
    "description": "Paginated collection of DAGs",
    "properties": {
        "dags": {
            "type": "array",
            "items": DAG_SCHEMA,
            "description": "Array of DAG objects"
        },
        "total_entries": {
            "type": "integer",
            "description": "Total number of matching DAGs",
            "minimum": 0
        }
    },
    "required": ["dags", "total_entries"]
}





async def get_dags_tool(
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    tags: Optional[List[str]] = None,
    fields: Optional[List[str]] = None,
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
        fields: List of fields to return
        only_active: Only filter active DAGs (default: True)
        paused: Only filter paused/unpaused DAGs
        dag_id_pattern: If set, only return DAGs with dag_ids matching this pattern
    
    Returns:
        JSON response containing list of DAGs with their basic information
    """
    endpoint = "dags"
    # Build query params
    params: Dict[str, Union[str, int, bool]] = {}
    if limit is not None: params["limit"] = int(limit)
    if offset is not None: params["offset"] = int(offset)
    if order_by: params["order_by"] = str(order_by)
    if only_active is not None: params["only_active"] = bool(only_active)
    if paused is not None: params["paused"] = bool(paused)
    if dag_id_pattern: params["dag_id_pattern"] = str(dag_id_pattern)
    if tags: params["tags"] = ",".join(tags)
    if fields: params["fields"] = ",".join(fields)
    # Make the request
    response = http_utils.get_json_response(endpoint, params=params)
    print("CCCCCCCCCCCC",response)
    return response



async def get_dag_tool(
    dag_id: str,
    fields: Optional[List[str]] = None
) -> dict:
    """
    Get details of a specific DAG by its dag_id.
    
    Args:
        dag_id: The unique ID of the DAG to retrieve.
        fields: Optional list of fields to return. 
                Example: ["dag_id", "is_paused", "is_active", "owners", "tags", "timetable_description"]
    
    Returns:
        JSON response containing detailed information about the specified DAG.
        Typical fields include:
          - dag_id: The DAG identifier
          - is_paused: Whether the DAG is currently paused
          - is_active: Whether the DAG is active
          - owners: List of DAG owners
          - tags: Any tags applied to the DAG
          - timetable_description / schedule_interval: DAG scheduling info
          - concurrency, max_active_tasks, max_active_runs: execution limits
          - default_view, description/doc_md, catchup, params, etc.
    """
    endpoint = f"dags/{dag_id}"
    params: Dict[str, str] = {}
    if fields:
        params["fields"] = ",".join(fields)
    
    response = http_utils.get_json_response(endpoint, params=params)
    return response

