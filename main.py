"""Compatibility entrypoint for tests and local tooling.

Exposes `load_tool_schemas` and `TOOL_FUNCTIONS` as expected by `test_server.py`.
"""

from weather_api_mcp_server.server import load_tool_schemas, TOOL_FUNCTIONS  # re-export

__all__ = [
    "load_tool_schemas",
    "TOOL_FUNCTIONS",
]
