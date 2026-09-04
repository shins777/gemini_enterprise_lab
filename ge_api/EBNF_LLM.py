#!/usr/bin/env python3
"""EBNF Search Filter Extractor powered by Gemini 3.5 Flash Lite.

Uses Gemini 3.5 Flash Lite to extract search filter conditions (문서종류, 문서 타입, 작성자, 작성 일자)
from natural language queries via prompting and synthesize an Extended Backus-Naur Form (EBNF) filter.
"""

import json
import os
import subprocess
import sys
from typing import Any, Dict

import google.auth
from google.auth.transport.requests import Request
from google import genai
from google.genai import types
from google.oauth2.credentials import Credentials

DEFAULT_PROJECT = os.getenv("GCP_PROJECT", "ai-hangsik")
DEFAULT_LOCATION = os.getenv("GEMINI_LOCATION", "global")
DEFAULT_MODEL = "gemini-3.5-flash-lite"

SYSTEM_PROMPT = """You are an expert search filter parser for Google Cloud Discovery Engine & Vertex AI Search.
Extract metadata constraints from the user query and synthesize an Extended Backus-Naur Form (EBNF) filter.

Target Fields to Extract:
- 문서종류 (category): e.g. "재무 보고서", "보안 감사 보고서", "기획서" -> category = "..."
- 문서 타입 (file_type): e.g. "pdf", "docx", "xlsx" -> file_type = "..."
- 작성자 (author): e.g. "홍길동", "John Doe" -> author = "..."
- 작성 일자 (year / date): e.g. "2024년 이후" -> year >= 2024, "2023년" -> year = 2023

EBNF Syntax Rules:
- Combine conditions with uppercase AND.
- Strings in double quotes, numbers unquoted.

Respond ONLY with valid JSON:
{
  "clean_query": "<core search query without filters>",
  "ebnf_filter": "<synthesized EBNF filter string>",
  "extracted_info": {
    "문서종류": "<value or null>",
    "문서 타입": "<value or null>",
    "작성자": "<value or null>",
    "작성 일자": "<value or null>"
  }
}"""


def get_genai_client(project_id: str = DEFAULT_PROJECT) -> genai.Client:
    """Initialize a Vertex AI GenAI Client with resilient authentication."""
    creds = None
    try:
        creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        if not creds.valid:
            creds.refresh(Request())
    except Exception:
        token = os.getenv("CLOUDSDK_AUTH_ACCESS_TOKEN") or os.getenv("GOOGLE_ACCESS_TOKEN")
        if not token:
            try:
                token = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip().splitlines()[-1]
            except Exception:
                pass
        if token:
            creds = Credentials(token=token)

    return genai.Client(
        vertexai=True,
        project=project_id,
        location=DEFAULT_LOCATION,
        credentials=creds,
    )


def extract_ebnf_with_llm(query: str, project_id: str = DEFAULT_PROJECT) -> Dict[str, Any]:
    """Extract filter conditions from query and compose an EBNF filter using Gemini 3.5 Flash Lite."""
    client = get_genai_client(project_id=project_id)

    response = client.models.generate_content(
        model=DEFAULT_MODEL,
        contents=f"Analyze and extract EBNF filter for query: {query}",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            response_mime_type="application/json",
            temperature=0.0,
        ),
    )

    try:
        return json.loads(response.text)
    except Exception:
        return {"raw_response": response.text, "clean_query": query, "ebnf_filter": ""}


if __name__ == "__main__":
    query = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "2024년 이후에 작성된 재무 보고서 PDF 파일을 찾아줘"
    )

    print("\n" + "=" * 65)
    print(f"🚀 Gemini 3.5 Flash Lite - EBNF Filter Extractor")
    print(f"Model: {DEFAULT_MODEL} (Location: {DEFAULT_LOCATION})")
    print(f"Query: {query}")
    print("=" * 65 + "\n")

    result = extract_ebnf_with_llm(query)

    print("📋 Extracted Filter Information (주어진 조건 정보):")
    for key, val in result.get("extracted_info", {}).items():
        if val:
            print(f"  • {key:10}: {val}")

    print(f"\n🎯 Clean Query (검색어): {result.get('clean_query')}")
    print(f"\n👉 EBNF Filter (조합된 EBNF 필터):\n{result.get('ebnf_filter')}\n")
