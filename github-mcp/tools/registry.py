from typing import Callable, Dict, Any, List, TypedDict

# Import tool handlers and schemas from modules
from tools.content import (
    CONTENT_TREE_SCHEMA,
    get_file_contents_tool,
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
    ]


def register_all(mcp) -> None:
    for spec in get_all_tool_specs():
        mcp.tool(
            name=spec["name"],
            description=spec["description"],
            output_schema=spec["output_schema"],
        )(spec["handler"])
