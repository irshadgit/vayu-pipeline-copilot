from typing import Optional, List, Dict, Union
from schema import load_schema, http_utils


# ============================================================================
# Variable Schema
# ============================================================================

VARIABLE_SCHEMA = load_schema("variable/variable")

# ============================================================================
# Variable Collection Schema
# ============================================================================

VARIABLE_COLLECTION_SCHEMA = load_schema("variable/variable_collection")


async def get_variables_tool(
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    fields: Optional[List[str]] = None
) -> dict:
    """
    Get all variables with optional filtering and pagination.
    
    This tool retrieves a list of all variables configured in Airflow with optional
    filtering and pagination support. Variables are used to store configuration values,
    secrets, and other data that can be accessed by DAGs and tasks.
    
    Use this tool when you need to:
    - List all available variables in Airflow
    - Check what variables are configured
    - Find specific variables by browsing the list
    - Get an overview of variable configuration
    
    Args:
        limit: The numbers of items to return (default: 100, max: 100)
        offset: The number of items to skip before starting to collect the result set (default: 0)
        order_by: The name of the field to order the results by. Prefix a field name with `-` to reverse the sort order
        fields: List of fields to return in the response
    
    Returns:
        JSON response containing list of variables with their configuration details.
        Each variable includes:
        - key: Unique identifier for the variable
        - value: The variable value (may be masked if sensitive)
        - description: Description of the variable
        - is_encrypted: Whether the variable is encrypted
    """
    endpoint = "variables"
    
    # Build query params
    params: Dict[str, Union[str, int]] = {}
    if limit is not None: 
        params["limit"] = int(limit)
    if offset is not None: 
        params["offset"] = int(offset)
    if order_by: 
        params["order_by"] = str(order_by)
    if fields: 
        params["fields"] = ",".join(fields)
    
    print(f"🔧 GET_VARIABLES - Endpoint: {endpoint}")
    print(f"🔧 GET_VARIABLES - Params: {params}")
    
    # Make the request
    response = http_utils.get_json_response(endpoint, params=params)
    print(f"🔧 GET_VARIABLES - Response: {response}")
    return response


async def get_variable_tool(
    variable_key: str,
    fields: Optional[List[str]] = None
) -> dict:
    """
    Get details of a specific variable by its key.
    
    This tool retrieves detailed information about a specific variable configuration
    in Airflow. This is useful for getting variable details, checking configuration,
    or debugging variable issues.
    
    Use this tool when you need to:
    - Get detailed information about a specific variable
    - Check variable configuration and value
    - Debug variable-related issues
    - Verify variable settings before using in DAGs
    - Get variable values for configuration or secrets
    
    Args:
        variable_key: The unique key of the variable to retrieve (required)
        fields: Optional list of fields to return in the response
    
    Returns:
        JSON response containing detailed information about the specified variable.
        The response includes:
        - key: Unique identifier for the variable
        - value: The variable value (may be masked if sensitive)
        - description: Description of the variable
        - is_encrypted: Whether the variable is encrypted
    """
    endpoint = f"variables/{variable_key}"
    
    # Build query params
    params: Dict[str, str] = {}
    if fields:
        params["fields"] = ",".join(fields)
    
    print(f"🔧 GET_VARIABLE - Endpoint: {endpoint}")
    print(f"🔧 GET_VARIABLE - Params: {params}")
    
    # Make the request
    response = http_utils.get_json_response(endpoint, params=params)
    print(f"🔧 GET_VARIABLE - Response: {response}")
    return response


async def create_variable_tool(
    key: str,
    value: str,
    description: Optional[str] = None
) -> dict:
    """
    Create a new variable in Airflow.
    
    This tool creates a new variable configuration in Airflow with the specified
    key and value. Variables are essential for DAGs to access configuration values,
    secrets, and other data that should be externalized from code.
    
    Use this tool when you need to:
    - Set up new configuration variables for DAGs
    - Store secrets and sensitive data
    - Create environment-specific configuration values
    - Set up variables for external system connections
    - Configure variables programmatically
    
    Args:
        key: Unique identifier for the variable (required)
        value: The variable value (required)
        description: Description of the variable
    
    Returns:
        JSON response containing the created variable details.
        The response includes all the variable parameters that were set,
        along with any default values applied by Airflow.
    """
    endpoint = "variables"
    
    # Build request body
    body = {
        "key": key,
        "value": value
    }
    
    # Add optional fields if provided
    if description is not None:
        body["description"] = description
    
    print(f"🔧 CREATE_VARIABLE - Endpoint: {endpoint}")
    print(f"🔧 CREATE_VARIABLE - Body: {body}")
    
    # Make the request
    response = http_utils.get_json_response(endpoint, method="POST", body=body)
    print(f"🔧 CREATE_VARIABLE - Response: {response}")
    return response


async def update_variable_tool(
    variable_key: str,
    value: str,
    description: Optional[str] = None
) -> dict:
    """
    Update an existing variable in Airflow.
    
    This tool updates an existing variable in Airflow using the PATCH endpoint.
    Based on the Airflow source code, the PATCH endpoint can update both value and description.
    The request body must include the key that matches the URL parameter.
    
    Use this tool when you need to:
    - Update variable values (secrets, configuration)
    - Update variable descriptions
    - Change variable configuration
    - Fix variable configuration issues
    - Update environment-specific values
    
    Args:
        variable_key: Unique identifier for the variable to update (required)
        value: The new variable value (required)
        description: The new description for the variable (optional)
    
    Returns:
        JSON response containing the updated variable details.
        The response includes the variable parameters after the update.
    """
    endpoint = f"variables/{variable_key}"
    
    # Build request body according to Airflow's variable schema
    body = {
        "key": variable_key,
        "value": value
    }
    
    # Add description if provided
    if description is not None:
        body["description"] = description
    
    print(f"🔧 UPDATE_VARIABLE - Endpoint: {endpoint}")
    print(f"🔧 UPDATE_VARIABLE - Body: {body}")
    
    # Make the request using PATCH
    response = http_utils.get_json_response(endpoint, method="PATCH", body=body)
    print(f"🔧 UPDATE_VARIABLE - Response: {response}")
    return response


async def delete_variable_tool(
    variable_key: str
) -> dict:
    """
    Delete a variable from Airflow.
    
    This tool removes a variable configuration from Airflow. This action cannot
    be undone, so ensure the variable is not being used by any active DAGs
    before deletion.
    
    Use this tool when you need to:
    - Remove unused or obsolete variables
    - Clean up variable configurations
    - Remove variables that are no longer needed
    - Delete variables with incorrect configurations
    
    Args:
        variable_key: Unique identifier for the variable to delete (required)
    
    Returns:
        JSON response confirming the deletion operation.
        The response typically includes a success message or status.
    """
    endpoint = f"variables/{variable_key}"
    
    print(f"🔧 DELETE_VARIABLE - Endpoint: {endpoint}")
    
    # Make the request
    response = http_utils.get_json_response(endpoint, method="DELETE")
    print(f"🔧 DELETE_VARIABLE - Response: {response}")
    return response
