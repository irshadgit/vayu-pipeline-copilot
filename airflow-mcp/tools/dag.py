
from typing import Optional, List, Dict, Union
from schema import load_schema, http_utils


TIME_DELTA_SCHEMA = load_schema("commons/time_delta")
CRON_EXPRESSION_SCHEMA = load_schema("commons/cron_expression")
SCHEDULE_INTERVAL_SCHEMA = load_schema("dag/schedule_interval")
TAG_SCHEMA = load_schema("commons/tag")
PARAMS_SCHEMA = load_schema("commons/params")

# ============================================================================
# DAG Schema
# ============================================================================

DAG_SCHEMA = load_schema("dag/dag")

# ============================================================================
# DAG Collection Schema
# ============================================================================

DAG_COLLECTION_SCHEMA = load_schema("dag/dag_collection")

# ============================================================================
# DAG Run Schema
# ============================================================================

DAG_RUN_SCHEMA = load_schema("dag/dag_run")

# ============================================================================
# DAG Run Collection Schema
# ============================================================================

DAG_RUN_COLLECTION_SCHEMA = load_schema("dag/dag_run_collection")

# ============================================================================
# DAG Source Schema
# ============================================================================

DAG_SOURCE_SCHEMA = load_schema("dag/dag_source")





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


async def get_dag_runs_tool(
    dag_id: str,
    limit: int = 100,
    offset: int = 0,
    execution_date_gte: Optional[str] = None,
    execution_date_lte: Optional[str] = None,
    start_date_gte: Optional[str] = None,
    start_date_lte: Optional[str] = None,
    end_date_gte: Optional[str] = None,
    end_date_lte: Optional[str] = None,
    updated_at_gte: Optional[str] = None,
    updated_at_lte: Optional[str] = None,
    state: Optional[List[str]] = None,
    order_by: Optional[str] = None,
    fields: Optional[List[str]] = None
) -> str:
    """
    Get DAG runs for a specific DAG or all DAGs.
    
    This endpoint allows specifying ~ as the dag_id to retrieve DAG runs for all DAGs.
    
    Args:
        dag_id: The DAG ID. Use "~" to retrieve runs for all DAGs.
        limit: The numbers of items to return (default: 100)
        offset: The number of items to skip before starting to collect the result set (default: 0)
        execution_date_gte: Returns objects greater or equal to the specified date.
                           This can be combined with execution_date_lte parameter to receive only the selected period.
        execution_date_lte: Returns objects less than or equal to the specified date.
                           This can be combined with execution_date_gte parameter to receive only the selected period.
        start_date_gte: Returns objects greater or equal the specified date.
                       This can be combined with start_date_lte parameter to receive only the selected period.
        start_date_lte: Returns objects less or equal the specified date.
                       This can be combined with start_date_gte parameter to receive only the selected period.
        end_date_gte: Returns objects greater or equal the specified date.
                     This can be combined with start_date_lte parameter to receive only the selected period.
        end_date_lte: Returns objects less than or equal to the specified date.
                     This can be combined with start_date_gte parameter to receive only the selected period.
        updated_at_gte: Returns objects greater or equal the specified date.
                       This can be combined with updated_at_lte parameter to receive only the selected period.
                       (New in version 2.6.0)
        updated_at_lte: Returns objects less or equal the specified date.
                       This can be combined with updated_at_gte parameter to receive only the selected period.
                       (New in version 2.6.0)
        state: The value can be repeated to retrieve multiple matching values (OR condition).
               Valid states: queued, running, success, failed, up_for_retry, up_for_reschedule, upstream_failed, skipped, scheduled
        order_by: The name of the field to order the results by. 
                 Prefix a field name with - to reverse the sort order. (New in version 2.1.0)
        fields: List of field for return.
    
    Returns:
        JSON response containing list of DAG runs with their information
    """
    endpoint = f"dags/{dag_id}/dagRuns"
    
    # Build query params
    params: Dict[str, Union[str, int]] = {}
    if limit is not None: 
        params["limit"] = int(limit)
    if offset is not None: 
        params["offset"] = int(offset)
    if execution_date_gte: 
        params["execution_date_gte"] = str(execution_date_gte)
    if execution_date_lte: 
        params["execution_date_lte"] = str(execution_date_lte)
    if start_date_gte: 
        params["start_date_gte"] = str(start_date_gte)
    if start_date_lte: 
        params["start_date_lte"] = str(start_date_lte)
    if end_date_gte: 
        params["end_date_gte"] = str(end_date_gte)
    if end_date_lte: 
        params["end_date_lte"] = str(end_date_lte)
    if updated_at_gte: 
        params["updated_at_gte"] = str(updated_at_gte)
    if updated_at_lte: 
        params["updated_at_lte"] = str(updated_at_lte)
    if order_by: 
        params["order_by"] = str(order_by)
    if state: 
        # Handle multiple state values by joining them with commas
        # The Airflow API typically accepts comma-separated values for array parameters
        params["state"] = ",".join(state)
    if fields: 
        params["fields"] = ",".join(fields)
    
    # Make the request
    response = http_utils.get_json_response(endpoint, params=params)
    return response


async def get_dag_source_tool(
    file_token: str
) -> dict:
    """
    Get the source code of a DAG using its file token.
    
    The file_token is obtained from the get_dag_details response file_token attribute.
    This endpoint retrieves the actual Python source code of the DAG file.
    
    Args:
        file_token: The encrypted file token obtained from DAG details.
                   This is a secure token that prevents unauthorized access to non-DAG files.
    
    Returns:
        JSON response containing the DAG source code with the following fields:
          - content: The actual Python source code of the DAG file
          - file_token: The file token used to retrieve the source code
          - dag_id: The DAG ID this source code belongs to (if available)
    """
    endpoint = f"dagSources/{file_token}"
    
    # Make the request - no additional parameters needed for this endpoint
    response = http_utils.get_json_response(endpoint)
    return response

