import base64
from typing import Dict, Any, Optional
from schema import load_schema, http_utils


CREATE_OR_UPDATE_FILE_SCHEMA = load_schema("content/create_or_update_file")


async def create_or_update_file_tool(
    owner: str,
    repo: str,
    path: str,
    content: str,
    message: str,
    branch: str = "main",
    sha: Optional[str] = None
) -> Dict[str, Any]:
    """
    Create or update a file in a GitHub repository using the GitHub API.
    This tool can create a new file or update an existing one.
    
    For updating an existing file, you MUST include the SHA parameter.
    For creating a new file, omit the SHA parameter.
    
    Args:
        owner: The account owner of the repository. The name is not case sensitive.
        repo: The name of the repository without the .git extension. The name is not case sensitive.
        path: The path to the file in the repository (e.g., "src/main.py" or "README.md").
        content: The content of the file as a string.
        message: The commit message for this change.
        branch: The branch name to commit to (defaults to "main").
        sha: The SHA of the file to update (required for updates, omit for new files).
    
    Returns:
        JSON response containing the file content and commit information
    """
    print(f"Creating/updating file '{path}' in repository {owner}/{repo}")
    print(f"Branch: {branch}")
    print(f"SHA: {sha if sha else 'None (new file)'}")
    
    # Encode content to base64 as required by GitHub API
    try:
        content_bytes = content.encode('utf-8')
        encoded_content = base64.b64encode(content_bytes).decode('utf-8')
        print(f"Content encoded to base64 (length: {len(encoded_content)})")
    except Exception as e:
        raise ValueError(f"Failed to encode content to base64: {str(e)}")
    
    # Prepare the request payload
    payload = {
        "message": message,
        "content": encoded_content,
        "branch": branch
    }
    
    # Add SHA for updates (required for existing files)
    if sha:
        payload["sha"] = sha
        print(f"Updating existing file with SHA: {sha}")
    else:
        print("Creating new file")
    
    # Make the API request
    endpoint = f"repos/{owner}/{repo}/contents/{path}"
    print(f"Making request to: {endpoint}")
    print(f"Payload keys: {list(payload.keys())}")
    
    try:
        response = http_utils.get_json_response(endpoint, method='PUT', body=payload)
        print(f"Successfully created/updated file")
        return response
        
    except Exception as e:
        print(f"Error creating/updating file: {e}")
        raise ValueError(f"Failed to create/update file '{path}': {str(e)}")
