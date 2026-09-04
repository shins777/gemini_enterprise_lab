#!/usr/bin/env python3
"""Direct Vertex AI Gemini 3.5 Flash Lite Caller with EBNF Filter Composer.

This module provides:
1. Direct calls to the `gemini-3.5-flash-lite` foundation model on Google Cloud Vertex AI
   with streaming, low latency (<2s), and auto-authentication.
2. Extended Backus-Naur Form (EBNF) programmatic filter builder and classes
   strictly conforming to Google Cloud Discovery Engine & Vertex AI Search AIP-160 filter grammar.
3. Automated EBNF filter composition from natural language user queries using
   Gemini 3.5 Flash Lite (extracting clean search query, metadata attributes, and EBNF filter).
"""

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
import json
import os
import re
import subprocess
import sys
import time
from typing import Any, Generator, List, Optional, Sequence, Union

from google import genai
from google.genai import types
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# Configuration defaults
DEFAULT_PROJECT = os.getenv("GCP_PROJECT", "ai-hangsik")
DEFAULT_LOCATION = os.getenv("GEMINI_LOCATION", "global")  # gemini-3.5-flash-lite is hosted in 'global'
DEFAULT_MODEL = "gemini-3.5-flash-lite"


# ==============================================================================
# 1. Extended Backus-Naur Form (EBNF) Grammar Specification
# ==============================================================================
EBNF_FILTER_GRAMMAR = """
(* Formal Extended Backus-Naur Form (EBNF) for Google Cloud Discovery Engine & Vertex AI Search *)

filter               ::= expression ?
expression           ::= sequence ('OR' sequence)*
sequence             ::= factor ('AND' factor)*
factor               ::= term | ('NOT' | '-') factor
term                 ::= simple_condition | '(' expression ')'
simple_condition     ::= comparison | text_restriction | any_function
comparison           ::= field comparator value
comparator           ::= '=' | '!=' | '<=' | '<' | '>=' | '>'
text_restriction     ::= field ':' text_value
any_function         ::= field ':' 'ANY' '(' value_list ')'
value_list           ::= value (',' value)*
field                ::= identifier ('.' identifier)*
value                ::= string_literal | number_literal | boolean_literal | timestamp_literal
string_literal       ::= '"' [^"]* '"'
number_literal       ::= ['-']? [0-9]+ ('.' [0-9]+)?
boolean_literal      ::= 'true' | 'false'
timestamp_literal    ::= '"' [0-9]{4} '-' [0-9]{2} '-' [0-9]{2} ('T' [0-9]{2} ':' [0-9]{2} ':' [0-9]{2} ('Z' | ('+' | '-') [0-9]{2} ':' [0-9]{2}))? '"'
"""


# ==============================================================================
# 2. Programmatic EBNF Filter Classes & Builder
# ==============================================================================
def _format_ebnf_value(value: Any) -> str:
    """Format a Python value into a valid EBNF literal."""
    if isinstance(value, bool):
        return "true" if value else "false"
    elif isinstance(value, (int, float)):
        return str(value)
    else:
        # String / timestamp: double-quote with escaping
        s = str(value).replace('"', '\\"')
        return f'"{s}"'


class EBNFExpression(ABC):
    """Abstract base class for all EBNF filter expressions."""

    @abstractmethod
    def to_ebnf(self) -> str:
        """Serialize expression into valid Discovery Engine EBNF filter syntax."""
        pass

    def __str__(self) -> str:
        return self.to_ebnf()

    def __and__(self, other: "EBNFExpression") -> "LogicalAnd":
        return LogicalAnd([self, other])

    def __or__(self, other: "EBNFExpression") -> "LogicalOr":
        return LogicalOr([self, other])

    def __invert__(self) -> "LogicalNot":
        return LogicalNot(self)


class Comparison(EBNFExpression):
    """EBNF Comparison: field operator value (e.g. year >= 2024, file_type = "pdf")."""

    VALID_OPS = {"=", "!=", "<", "<=", ">", ">="}

    def __init__(self, field_name: str, operator: str, value: Any):
        if operator not in self.VALID_OPS:
            raise ValueError(f"Invalid comparator '{operator}'. Must be one of {self.VALID_OPS}")
        self.field_name = field_name.strip()
        self.operator = operator
        self.value = value

    def to_ebnf(self) -> str:
        formatted_val = _format_ebnf_value(self.value)
        return f"{self.field_name} {self.operator} {formatted_val}"


class TextRestriction(EBNFExpression):
    """EBNF Text containment restriction: field: "value" (e.g. department: "Finance")."""

    def __init__(self, field_name: str, value: str):
        self.field_name = field_name.strip()
        self.value = value

    def to_ebnf(self) -> str:
        formatted_val = _format_ebnf_value(self.value)
        return f"{self.field_name}: {formatted_val}"


class AnyFunction(EBNFExpression):
    """EBNF ANY function: field: ANY("val1", "val2") (e.g. tag: ANY("AI", "ML"))."""

    def __init__(self, field_name: str, values: Sequence[Any]):
        self.field_name = field_name.strip()
        self.values = list(values)

    def to_ebnf(self) -> str:
        val_str = ", ".join(_format_ebnf_value(v) for v in self.values)
        return f"{self.field_name}: ANY({val_str})"


class LogicalAnd(EBNFExpression):
    """EBNF Conjunction: expr1 AND expr2 AND expr3."""

    def __init__(self, expressions: Sequence[EBNFExpression]):
        self.expressions: List[EBNFExpression] = []
        for expr in expressions:
            if isinstance(expr, LogicalAnd):
                self.expressions.extend(expr.expressions)
            elif expr:
                self.expressions.append(expr)

    def to_ebnf(self) -> str:
        valid = [e.to_ebnf() for e in self.expressions if e.to_ebnf().strip()]
        if not valid:
            return ""
        return " AND ".join(valid)


class LogicalOr(EBNFExpression):
    """EBNF Disjunction: (expr1 OR expr2)."""

    def __init__(self, expressions: Sequence[EBNFExpression]):
        self.expressions: List[EBNFExpression] = []
        for expr in expressions:
            if isinstance(expr, LogicalOr):
                self.expressions.extend(expr.expressions)
            elif expr:
                self.expressions.append(expr)

    def to_ebnf(self) -> str:
        valid = [e.to_ebnf() for e in self.expressions if e.to_ebnf().strip()]
        if not valid:
            return ""
        if len(valid) == 1:
            return valid[0]
        return f"({' OR '.join(valid)})"


class LogicalNot(EBNFExpression):
    """EBNF Inversion: NOT (expression)."""

    def __init__(self, expression: EBNFExpression):
        self.expression = expression

    def to_ebnf(self) -> str:
        inner = self.expression.to_ebnf().strip()
        if not inner:
            return ""
        if " " in inner and not (inner.startswith("(") and inner.endswith(")")):
            return f"NOT ({inner})"
        return f"NOT {inner}"


class EBNFFilterBuilder:
    """Fluent Builder for synthesizing Discovery Engine EBNF filter expressions."""

    def __init__(self):
        self._clauses: List[EBNFExpression] = []

    def equals(self, field_name: str, value: Any) -> "EBNFFilterBuilder":
        self._clauses.append(Comparison(field_name, "=", value))
        return self

    def not_equals(self, field_name: str, value: Any) -> "EBNFFilterBuilder":
        self._clauses.append(Comparison(field_name, "!=", value))
        return self

    def greater_than(self, field_name: str, value: Any) -> "EBNFFilterBuilder":
        self._clauses.append(Comparison(field_name, ">", value))
        return self

    def greater_or_equal(self, field_name: str, value: Any) -> "EBNFFilterBuilder":
        self._clauses.append(Comparison(field_name, ">=", value))
        return self

    def less_than(self, field_name: str, value: Any) -> "EBNFFilterBuilder":
        self._clauses.append(Comparison(field_name, "<", value))
        return self

    def less_or_equal(self, field_name: str, value: Any) -> "EBNFFilterBuilder":
        self._clauses.append(Comparison(field_name, "<=", value))
        return self

    def text_match(self, field_name: str, value: str) -> "EBNFFilterBuilder":
        self._clauses.append(TextRestriction(field_name, value))
        return self

    def any_of(self, field_name: str, values: Sequence[Any]) -> "EBNFFilterBuilder":
        self._clauses.append(AnyFunction(field_name, values))
        return self

    def add_custom(self, expression: EBNFExpression) -> "EBNFFilterBuilder":
        self._clauses.append(expression)
        return self

    def clear(self) -> "EBNFFilterBuilder":
        self._clauses.clear()
        return self

    def build(self) -> str:
        """Construct the final EBNF filter string."""
        if not self._clauses:
            return ""
        return LogicalAnd(self._clauses).to_ebnf()


# ==============================================================================
# 3. Filter Result Data Structure
# ==============================================================================
@dataclass
class EBNFFilterResult:
    """Encapsulates the parsed query and synthesized EBNF filter."""

    raw_query: str
    clean_query: str
    ebnf_filter: str
    attributes: dict[str, Any] = field(default_factory=dict)
    explanation: str = ""
    latency_seconds: float = 0.0

    @property
    def has_filter(self) -> bool:
        return bool(self.ebnf_filter and self.ebnf_filter.strip())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=indent)


# ==============================================================================
# 4. Authentication & Client Initialization
# ==============================================================================
def get_credentials() -> Optional[Credentials]:
    """Resolve valid Google Cloud OAuth2 credentials with automatic refresh support."""
    try:
        creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        if not creds.valid:
            creds.refresh(Request())
        return creds
    except Exception:
        pass

    # Fallback to token environment variable or gcloud CLI
    token = os.getenv("CLOUDSDK_AUTH_ACCESS_TOKEN") or os.getenv("GOOGLE_ACCESS_TOKEN")
    if not token:
        try:
            output = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip()
            # Extract only the token line in case of proxy/cert logs
            for line in output.splitlines():
                line = line.strip()
                if line.startswith("ya29."):
                    token = line
                    break
            if not token and output:
                token = output.splitlines()[-1].strip()
        except Exception:
            token = None

    if token:
        return Credentials(token=token)
    return None


def get_genai_client(
    project_id: str = DEFAULT_PROJECT,
    location: str = DEFAULT_LOCATION,
) -> genai.Client:
    """Initialize a Google GenAI Client targeting Vertex AI with resilient auth."""
    creds = get_credentials()
    if creds:
        return genai.Client(
            vertexai=True,
            project=project_id,
            location=location,
            credentials=creds,
        )
    return genai.Client(
        vertexai=True,
        project=project_id,
        location=location,
    )


# ==============================================================================
# 5. Automated EBNF Filter Composition via Gemini 3.5 Flash Lite
# ==============================================================================
EBNF_COMPOSER_SYSTEM_INSTRUCTION = """You are a specialized query analyzer and filter generator for Google Cloud Discovery Engine and Vertex AI Search.
Your task is to analyze natural language user queries (in Korean, English, or any language), extract metadata filtering constraints, and synthesize an Extended Backus-Naur Form (EBNF) filter expression strictly conforming to the Google Cloud Discovery Engine filter grammar.

### Discovery Engine EBNF Filter Rules:
1. Filter Syntax (AIP-160):
   - filter ::= expression
   - expression ::= sequence ("OR" sequence)*
   - sequence ::= factor ("AND" factor)*
   - factor ::= term | "NOT" factor | "-" factor
   - term ::= comparison | text_restriction | any_function | "(" expression ")"
2. Comparisons:
   - field comparator value where comparator is one of: =, !=, <, <=, >, >=
   - Numeric values are unquoted: 2024, 100, 4.5
   - String values MUST be enclosed in double quotes: "pdf", "John Doe"
   - Booleans are unquoted: true, false
3. Text Match & ANY:
   - field: "value" (containment/search in field)
   - field: ANY("val1", "val2") (matches any in list)
4. Common Recognized Fields:
   - file_type: "pdf", "docx", "xlsx", "pptx", etc.
   - year: integer (e.g. >= 2024, 2023)
   - date / created_time: ISO-8601 string (e.g. >= "2024-01-01")
   - author / owner: person name string
   - department: "HR", "Legal", "Finance", "Engineering", etc.
   - category: document classification (e.g. "financial_report", "policy")
   - tag: keyword labels
   - status: "draft", "published", "archived", "resolved", etc.
   - priority: "high", "medium", "low"
5. Operators:
   - Conjunctions: AND, OR, NOT (must be uppercase)
   - Grouping: Always wrap OR expressions in parentheses when combined with AND, e.g. (dept = "HR" OR dept = "Legal") AND status = "active".

### Output Requirement:
Respond ONLY with a JSON object containing:
- clean_query: string (The core semantic search query with filter keywords removed).
- ebnf_filter: string (The synthesized EBNF filter string. Return empty string "" if the query contains NO filtering constraints).
- attributes: dict (Key-value mapping of extracted metadata fields and conditions).
- explanation: string (Brief 1-sentence explanation of why the filter was composed).
"""


def compose_ebnf_filter(
    query: str,
    model: str = DEFAULT_MODEL,
    project_id: str = DEFAULT_PROJECT,
    location: str = DEFAULT_LOCATION,
    temperature: float = 0.0,
) -> EBNFFilterResult:
    """Analyze a natural language query and compose an EBNF filter using Gemini 3.5 Flash Lite.

    Args:
        query: User input query string (natural language in any language).
        model: Model ID to use for extraction (defaults to 'gemini-3.5-flash-lite').
        project_id: Google Cloud project ID.
        location: Vertex AI location (defaults to 'global').
        temperature: Sampling temperature (0.0 for deterministic extraction).

    Returns:
        EBNFFilterResult containing clean query, EBNF filter expression, attributes, and latency.
    """
    client = get_genai_client(project_id=project_id, location=location)

    prompt = f"Analyze and synthesize an EBNF filter for user query:\n\n\"{query}\""

    config = types.GenerateContentConfig(
        system_instruction=EBNF_COMPOSER_SYSTEM_INSTRUCTION,
        response_mime_type="application/json",
        temperature=temperature,
    )

    start_time = time.perf_counter()
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )
    elapsed = time.perf_counter() - start_time

    raw_text = response.text.strip() if response.text else "{}"

    # Parse JSON output
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError:
        # Fallback regex extraction if markdown fences exist
        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
        else:
            data = {"clean_query": query, "ebnf_filter": "", "attributes": {}, "explanation": raw_text}

    return EBNFFilterResult(
        raw_query=query,
        clean_query=data.get("clean_query", query),
        ebnf_filter=data.get("ebnf_filter", ""),
        attributes=data.get("attributes", {}),
        explanation=data.get("explanation", ""),
        latency_seconds=round(elapsed, 3),
    )


def format_ebnf_filter_banner(result: EBNFFilterResult) -> str:
    """Format an EBNFFilterResult into a clear, readable terminal display."""
    lines = [
        "┌" + "─" * 70 + "┐",
        "│ 🧩 AUTOMATIC EBNF FILTER COMPOSITION (Discovery Engine Syntax)      │",
        "├" + "─" * 70 + "┤",
        f"│  • Input Query:    {result.raw_query[:52]}",
        f"│  • Clean Query:    {result.clean_query[:52]}",
        f"│  • EBNF Filter:    {result.ebnf_filter if result.ebnf_filter else '(None - semantic query only)'}",
    ]
    if result.attributes:
        attr_str = ", ".join(f"{k}={v}" for k, v in result.attributes.items())
        lines.append(f"│  • Attributes:     {attr_str[:52]}")
    if result.explanation:
        lines.append(f"│  • Explanation:    {result.explanation[:52]}")
    lines.append(f"│  • Latency:        {result.latency_seconds:.3f}s")
    lines.append("└" + "─" * 70 + "┘")
    return "\n".join(lines)


# ==============================================================================
# 6. Content Generation & Streaming
# ==============================================================================
def generate_content(
    prompt: str,
    model: str = DEFAULT_MODEL,
    project_id: str = DEFAULT_PROJECT,
    location: str = DEFAULT_LOCATION,
    temperature: float = 0.7,
) -> dict:
    """Call Gemini 3.5 Flash Lite directly and return text with latency metrics."""
    client = get_genai_client(project_id=project_id, location=location)

    config = types.GenerateContentConfig(
        temperature=temperature,
    )

    start_time = time.perf_counter()
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )
    total_time = time.perf_counter() - start_time

    return {
        "text": response.text,
        "model": model,
        "latency_seconds": round(total_time, 3),
        "usage": {
            "prompt_token_count": getattr(response.usage_metadata, "prompt_token_count", None),
            "candidates_token_count": getattr(response.usage_metadata, "candidates_token_count", None),
        },
    }


def stream_content(
    prompt: str,
    model: str = DEFAULT_MODEL,
    project_id: str = DEFAULT_PROJECT,
    location: str = DEFAULT_LOCATION,
    temperature: float = 0.7,
) -> Generator[str, None, None]:
    """Stream Gemini 3.5 Flash Lite responses chunk-by-chunk in real-time with resilient fallback."""
    client = get_genai_client(project_id=project_id, location=location)

    config = types.GenerateContentConfig(
        temperature=temperature,
    )

    # Note: google-genai SDK 2.17.0 has an SSE chunk boundary issue with multi-byte UTF-8
    # characters (e.g. Korean / CJK) in request_streamed. For non-ASCII prompts/outputs,
    # generate_content provides 100% reliable responses without SSE decode errors.
    has_non_ascii = any(ord(c) > 127 for c in prompt)
    if has_non_ascii:
        res = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )
        if res.text:
            yield res.text
        return

    try:
        response_stream = client.models.generate_content_stream(
            model=model,
            contents=prompt,
            config=config,
        )
        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
    except Exception:
        res = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )
        if res.text:
            yield res.text


# ==============================================================================
# 7. Main CLI Execution
# ==============================================================================
if __name__ == "__main__":
    # Default query demonstrating EBNF filter extraction if no CLI argument given
    query = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "2024년 이후에 작성된 재무 보고서 PDF 파일을 찾아줘"
    )

    print("\n" + "=" * 72)
    print(f"🚀 Gemini 3.5 Flash Lite: EBNF Filter Synthesis & Model Execution")
    print(f"Target Model:    {DEFAULT_MODEL}")
    print(f"Vertex Location: {DEFAULT_LOCATION}")
    print("=" * 72 + "\n")

    # Step 1: Automatic EBNF Filter Composition
    print("⏳ Analyzing query and composing Extended Backus-Naur Form filter...\n")
    try:
        filter_result = compose_ebnf_filter(query)
        print(format_ebnf_filter_banner(filter_result))
        print()

        # Step 2: Programmatic Builder Demonstration
        print("🛠️  Programmatic EBNFFilterBuilder Demonstration:")
        demo_filter = (
            EBNFFilterBuilder()
            .equals("file_type", "pdf")
            .greater_or_equal("year", 2024)
            .any_of("category", ["finance", "accounting"])
            .build()
        )
        print(f"  • Programmatically built filter: {demo_filter}\n")

    except Exception as e:
        print(f"⚠️ Filter composition warning: {e}\n", file=sys.stderr)
        filter_result = EBNFFilterResult(raw_query=query, clean_query=query, ebnf_filter="")

    # Step 3: Stream Gemini 3.5 Flash Lite Response
    print(f"💬 Generating Response for: '{filter_result.clean_query}'")
    print("-" * 72)

    start_time = time.perf_counter()
    first_token_time = None

    try:
        for text_chunk in stream_content(
            f"Please answer the user's request: {query} (Semantic search focus: {filter_result.clean_query})"
        ):
            if first_token_time is None:
                first_token_time = time.perf_counter() - start_time
            print(text_chunk, end="", flush=True)

        total_time = time.perf_counter() - start_time
        ttft = first_token_time if first_token_time is not None else total_time

        print("\n\n" + "-" * 45)
        print("⏱️  Latency Metrics:")
        print(f"  • Filter Composition Latency: {filter_result.latency_seconds:.3f}s")
        print(f"  • Time to First Token (TTFT): {ttft:.3f}s")
        print(f"  • Total Stream Latency:      {total_time:.3f}s")
        print("-" * 45 + "\n")

    except Exception as e:
        print(f"\n\n❌ Error calling {DEFAULT_MODEL}: {e}", file=sys.stderr)
        sys.exit(1)
