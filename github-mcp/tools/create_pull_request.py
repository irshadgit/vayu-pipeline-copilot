from typing import Dict, Any, Optional
from schema import load_schema, http_utils


CREATE_PULL_REQUEST_SCHEMA = load_schema("pull_request/create_pull_request")


async def create_pull_request_tool(
    owner: str,
    repo: str,
    title: str,
    head: str,
    base: str = "main",
    body: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create a pull request in a GitHub repository using the GitHub API.
    This tool creates a pull request from one branch to another branch.
    
    Args:
        owner: The account owner of the repository. The name is not case sensitive.
        repo: The name of the repository without the .git extension. The name is not case sensitive.
        title: The title of the pull request.
        head: The name of the branch where your changes are implemented (source branch).
        base: The name of the branch you want the changes pulled into (target branch, defaults to "main").
        body: The contents of the pull request description (optional).
    
    Returns:
        JSON response containing the created pull request information
    """
    print(f"Creating pull request in repository {owner}/{repo}")
    print(f"Title: {title}")
    print(f"Head branch: {head}")
    print(f"Base branch: {base}")
    print(f"Body: {body[:100] + '...' if body and len(body) > 100 else body}")
    
    # Prepare the request payload
    payload = {
        "title": title,
        "head": head,
        "base": base
    }
    
    # Add body if provided
    if body:
        payload["body"] = body
    
    # Make the API request
    endpoint = f"repos/{owner}/{repo}/pulls"
    print(f"Making request to: {endpoint}")
    print(f"Payload keys: {list(payload.keys())}")
    
    try:
        response = http_utils.get_json_response(endpoint, method='POST', body=payload)
        print(f"Successfully created pull request #{response.get('number', 'unknown')}")
        print(f"Pull request URL: {response.get('html_url', 'unknown')}")
        return response
        
    except Exception as e:
        print(f"Error creating pull request: {e}")
        raise ValueError(f"Failed to create pull request from '{head}' to '{base}': {str(e)}")
