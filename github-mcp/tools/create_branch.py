from typing import Dict, Any, Optional
from schema import load_schema, http_utils


GIT_REF_SCHEMA = load_schema("git_ref/git_ref")


async def create_branch_tool(
    owner: str, 
    repo: str, 
    new_branch_name: str,
    from_branch: str = "main"
) -> Dict[str, Any]:
    """
    Create a new branch in a GitHub repository from an existing branch.
    This tool performs a two-step process:
    1. Get the SHA of the source branch
    2. Create a new branch pointing to that SHA
    
    Args:
        owner: The account owner of the repository. The name is not case sensitive.
        repo: The name of the repository without the .git extension. The name is not case sensitive.
        new_branch_name: The name of the new branch to create.
        from_branch: The name of the branch to create from (defaults to "main").
    
    Returns:
        JSON response containing the created branch reference information
    """
    print(f"Creating branch '{new_branch_name}' from '{from_branch}' in repository {owner}/{repo}")
    
    # Step 1: Get the SHA of the existing branch
    ref_endpoint = f"repos/{owner}/{repo}/git/refs/heads/{from_branch}"
    print(f"Step 1: Getting SHA from {ref_endpoint}")
    
    try:
        ref_response = http_utils.get_json_response(ref_endpoint)
        print(f"Got reference response: {ref_response}")
        
        if "object" not in ref_response or "sha" not in ref_response["object"]:
            raise ValueError(f"Invalid response from reference endpoint: missing object.sha")
        
        source_sha = ref_response["object"]["sha"]
        print(f"Source branch SHA: {source_sha}")
        
    except Exception as e:
        print(f"Error getting source branch reference: {e}")
        raise ValueError(f"Failed to get SHA from source branch '{from_branch}': {str(e)}")
    
    # Step 2: Create the new branch
    create_endpoint = f"repos/{owner}/{repo}/git/refs"
    print(f"Step 2: Creating new branch at {create_endpoint}")
    
    payload = {
        "ref": f"refs/heads/{new_branch_name}",
        "sha": source_sha
    }
    
    print(f"Creating branch with payload: {payload}")
    
    try:
        response = http_utils.get_json_response(create_endpoint, method='POST', body=payload)
        print(f"Branch created successfully: {response}")
        return response
        
    except Exception as e:
        print(f"Error creating branch: {e}")
        raise ValueError(f"Failed to create branch '{new_branch_name}': {str(e)}")
