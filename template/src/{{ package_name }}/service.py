"""Side-effect-free service assembly."""

from __future__ import annotations

from typing import Any

import httpx
from fastmcp import FastMCP
from mcp_runtime import RuntimeSettings, create_server


def create_service(
    settings: RuntimeSettings,
    *,
    jwks_transport: httpx.AsyncBaseTransport | None = None,
) -> FastMCP[Any]:
    """Assemble the authenticated private service without starting it."""
    return create_server(settings, jwks_transport=jwks_transport)
