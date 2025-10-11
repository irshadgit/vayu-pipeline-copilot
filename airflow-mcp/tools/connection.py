from typing import Optional, List, Dict, Union
from schema import load_schema, http_utils


# ============================================================================
# Connection Schema
# ============================================================================

CONNECTION_SCHEMA = load_schema("connection/connection")

# ============================================================================
# Connection Collection Schema
# ============================================================================

CONNECTION_COLLECTION_SCHEMA = load_schema("connection/connection_collection")


async def get_connections_tool(
    limit: int = 100,
    offset: int = 0,
    order_by: Optional[str] = None,
    fields: Optional[List[str]] = None
) -> dict:
    """
    Get all connections with optional filtering and pagination.
    
    This tool retrieves a list of all connections configured in Airflow with optional
    filtering and pagination support. Connections are used to store database credentials,
    API keys, and other connection details for external systems.
    
    Use this tool when you need to:
    - List all available connections in Airflow
    - Check what connection types are configured
    - Find specific connections by browsing the list
    - Get an overview of connection configuration
    
    Args:
        limit: The numbers of items to return (default: 100, max: 100)
        offset: The number of items to skip before starting to collect the result set (default: 0)
        order_by: The name of the field to order the results by. Prefix a field name with `-` to reverse the sort order
        fields: List of fields to return in the response
    
    Returns:
        JSON response containing list of connections with their configuration details.
        Each connection includes:
        - connection_id: Unique identifier for the connection
        - conn_type: Type of connection (postgres, mysql, http, etc.)
        - host: Host address for the connection
        - login: Username for the connection
        - schema: Database schema name
        - port: Port number for the connection
        - description: Description of the connection
        - is_encrypted: Whether the connection is encrypted
        - is_extra_encrypted: Whether the extra field is encrypted
    """
    endpoint = "connections"
    
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
    
    print(f"🔗 GET_CONNECTIONS - Endpoint: {endpoint}")
    print(f"🔗 GET_CONNECTIONS - Params: {params}")
    
    # Make the request
    response = http_utils.get_json_response(endpoint, params=params)
    print(f"🔗 GET_CONNECTIONS - Response: {response}")
    return response


async def get_connection_tool(
    connection_id: str,
    fields: Optional[List[str]] = None
) -> dict:
    """
    Get details of a specific connection by its connection_id.
    
    This tool retrieves detailed information about a specific connection configuration
    in Airflow. This is useful for getting connection details, checking configuration,
    or debugging connection issues.
    
    Use this tool when you need to:
    - Get detailed information about a specific connection
    - Check connection configuration and parameters
    - Debug connection-related issues
    - Verify connection settings before using in DAGs
    - Get connection credentials for external system access
    
    Args:
        connection_id: The unique ID of the connection to retrieve (required)
        fields: Optional list of fields to return in the response
    
    Returns:
        JSON response containing detailed information about the specified connection.
        The response includes:
        - connection_id: Unique identifier for the connection
        - conn_type: Type of connection (postgres, mysql, http, etc.)
        - host: Host address for the connection
        - login: Username for the connection
        - schema: Database schema name
        - port: Port number for the connection
        - password: Password for the connection (if not encrypted)
        - extra: Additional connection parameters
        - description: Description of the connection
        - is_encrypted: Whether the connection is encrypted
        - is_extra_encrypted: Whether the extra field is encrypted
    """
    endpoint = f"connections/{connection_id}"
    
    # Build query params
    params: Dict[str, str] = {}
    if fields:
        params["fields"] = ",".join(fields)
    
    print(f"🔗 GET_CONNECTION - Endpoint: {endpoint}")
    print(f"🔗 GET_CONNECTION - Params: {params}")
    
    # Make the request
    response = http_utils.get_json_response(endpoint, params=params)
    print(f"🔗 GET_CONNECTION - Response: {response}")
    return response


async def create_connection_tool(
    connection_id: str,
    conn_type: str,
    host: Optional[str] = None,
    login: Optional[str] = None,
    schema: Optional[str] = None,
    port: Optional[int] = None,
    password: Optional[str] = None,
    extra: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """
    Create a new connection in Airflow.
    
    This tool creates a new connection configuration in Airflow with the specified
    parameters. Connections are essential for DAGs to connect to external systems
    like databases, APIs, or cloud services.
    
    Use this tool when you need to:
    - Set up new database connections for DAGs
    - Configure API connections for external services
    - Create connections for cloud storage or messaging systems
    - Set up authentication for external systems
    - Configure connections programmatically
    
    Args:
        connection_id: Unique identifier for the connection (required)
        conn_type: Type of connection (postgres, mysql, http, s3, gcs, etc.) (required)
        host: Host address for the connection
        login: Username for the connection
        schema: Database schema name
        port: Port number for the connection
        password: Password for the connection
        extra: Additional connection parameters as JSON string
        description: Description of the connection
    
    Returns:
        JSON response containing the created connection details.
        The response includes all the connection parameters that were set,
        along with any default values applied by Airflow.
    """
    endpoint = "connections"
    
    # Build request body
    body = {
        "connection_id": connection_id,
        "conn_type": conn_type
    }
    
    # Add optional fields if provided
    if host is not None:
        body["host"] = host
    if login is not None:
        body["login"] = login
    if schema is not None:
        body["schema"] = schema
    if port is not None:
        body["port"] = int(port)
    if password is not None:
        body["password"] = password
    if extra is not None:
        body["extra"] = extra
    if description is not None:
        body["description"] = description
    
    print(f"🔗 CREATE_CONNECTION - Endpoint: {endpoint}")
    print(f"🔗 CREATE_CONNECTION - Body: {body}")
    
    # Make the request
    response = http_utils.get_json_response(endpoint, method="POST", body=body)
    print(f"🔗 CREATE_CONNECTION - Response: {response}")
    return response


async def update_connection_tool(
    connection_id: str,
    conn_type: Optional[str] = None,
    host: Optional[str] = None,
    login: Optional[str] = None,
    schema: Optional[str] = None,
    port: Optional[int] = None,
    password: Optional[str] = None,
    extra: Optional[str] = None,
    description: Optional[str] = None
) -> dict:
    """
    Update an existing connection in Airflow.
    
    This tool updates an existing connection configuration in Airflow with new
    parameters. Only the provided fields will be updated, leaving other fields
    unchanged.
    
    Use this tool when you need to:
    - Update connection credentials (password, host, port)
    - Modify connection parameters or extra fields
    - Change connection type or schema
    - Update connection description
    - Fix connection configuration issues
    
    Args:
        connection_id: Unique identifier for the connection to update (required)
        conn_type: Type of connection (postgres, mysql, http, s3, gcs, etc.)
        host: Host address for the connection
        login: Username for the connection
        schema: Database schema name
        port: Port number for the connection
        password: Password for the connection
        extra: Additional connection parameters as JSON string
        description: Description of the connection
    
    Returns:
        JSON response containing the updated connection details.
        The response includes all the connection parameters after the update.
    """
    endpoint = f"connections/{connection_id}"
    
    # Build request body with only provided fields
    body = {}
    if conn_type is not None:
        body["conn_type"] = conn_type
    if host is not None:
        body["host"] = host
    if login is not None:
        body["login"] = login
    if schema is not None:
        body["schema"] = schema
    if port is not None:
        body["port"] = int(port)
    if password is not None:
        body["password"] = password
    if extra is not None:
        body["extra"] = extra
    if description is not None:
        body["description"] = description
    
    print(f"🔗 UPDATE_CONNECTION - Endpoint: {endpoint}")
    print(f"🔗 UPDATE_CONNECTION - Body: {body}")
    
    # Make the request
    response = http_utils.get_json_response(endpoint, method="PATCH", body=body)
    print(f"🔗 UPDATE_CONNECTION - Response: {response}")
    return response


async def delete_connection_tool(
    connection_id: str
) -> dict:
    """
    Delete a connection from Airflow.
    
    This tool removes a connection configuration from Airflow. This action cannot
    be undone, so ensure the connection is not being used by any active DAGs
    before deletion.
    
    Use this tool when you need to:
    - Remove unused or obsolete connections
    - Clean up connection configurations
    - Remove connections that are no longer needed
    - Delete connections with incorrect configurations
    
    Args:
        connection_id: Unique identifier for the connection to delete (required)
    
    Returns:
        JSON response confirming the deletion operation.
        The response typically includes a success message or status.
    """
    endpoint = f"connections/{connection_id}"
    
    print(f"🔗 DELETE_CONNECTION - Endpoint: {endpoint}")
    
    # Make the request
    response = http_utils.get_json_response(endpoint, method="DELETE")
    print(f"🔗 DELETE_CONNECTION - Response: {response}")
    return response


async def test_connection_tool(
    connection_id: str
) -> dict:
    """
    Test a connection to verify it's working correctly.
    
    This tool tests an existing connection to verify that it can successfully
    connect to the external system. This is useful for validating connection
    configuration and troubleshooting connection issues.
    
    Use this tool when you need to:
    - Verify connection configuration is correct
    - Test connectivity to external systems
    - Debug connection-related issues
    - Validate credentials and connection parameters
    - Ensure connections are working before using in DAGs
    
    Args:
        connection_id: Unique identifier for the connection to test (required)
    
    Returns:
        JSON response containing the test results.
        The response includes:
        - status: Test status (success, failed, etc.)
        - message: Detailed message about the test result
        - exception: Exception details if the test failed
    """
    endpoint = f"connections/{connection_id}/test"
    
    print(f"🔗 TEST_CONNECTION - Endpoint: {endpoint}")
    
    # Make the request
    response = http_utils.get_json_response(endpoint, method="POST")
    print(f"🔗 TEST_CONNECTION - Response: {response}")
    return response
