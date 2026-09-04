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


def compose_ebnf_filter_local(query: str) -> EBNFFilterResult:
    """Extract filter conditions and compose an EBNF filter locally WITHOUT calling Gemini.

    This local rule-based extractor uses regex pattern matching and search operator syntax:
    - Zero API cost ($0)
    - Sub-millisecond latency (< 1ms)
    - 100% deterministic evaluation
    - No external network or credentials needed

    Supports:
    - Search syntax: filetype:pdf, author:"John Doe", dept:HR, year:>=2024, status:draft
    - Natural language (Korean/English):
      - File formats (PDF, Word, Excel, PPT, etc.)
      - Years and date ranges (2024년 이후, from 2023, 2022~2024년, etc.)
      - Departments & disjunctions (HR or Legal, 인사 또는 법무)
      - Authors (by John Doe, 작성자: 홍길동)
      - Status & negation (draft 제외, not draft)

    Args:
        query: User input query string.

    Returns:
        EBNFFilterResult with synthesized EBNF filter, clean query, attributes, and latency.
    """
    start = time.perf_counter()
    working_text = query
    clauses: List[str] = []
    attributes: dict[str, Any] = {}

    # 1. Search Operator Syntax (e.g. filetype:pdf, author:"John Doe", year:>=2024)
    op_pattern = re.compile(r'(?:(\b\w+):("([^"]+)"|(\S+)))')
    found_ops = []
    for m in op_pattern.finditer(working_text):
        key, full_val, quoted, unquoted = m.group(1).lower(), m.group(2), m.group(3), m.group(4)
        val = quoted if quoted is not None else unquoted
        if key in ("filetype", "type", "ext", "format"):
            clauses.append(f'file_type = "{val.lower()}"')
            attributes["file_type"] = val.lower()
            found_ops.append(m.group(0))
        elif key in ("author", "owner", "creator"):
            clauses.append(f'author = "{val}"')
            attributes["author"] = val
            found_ops.append(m.group(0))
        elif key in ("department", "dept", "team"):
            clauses.append(f'department = "{val}"')
            attributes["department"] = val
            found_ops.append(m.group(0))
        elif key in ("year", "date"):
            if val.startswith((">=", "<=", ">", "<", "!=")):
                op = val[:2] if val.startswith((">=", "<=", "!=")) else val[:1]
                num = val[len(op):]
                clauses.append(f"year {op} {num}")
                attributes["year"] = f"{op} {num}"
            else:
                clauses.append(f"year = {val}")
                attributes["year"] = val
            found_ops.append(m.group(0))
        elif key in ("status", "priority", "category", "tag"):
            clauses.append(f'{key} = "{val}"')
            attributes[key] = val
            found_ops.append(m.group(0))

    for op in found_ops:
        working_text = working_text.replace(op, "")

    # 2. File type detection in natural language
    filetype_match = re.search(r"(?i)\b(pdf|docx?|xlsx?|pptx?|csv|txt|json|html)\b|(워드|엑셀|파워포인트)", working_text)
    if filetype_match and "file_type" not in attributes:
        val = filetype_match.group(0).lower()
        mapping = {"워드": "docx", "엑셀": "xlsx", "파워포인트": "pptx"}
        ft = mapping.get(val, val)
        clauses.append(f'file_type = "{ft}"')
        attributes["file_type"] = ft
        working_text = re.sub(r"(?i)\b(pdf|docx?|xlsx?|pptx?|csv|txt|json|html)\s*(?:파일|문서)?|(워드|엑셀|파워포인트)\s*(?:파일|문서)?", "", working_text)

    # 3. Year / Date detection
    year_range = re.search(r"(\d{4})\s*(?:년)?\s*(?:~|-|부터|에서)\s*(\d{4})\s*(?:년)?(?:\s*사이)?|\b(?:between)\s*(\d{4})\s*(?:and|-)\s*(\d{4})\b", working_text, re.IGNORECASE)
    if year_range and "year" not in attributes:
        y1 = year_range.group(1) or year_range.group(3)
        y2 = year_range.group(2) or year_range.group(4)
        clauses.append(f"year >= {y1} AND year <= {y2}")
        attributes["year"] = f"{y1}..{y2}"
        working_text = working_text.replace(year_range.group(0), "")
    elif "year" not in attributes:
        year_gte = re.search(r"(\d{4})\s*년?\s*(?:이후|부터|이상)|\b(?:from|after|since)\s*(\d{4})\b", working_text, re.IGNORECASE)
        if year_gte:
            y = year_gte.group(1) or year_gte.group(2)
            clauses.append(f"year >= {y}")
            attributes["year"] = f">= {y}"
            working_text = working_text.replace(year_gte.group(0), "")
        else:
            year_lte = re.search(r"(\d{4})\s*년?\s*(?:이전|까지|이하)|\b(?:before|until|prior to)\s*(\d{4})\b", working_text, re.IGNORECASE)
            if year_lte:
                y = year_lte.group(1) or year_lte.group(2)
                clauses.append(f"year <= {y}")
                attributes["year"] = f"<= {y}"
                working_text = working_text.replace(year_lte.group(0), "")

    # 4. Department disjunction (e.g. HR or Legal, 인사 또는 법무)
    dept_disjunction = re.search(r"\b(HR|Legal|Finance|Engineering|Marketing|Sales)\s*(?:or|또는|혹은|\/)\s*(HR|Legal|Finance|Engineering|Marketing|Sales)\b|\b(인사|법무|재무|개발|영업)\s*(?:또는|혹은|\/)\s*(인사|법무|재무|개발|영업)\b", working_text, re.IGNORECASE)
    if dept_disjunction and "department" not in attributes:
        d1 = dept_disjunction.group(1) or dept_disjunction.group(3)
        d2 = dept_disjunction.group(2) or dept_disjunction.group(4)
        clauses.append(f'department: ANY("{d1}", "{d2}")')
        attributes["department"] = [d1, d2]
        working_text = working_text.replace(dept_disjunction.group(0), "")

    # 5. Author in natural language (e.g. by John Doe, 작성자: 홍길동, 홍길동이 작성한)
    author_match = re.search(r"(?:by|authored by)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)|작성자\s*[:=]?\s*([가-힣a-zA-Z]+)|([가-힣a-zA-Z]+)\s*(?:이|가)?\s*작성한", working_text)
    if author_match and "author" not in attributes:
        author_name = author_match.group(1) or author_match.group(2) or author_match.group(3)
        if author_name and author_name.lower() not in ("pdf", "word", "excel"):
            clauses.append(f'author = "{author_name.strip()}"')
            attributes["author"] = author_name.strip()
            working_text = working_text.replace(author_match.group(0), "")

    # 6. Status & Negation (e.g. not draft, 초안 제외)
    neg_status = re.search(r"(?:not|excluding|except)\s*(draft|archived|resolved)|\b(draft|초안|임시)\s*(?:제외|말고|아닌)", working_text, re.IGNORECASE)
    if neg_status and "status" not in attributes:
        s = neg_status.group(1) or neg_status.group(2)
        mapping = {"초안": "draft", "임시": "draft"}
        st = mapping.get(s, s)
        clauses.append(f'NOT status = "{st}"')
        attributes["status"] = f"NOT {st}"
        working_text = working_text.replace(neg_status.group(0), "")

    # Clean up remaining text to form clean_query
    clean = re.sub(r"[에|을|를|의|에서|로|으로]\b", " ", working_text)
    clean = re.sub(r"\b(찾아줘|검색해줘|보여줘|알려줘|작성된|생성된|문서|파일|find|show me|search for|look for|get me)\b", " ", clean, flags=re.IGNORECASE)
    clean = re.sub(r"\s+", " ", clean).strip()

    ebnf_filter = " AND ".join(clauses)
    elapsed = time.perf_counter() - start

    return EBNFFilterResult(
        raw_query=query,
        clean_query=clean,
        ebnf_filter=ebnf_filter,
        attributes=attributes,
        explanation="Synthesized locally via rule-based regex and search operator extraction (zero API calls).",
        latency_seconds=round(elapsed, 4),
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
    # Check for --local flag
    use_only_local = "--local" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--local"]
    if args:
        query = args[0]

    # Step 1: Local Rule-Based EBNF Filter Extraction (Zero API calls, <1ms)
    print("⚡ [Approach 1] Local Rule-Based Extraction (No LLM Call, <1ms):")
    local_result = compose_ebnf_filter_local(query)
    print(format_ebnf_filter_banner(local_result))
    print()

    # Step 2: AI-Powered EBNF Filter Extraction via Gemini 3.5 Flash Lite
    if not use_only_local:
        print("🤖 [Approach 2] Gemini 3.5 Flash Lite AI Extraction:")
        try:
            filter_result = compose_ebnf_filter(query)
            print(format_ebnf_filter_banner(filter_result))
            print()
        except Exception as e:
            print(f"⚠️ Filter composition warning: {e}\n", file=sys.stderr)
            filter_result = local_result
    else:
        filter_result = local_result

    # Step 3: Programmatic Builder Demonstration
    print("🛠️  [Approach 3] Programmatic EBNFFilterBuilder:")
    demo_filter = (
        EBNFFilterBuilder()
        .equals("file_type", "pdf")
        .greater_or_equal("year", 2024)
        .any_of("category", ["finance", "accounting"])
        .build()
    )
    print(f"  • Programmatically built filter: {demo_filter}\n")

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
