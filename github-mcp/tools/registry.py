from typing import Callable, Dict, Any, List, TypedDict

# Import tool handlers and schemas from modules
from tools.content import (
    CONTENT_TREE_SCHEMA,
    get_file_contents_tool,
)
from tools.search_code import (
    GIT_TREE_SCHEMA,
    search_code_tool,
)
from tools.create_branch import (
    GIT_REF_SCHEMA,
    create_branch_tool,
)
from tools.create_or_update_file import (
    CREATE_OR_UPDATE_FILE_SCHEMA,
    create_or_update_file_tool,
)
from tools.create_pull_request import (
    CREATE_PULL_REQUEST_SCHEMA,
    create_pull_request_tool,
)


class ToolSpec(TypedDict):
    name: str
    description: str
    output_schema: Dict[str, Any]
    handler: Callable[..., Any]


def get_all_tool_specs() -> List[ToolSpec]:
    return [
        {
            "name": "get_file_contents",
            "description": "Get the information of a file or directory in a GitHub repository. Specify the file path or directory with the path parameter. If you omit the path parameter, you will receive the contents of the repository's root directory.",
            "output_schema": CONTENT_TREE_SCHEMA,
            "handler": get_file_contents_tool,
        },
        {
            "name": "search_code",
            "description": "Search for files in a GitHub repository using the Git Trees API. This tool recursively fetches the repository tree and filters files based on search criteria including query, file extension, and path filters.",
            "output_schema": GIT_TREE_SCHEMA,
            "handler": search_code_tool,
        },
        {
            "name": "create_branch",
            "description": "Create a new branch in a GitHub repository from an existing branch. This tool performs a two-step process: first gets the SHA of the source branch, then creates a new branch pointing to that SHA.",
            "output_schema": GIT_REF_SCHEMA,
            "handler": create_branch_tool,
        },
        {
            "name": "create_or_update_file",
            "description": "Create or update a file in a GitHub repository. For new files, omit the sha parameter. For updating existing files, include the sha parameter from the file's current state in github.",
            "output_schema": CREATE_OR_UPDATE_FILE_SCHEMA,
            "handler": create_or_update_file_tool,
        },
        {
            "name": "create_pull_request",
            "description": "Create a pull request in a GitHub repository from one branch to another. Defaults to merging into the main branch.",
            "output_schema": CREATE_PULL_REQUEST_SCHEMA,
            "handler": create_pull_request_tool,
        },
    ]


def register_all(mcp) -> None:
    for spec in get_all_tool_specs():
        mcp.tool(
            name=spec["name"],
            description=spec["description"],
            output_schema=spec["output_schema"],
        )(spec["handler"])
