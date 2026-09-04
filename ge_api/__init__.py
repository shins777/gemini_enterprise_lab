"""Gemini Enterprise API Client Suite.
"""

from . import EBNF
from . import EBNF_LLM
from . import discovery_engine
from . import stream_assist
from .EBNF import extract_ebnf_filter
from .EBNF_LLM import (
    EBNFFilterBuilder,
    EBNFFilterResult,
    compose_ebnf_filter,
    compose_ebnf_filter_local,
)

# Backward-compatibility alias
call_gemini_3_5_flash_lite = EBNF_LLM

__all__ = [
    "EBNF",
    "EBNF_LLM",
    "extract_ebnf_filter",
    "stream_assist",
    "discovery_engine",
    "call_gemini_3_5_flash_lite",
    "compose_ebnf_filter",
    "compose_ebnf_filter_local",
    "EBNFFilterBuilder",
    "EBNFFilterResult",
]
