import json
import os
from typing import Any, Dict, Set

from http_utils import HTTPUtils
from urllib.parse import urljoin
import os
from typing import Dict, Any

GITHUB_BASE_URL = "https://api.github.com"
GITHUB_TOKEN = os.getenv("GITHUB_PAT_TOKEN")
http_utils = HTTPUtils(
    base_url=GITHUB_BASE_URL, 
    verify_ssl=True, 
    headers={"Authorization": f"Bearer {GITHUB_TOKEN}"} if GITHUB_TOKEN else {}
)


def _load_json(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _resolve_refs(node: Any, current_dir: str, visited: Set[str]) -> Any:
    if isinstance(node, dict):
        if "$ref" in node and isinstance(node["$ref"], str):
            ref: str = node["$ref"]
            if not (ref.startswith("http://") or ref.startswith("https://") or ref.startswith("#")):
                target_path = os.path.normpath(os.path.join(current_dir, ref))
                if target_path in visited:
                    return {}
                visited.add(target_path)
                referenced = _load_json(target_path)
                resolved = _resolve_refs(referenced, os.path.dirname(target_path), visited)
                return resolved
        return {k: _resolve_refs(v, current_dir, visited) for k, v in node.items()}
    if isinstance(node, list):
        return [_resolve_refs(item, current_dir, visited) for item in node]
    return node


def load_schema(name: str) -> Dict[str, Any]:
    """
    Load a schema JSON by filename (without extension) from this package directory.
    Inlines local file $ref references so it's self-contained for validators.
    """
    base_dir = os.path.dirname(__file__)
    parts = name.split("/")
    path = os.path.join(base_dir, *parts) + ".json"
    raw = _load_json(path)
    return _resolve_refs(raw, os.path.dirname(path), visited=set())
