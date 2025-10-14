from typing import Dict, Any
from schema import load_schema, http_utils


CONTENT_TREE_SCHEMA = load_schema("content/content_tree")


async def get_file_contents_tool(owner: str, repo: str, path: str = "", ref: str = "") -> Dict[str, Any]:
    """
    Get the contents of a file or directory in a GitHub repository. This tool is used to get any information of a file in a GitHub repository.
    
    Args:
        owner: The account owner of the repository. The name is not case sensitive.
        repo: The name of the repository without the .git extension. The name is not case sensitive.
        path: The path to the file or directory (optional, defaults to repository root)
        ref: The name of the commit/branch/tag (optional, defaults to repository's default branch)
    
    Returns:
        JSON response containing file or directory contents
    """
    endpoint = f"repos/{owner}/{repo}/contents/{path}" if path else f"repos/{owner}/{repo}/contents"
    print(f"Getting file contents for {endpoint}")
    params = {}
    if ref:
        params["ref"] = ref
    print(f"Params: {params}")
    response = http_utils.get_json_response(endpoint, params=params)
    print(f"Response: {response}")
    return response
