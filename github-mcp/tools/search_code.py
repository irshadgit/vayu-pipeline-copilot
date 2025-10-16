from typing import Dict, Any, List, Optional
from schema import load_schema, http_utils


GIT_TREE_SCHEMA = load_schema("git_tree/git_tree")


async def search_code_tool(
    owner: str, 
    repo: str, 
    query: str = "", 
    ref: str = "main", 
    recursive: bool = True,
    file_extension: Optional[str] = None,
    path_filter: Optional[str] = None
) -> Dict[str, Any]:
    """
    Search for files in a GitHub repository using the Git Trees API. This tool recursively 
    fetches the repository tree and filters files based on the provided criteria.
    
    Args:
        owner: The account owner of the repository. The name is not case sensitive.
        repo: The name of the repository without the .git extension. The name is not case sensitive.
        query: Search query to filter file names or paths (case-insensitive substring match).
        ref: The name of the commit/branch/tag (defaults to "main").
        recursive: Whether to fetch the tree recursively (defaults to True).
        file_extension: Optional file extension filter (e.g., ".py", ".js", ".md").
        path_filter: Optional path filter to limit search to specific directories.
    
    Returns:
        JSON response containing filtered file tree with matching files
    """
    endpoint = f"repos/{owner}/{repo}/git/trees/{ref}"
    print(f"Searching code in repository {owner}/{repo} at ref {ref}")
    
    params = {}
    if recursive:
        params["recursive"] = "1"
    
    print(f"Params: {params}")
    response = http_utils.get_json_response(endpoint, params=params)
    print(f"Raw response received, filtering files...")
    
    # Filter the tree based on search criteria and return clean schema-compliant response
    filtered_tree = []
    query_lower = query.lower() if query else ""
    path_filter_lower = path_filter.lower() if path_filter else ""
    
    if "tree" in response:
        for item in response["tree"]:
            # Only process blob (file) items, skip tree (directory) items
            if item.get("type") != "blob":
                continue
                
            file_path = item.get("path", "")
            file_name = file_path.split("/")[-1] if "/" in file_path else file_path
            
            # Apply filters
            matches_query = not query or query_lower in file_path.lower() or query_lower in file_name.lower()
            matches_extension = not file_extension or file_name.endswith(file_extension)
            matches_path = not path_filter or path_filter_lower in file_path.lower()
            
            if matches_query and matches_extension and matches_path:
                filtered_tree.append(item)
    
    # Return clean response matching the schema structure exactly
    result = {
        "sha": response.get("sha", ""),
        "url": response.get("url", ""),
        "truncated": response.get("truncated", False),
        "tree": filtered_tree
    }
    
    print(f"Found {len(filtered_tree)} matching files")
    return result
