"""Discovery Engine API Integration Module.
"""

from .call_gemini_3_5_flash_lite import (
    call_discovery_engine,
    call_discovery_engine_stream,
    get_access_token,
)

__all__ = [
    "call_discovery_engine",
    "call_discovery_engine_stream",
    "get_access_token",
]
