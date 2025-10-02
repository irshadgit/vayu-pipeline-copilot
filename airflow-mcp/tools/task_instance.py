from typing import Optional, List, Dict, Union
from schema import load_schema, http_utils


# ============================================================================
# Task Instance Schema
# ============================================================================

TASK_INSTANCE_SCHEMA = load_schema("dag/task_instance")

# ============================================================================
# Task Instance Collection Schema
# ============================================================================

TASK_INSTANCE_COLLECTION_SCHEMA = load_schema("dag/task_instance_collection")

# ============================================================================
# Task Instance Tries Schema
# ============================================================================

TASK_INSTANCE_TRIES_SCHEMA = load_schema("dag/task_instance_tries")

# ============================================================================
# Task Instance Try Details Schema
# ============================================================================

TASK_INSTANCE_TRY_DETAILS_SCHEMA = load_schema("dag/task_instance_try_details")

# ============================================================================
# Task Instance Log Schema
# ============================================================================

TASK_INSTANCE_LOG_SCHEMA = load_schema("dag/task_instance_log")


async def list_task_instances_tool(
    dag_id: str,
    dag_run_id: str,
    limit: int = 100,
    offset: int = 0,
    execution_date_gte: Optional[str] = None,
    execution_date_lte: Optional[str] = None,
    start_date_gte: Optional[str] = None,
    start_date_lte: Optional[str] = None,
    end_date_gte: Optional[str] = None,
    end_date_lte: Optional[str] = None,
    duration_gte: Optional[float] = None,
    duration_lte: Optional[float] = None,
    state: Optional[List[str]] = None,
    pool: Optional[List[str]] = None,
    queue: Optional[List[str]] = None,
    order_by: Optional[str] = None,
    fields: Optional[List[str]] = None
) -> str:
    """
    List all task instances for a specific DAG run.
    
    This tool retrieves task instances associated with a specific DAG and DAG run from Airflow.
    Task instances represent individual executions of tasks within a DAG run and contain detailed
    information about their execution status, timing, and configuration.
    
    Use this tool when you need to:
    - Monitor the status and progress of tasks within a specific DAG run
    - Analyze task performance and execution times
    - Debug failed or problematic task instances
    - Get detailed information about task execution history
    - Filter tasks by state, pool, queue, or time ranges
    
    Args:
        dag_id: The DAG ID to retrieve task instances for (required)
        dag_run_id: The DAG run ID to retrieve task instances for (required)
        limit: The maximum number of task instances to return (default: 100, max: 100)
        offset: The number of task instances to skip before starting to collect the result set (default: 0)
        execution_date_gte: Filter by execution date greater than or equal to this value (ISO 8601 format)
        execution_date_lte: Filter by execution date less than or equal to this value (ISO 8601 format)
        start_date_gte: Filter by start date greater than or equal to this value (ISO 8601 format)
        start_date_lte: Filter by start date less than or equal to this value (ISO 8601 format)
        end_date_gte: Filter by end date greater than or equal to this value (ISO 8601 format)
        end_date_lte: Filter by end date less than or equal to this value (ISO 8601 format)
        duration_gte: Filter by duration greater than or equal to this value (in seconds)
        duration_lte: Filter by duration less than or equal to this value (in seconds)
        state: Filter by task state(s). Valid states: queued, running, success, failed, up_for_retry, 
               up_for_reschedule, upstream_failed, skipped, scheduled, deferred, removed, restarting
        pool: Filter by pool name(s)
        queue: Filter by queue name(s)
        order_by: The name of the field to order the results by. Prefix a field name with '-' to reverse the sort order
        fields: List of fields to return in the response
    
    Returns:
        JSON response containing a paginated list of task instances with their detailed information.
        Each task instance includes:
        - task_id: Unique identifier for the task within the DAG
        - dag_id: The DAG ID this task instance belongs to
        - dag_run_id: The DAG run ID this task instance belongs to
        - state: Current state of the task instance
        - execution_date: Logical execution date of the task instance
        - start_date: When the task instance started
        - end_date: When the task instance ended
        - duration: Duration of the task instance in seconds
        - pool: Pool name the task instance is assigned to
        - queue: Queue name the task instance is assigned to
        - operator: Operator type of the task
        - try_number: Current try number for the task instance
        - max_tries: Maximum number of retries for the task
        - hostname: Hostname where the task instance is running
        - pid: Process ID of the task instance
        - And many other detailed execution parameters
    """
    endpoint = f"dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances"
    
    # Build query params
    params: Dict[str, Union[str, int, float]] = {}
    if limit is not None: params["limit"] = int(limit)
    if offset is not None: params["offset"] = int(offset)
    if execution_date_gte: params["execution_date_gte"] = execution_date_gte
    if execution_date_lte: params["execution_date_lte"] = execution_date_lte
    if start_date_gte: params["start_date_gte"] = start_date_gte
    if start_date_lte: params["start_date_lte"] = start_date_lte
    if end_date_gte: params["end_date_gte"] = end_date_gte
    if end_date_lte: params["end_date_lte"] = end_date_lte
    if duration_gte is not None: params["duration_gte"] = float(duration_gte)
    if duration_lte is not None: params["duration_lte"] = float(duration_lte)
    if order_by: params["order_by"] = order_by
    if state: 
        # Handle multiple state values by joining them with commas
        params["state"] = ",".join(state)
    if pool: params["pool"] = ",".join(pool)
    if queue: params["queue"] = ",".join(queue)
    if fields: params["fields"] = ",".join(fields)
    
    # Make the request
    response = http_utils.get_json_response(endpoint, params=params)
    return response


async def get_task_instance_tool(
    dag_id: str,
    dag_run_id: str,
    task_id: str,
    fields: Optional[List[str]] = None
) -> dict:
    """
    Get details of a specific task instance.
    
    This tool retrieves detailed information about a specific task instance from a DAG run.
    Task instances represent individual executions of tasks and contain comprehensive
    information about their execution status, timing, configuration, and results.
    
    Use this tool when you need to:
    - Get detailed information about a specific task execution
    - Debug a particular task that failed or is having issues
    - Analyze the execution details of a specific task instance
    - Check the status, logs, and configuration of a single task
    - Monitor the progress of a specific task within a DAG run
    
    Args:
        dag_id: The DAG ID that contains the task instance (required)
        dag_run_id: The DAG run ID that contains the task instance (required)
        task_id: The task ID of the specific task instance to retrieve (required)
        fields: Optional list of fields to return in the response
    
    Returns:
        JSON response containing detailed information about the specified task instance.
        The response includes:
        - task_id: Unique identifier for the task within the DAG
        - dag_id: The DAG ID this task instance belongs to
        - dag_run_id: The DAG run ID this task instance belongs to
        - state: Current state of the task instance (queued, running, success, failed, etc.)
        - execution_date: Logical execution date of the task instance
        - start_date: When the task instance started
        - end_date: When the task instance ended
        - duration: Duration of the task instance in seconds
        - try_number: Current try number for the task instance
        - max_tries: Maximum number of retries for the task
        - hostname: Hostname where the task instance is running
        - pid: Process ID of the task instance
        - pool: Pool name the task instance is assigned to
        - queue: Queue name the task instance is assigned to
        - operator: Operator type of the task
        - priority_weight: Priority weight of the task instance
        - rendered_fields: Rendered fields for the task instance
        - map_index: Map index for the task instance (for mapped tasks)
        - note: Note attached to the task instance
        - And many other detailed execution parameters
    """
    endpoint = f"dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}"
    
    # Build query params
    params: Dict[str, str] = {}
    if fields: params["fields"] = ",".join(fields)
    
    # Make the request
    response = http_utils.get_json_response(endpoint, params=params)
    return response


async def get_task_instance_tries_tool(
    dag_id: str,
    dag_run_id: str,
    task_id: str,
    fields: Optional[List[str]] = None
) -> str:
    """
    Get all tries for a specific task instance.
    
    This tool retrieves information about all execution attempts (tries) for a specific task instance.
    Each task instance can have multiple tries due to retries, failures, or reschedules.
    This provides detailed history of all execution attempts for debugging and analysis.
    
    Use this tool when you need to:
    - Analyze the retry history of a failed task
    - Debug why a task is failing repeatedly
    - Monitor the progression of task execution attempts
    - Get detailed information about each retry attempt
    - Analyze performance patterns across multiple tries
    - Check the state and timing of each execution attempt
    
    Args:
        dag_id: The DAG ID that contains the task instance (required)
        dag_run_id: The DAG run ID that contains the task instance (required)
        task_id: The task ID of the specific task instance to retrieve tries for (required)
        fields: Optional list of fields to return in the response
    
    Returns:
        JSON response containing a list of all tries for the specified task instance.
        Each try includes:
        - try_number: The attempt number (1, 2, 3, etc.)
        - state: State of this specific try (queued, running, success, failed, etc.)
        - start_date: When this try started
        - end_date: When this try ended
        - duration: Duration of this try in seconds
        - hostname: Hostname where this try executed
        - unixname: Unix username for this try
        - job_id: Job ID for this try
        - pool: Pool name for this try
        - queue: Queue name for this try
        - priority_weight: Priority weight for this try
        - operator: Operator type for this try
        - queued_dttm: When this try was queued
        - pid: Process ID for this try
        - executor_config: Executor configuration for this try
    """
    endpoint = f"dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/tries"
    
    # Build query params
    params: Dict[str, str] = {}
    if fields: params["fields"] = ",".join(fields)
    
    # Make the request
    response = http_utils.get_json_response(endpoint, params=params)
    return response


async def get_task_instance_try_details_tool(
    dag_id: str,
    dag_run_id: str,
    task_id: str,
    try_number: int,
    fields: Optional[List[str]] = None
) -> dict:
    """
    Get detailed information about a specific try of a task instance.
    
    This tool retrieves comprehensive details about a specific execution attempt (try) 
    of a task instance. This provides the most detailed information available about
    a single execution attempt, including logs, configuration, and execution metadata.
    
    Use this tool when you need to:
    - Get detailed information about a specific retry attempt
    - Debug a particular execution that failed
    - Analyze the configuration and setup of a specific try
    - Get logs and detailed execution information for a specific attempt
    - Monitor the detailed progress of a specific execution
    - Investigate the exact conditions of a particular try
    
    Args:
        dag_id: The DAG ID that contains the task instance (required)
        dag_run_id: The DAG run ID that contains the task instance (required)
        task_id: The task ID of the specific task instance (required)
        try_number: The specific try number to get details for (required)
        fields: Optional list of fields to return in the response
    
    Returns:
        JSON response containing detailed information about the specified try.
        The response includes:
        - try_number: The attempt number
        - state: State of this specific try
        - start_date: When this try started
        - end_date: When this try ended
        - duration: Duration of this try in seconds
        - hostname: Hostname where this try executed
        - unixname: Unix username for this try
        - job_id: Job ID for this try
        - pool: Pool name for this try
        - queue: Queue name for this try
        - priority_weight: Priority weight for this try
        - operator: Operator type for this try
        - queued_dttm: When this try was queued
        - pid: Process ID for this try
        - executor_config: Executor configuration for this try
        - log_url: URL to access logs for this try
        - rendered_fields: Rendered fields for this try
        - rendered_map_index: Rendered map index for this try
        - map_index: Map index for this try
        - note: Note attached to this try
        - external_executor_id: External executor ID for this try
        - trigger_id: Trigger ID for this try
        - trigger_timeout: Trigger timeout for this try
        - next_method: Next method for this try
        - next_kwargs: Next kwargs for this try
        - updated_at: When this try was last updated
    """
    endpoint = f"dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/tries/{try_number}"
    
    # Build query params
    params: Dict[str, str] = {}
    if fields: params["fields"] = ",".join(fields)
    
    # Make the request
    response = http_utils.get_json_response(endpoint, params=params)
    return response


async def get_task_instance_log_tool(
    dag_id: str,
    dag_run_id: str,
    task_id: str,
    try_number: int,
    full_content: bool = False
) -> dict:
    """
    Get logs for a specific task instance try.
    
    This tool retrieves the log content and metadata for a specific execution attempt (try) 
    of a task instance. This provides access to the actual log output generated during
    task execution, which is essential for debugging and monitoring.
    
    Use this tool when you need to:
    - Debug task failures by examining log output
    - Monitor task execution progress through logs
    - Analyze error messages and stack traces
    - Get detailed execution information from logs
    - Troubleshoot specific execution attempts
    - Review task output and debugging information
    
    Args:
        dag_id: The DAG ID that contains the task instance (required)
        dag_run_id: The DAG run ID that contains the task instance (required)
        task_id: The task ID of the specific task instance (required)
        try_number: The specific try number to get logs for (required)
        full_content: Whether to return the full log content (default: False)
                      When False, returns a truncated version for performance
    
    Returns:
        JSON response containing log content and metadata for the specified try.
        The response includes:
        - content: The actual log content as a string
        - metadata: Metadata about the log including:
          - dag_id: The DAG ID
          - task_id: The task ID
          - dag_run_id: The DAG run ID
          - try_number: The try number
          - log_id: Unique identifier for the log
          - when: When the log was created
          - log_filename: The filename of the log
    """
    endpoint = f"dags/{dag_id}/dagRuns/{dag_run_id}/taskInstances/{task_id}/logs/{try_number}"
    
    # Build query params
    params: Dict[str, Union[str, bool]] = {}
    if full_content is not None: params["full_content"] = bool(full_content)
    
    # Make the request
    response = http_utils.get_json_response(endpoint, params=params)
    return response
