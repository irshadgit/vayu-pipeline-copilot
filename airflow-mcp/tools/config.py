from typing import Optional, List, Dict, Union
from schema import load_schema, http_utils


# ============================================================================
# Config Schema
# ============================================================================

CONFIG_SCHEMA = load_schema("config/config")

# ============================================================================
# Config Collection Schema
# ============================================================================

CONFIG_COLLECTION_SCHEMA = load_schema("config/config_collection")


async def get_configs_tool() -> dict:
    """
    Get all configuration settings in Airflow.
    
    This tool retrieves all configuration settings in Airflow. Configuration settings 
    control various aspects of Airflow behavior including database connections, executor 
    settings, logging, and security configurations.
    
    Use this tool when you need to:
    - List all available configuration settings in Airflow
    - Check current configuration values
    - Find specific configuration keys and their values
    - Get an overview of Airflow system configuration
    - Troubleshoot configuration-related issues
    
    Returns:
        JSON response containing all configuration settings with their details.
        The response includes:
        - key: The configuration key name
        - value: The current configuration value
        - description: Description of what the configuration controls
        - default_value: Default value for the configuration
        - is_sensitive: Whether the configuration contains sensitive information
    """
    endpoint = "config"
    
    # Make the request
    response = http_utils.get_json_response(endpoint)
    return response


async def get_config_tool(
    section: str,
    option: str
) -> dict:
    """
    Get a specific configuration value by section and option.
    
    This tool retrieves a specific configuration value from Airflow by providing
    both the section and option names. This is useful for checking specific
    configuration values or troubleshooting configuration issues.
    
    Use this tool when you need to:
    - Get a specific configuration value
    - Check the current value of a configuration setting
    - Debug configuration-related issues
    - Verify configuration values for troubleshooting
    
    Args:
        section: The configuration section name (required)
        option: The configuration option name (required)
    
    Returns:
        JSON response containing the configuration value in sections format.
        The response includes:
        - sections: Array containing the specific section
        - options: Array containing the specific option with key and value
    """
    endpoint = f"config/{section}/{option}"
    
    # Make the request
    response = http_utils.get_json_response(endpoint)
    return response


