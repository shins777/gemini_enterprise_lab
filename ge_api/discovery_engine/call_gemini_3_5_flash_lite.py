#!/usr/bin/env python3
"""Call Gemini 3.5 Flash Lite via Google Cloud Discovery Engine API.

This script demonstrates how to call the Discovery Engine AssistantService.StreamAssist API
with `generationSpec.modelId` set to `gemini-3.5-flash-lite`.
Includes automatic credential resolution, real-time streaming, latency benchmarking, and fallback handling.
"""

import json
import os
import subprocess
import sys
import time
from typing import Generator, Optional
import requests

# Locate and load .env configuration
def _load_env():
    for env_candidate in [
        os.path.join(os.path.dirname(__file__), ".env"),
        os.path.join(os.path.dirname(__file__), "..", "stream_assist", ".env"),
    ]:
        if os.path.exists(env_candidate):
            try:
                from dotenv import load_dotenv
                load_dotenv(env_candidate)
                break
            except ImportError:
                with open(env_candidate, "r") as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            k, v = line.split("=", 1)
                            os.environ.setdefault(k.strip(), v.strip().strip("'\""))
                break

_load_env()

DEFAULT_PROJECT = os.getenv("GCP_PROJECT", "ai-hangsik")
DEFAULT_LOCATION = os.getenv("GCP_LOCATION", "global")
DEFAULT_COLLECTION = os.getenv("GE_COLLECTION_ID", "default_collection")
DEFAULT_ENGINE = os.getenv("GE_ENGINE_ID", "gemini-enterprise-july-202_1782612363846")
DEFAULT_ASSISTANT = os.getenv("GE_ASSISTANT_ID", "default_assistant")
DEFAULT_MODEL = "gemini-3.5-flash-lite"


def get_access_token() -> str:
    """Resolve Google Cloud OAuth2 access token via environment, ADC, or gcloud CLI."""
    token = os.getenv("CLOUDSDK_AUTH_ACCESS_TOKEN") or os.getenv("GOOGLE_ACCESS_TOKEN")
    if token:
        return token.strip()
    try:
        import google.auth
        from google.auth.transport.requests import Request

        creds, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
        creds.refresh(Request())
        return creds.token
    except Exception:
        return subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip()


def call_discovery_engine_stream(
    query: str,
    model_id: str = DEFAULT_MODEL,
    project_id: str = DEFAULT_PROJECT,
    location: str = DEFAULT_LOCATION,
    collection_id: str = DEFAULT_COLLECTION,
    engine_id: str = DEFAULT_ENGINE,
    assistant_id: str = DEFAULT_ASSISTANT,
    session_id: Optional[str] = None,
    timeout: float = 120.0,
) -> Generator[dict, None, None]:
    """Call Discovery Engine streamAssist API with generationSpec modelId.

    Args:
        query: User question or prompt text.
        model_id: Foundation model ID to override via generationSpec (e.g. 'gemini-3.5-flash-lite').
        project_id: Google Cloud project ID.
        location: Discovery Engine location (e.g. 'global').
        collection_id: Discovery Engine collection ID (e.g. 'default_collection').
        engine_id: Discovery Engine / Gemini Enterprise app ID.
        assistant_id: Assistant ID (e.g. 'default_assistant').
        session_id: Optional session identifier for multi-turn history.
        timeout: HTTP request timeout in seconds.

    Yields:
        Parsed chunk dictionaries as they arrive over the HTTP response stream.
    """
    endpoint = (
        "https://discoveryengine.googleapis.com"
        if location == "global"
        else f"https://{location}-discoveryengine.googleapis.com"
    )
    resource = (
        f"projects/{project_id}/locations/{location}/"
        f"collections/{collection_id}/engines/{engine_id}/assistants/{assistant_id}"
    )
    url = f"{endpoint}/v1alpha/{resource}:streamAssist"

    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json",
        "X-Goog-User-Project": project_id,
    }

    payload = {
        "query": {"text": query},
        "toolsSpec": {
            "webGroundingSpec": {},
            "vertexAiSearchSpec": {},
        },
    }

    # Set generationSpec modelId for Discovery Engine
    if model_id:
        payload["generationSpec"] = {"modelId": model_id}

    if session_id:
        payload["session"] = (
            session_id
            if "/" in session_id
            else f"projects/{project_id}/locations/{location}/collections/{collection_id}/engines/{engine_id}/sessions/{session_id}"
        )

    start_time = time.perf_counter()
    response = requests.post(url, headers=headers, json=payload, stream=True, timeout=timeout)

    if response.status_code != 200:
        error_text = response.text
        try:
            err_json = json.loads(error_text)
            if isinstance(err_json, list) and len(err_json) > 0 and "error" in err_json[0]:
                error_msg = err_json[0]["error"].get("message", error_text)
            elif isinstance(err_json, dict) and "error" in err_json:
                error_msg = err_json["error"].get("message", error_text)
            else:
                error_msg = error_text
        except Exception:
            error_msg = error_text
        raise RuntimeError(f"Discovery Engine API Error [{response.status_code}]: {error_msg}")

    # Parse streaming JSON array chunks from HTTP response
    decoder = json.JSONDecoder()
    buffer = ""
    for raw in response.iter_content(chunk_size=1024, decode_unicode=True):
        if not raw:
            continue
        buffer += raw
        while buffer:
            buffer = buffer.lstrip("[\n\r\t ,]")
            if not buffer or buffer.startswith("]"):
                break
            try:
                obj, idx = decoder.raw_decode(buffer)
                buffer = buffer[idx:]
                obj["_elapsed_seconds"] = round(time.perf_counter() - start_time, 3)
                yield obj
            except json.JSONDecodeError:
                break


def call_discovery_engine(
    query: str,
    model_id: str = DEFAULT_MODEL,
    **kwargs
) -> dict:
    """Call Discovery Engine API and aggregate the full response with latency metrics."""
    start_time = time.perf_counter()
    first_token_time = None
    text_parts = []
    documents = []
    session_id = None

    for chunk in call_discovery_engine_stream(query, model_id=model_id, **kwargs):
        if "sessionInfo" in chunk and "session" in chunk["sessionInfo"]:
            session_id = chunk["sessionInfo"]["session"].split("/")[-1]

        answer = chunk.get("answer", {})
        for reply in answer.get("replies", []):
            grounded = reply.get("groundedContent", {})
            content = grounded.get("content", {})
            if "text" in content and not content.get("thought", False):
                if first_token_time is None:
                    first_token_time = time.perf_counter() - start_time
                text_parts.append(content["text"])

            meta = grounded.get("textGroundingMetadata", {})
            for ref in meta.get("references", []):
                doc_meta = ref.get("documentMetadata", {})
                doc = {
                    "title": doc_meta.get("title", ""),
                    "uri": doc_meta.get("uri", ""),
                    "domain": doc_meta.get("domain", ""),
                    "snippet": ref.get("content", ""),
                }
                if doc not in documents:
                    documents.append(doc)

    total_time = time.perf_counter() - start_time
    return {
        "text": "".join(text_parts),
        "model": model_id,
        "documents": documents,
        "session_id": session_id,
        "latency": {
            "time_to_first_token_seconds": round(first_token_time, 3) if first_token_time else round(total_time, 3),
            "total_latency_seconds": round(total_time, 3),
        },
    }


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Introduce yourself and what you can do."
    model_to_use = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_MODEL

    print("=" * 70)
    print(f"🔍 Google Cloud Discovery Engine API Call")
    print(f"Target Model (generationSpec.modelId): {model_to_use}")
    print(f"Project: {DEFAULT_PROJECT} | Location: {DEFAULT_LOCATION}")
    print(f"Engine ID: {DEFAULT_ENGINE}")
    print(f"Prompt: {prompt}")
    print("=" * 70 + "\n")

    start_time = time.perf_counter()
    first_token_time = None

    print("Response: ", end="", flush=True)
    try:
        for chunk in call_discovery_engine_stream(prompt, model_id=model_to_use):
            for reply in chunk.get("answer", {}).get("replies", []):
                text = reply.get("groundedContent", {}).get("content", {}).get("text", "")
                if text:
                    if first_token_time is None:
                        first_token_time = time.perf_counter() - start_time
                    print(text, end="", flush=True)

        total_time = time.perf_counter() - start_time
        ttft = first_token_time if first_token_time is not None else total_time

        print("\n\n" + "-" * 45)
        print("⏱️  Latency Metrics:")
        print(f"  • Time to First Token (TTFT): {ttft:.3f}s")
        print(f"  • Total Stream Latency:      {total_time:.3f}s")
        print("-" * 45 + "\n")

    except Exception as e:
        print(f"\n\n❌ Discovery Engine API Error: {e}", file=sys.stderr)
        if "invalid" in str(e).lower() and model_to_use == "gemini-3.5-flash-lite":
            print(
                "\n💡 Note: In Discovery Engine, 'gemini-3.5-flash-lite' is not yet routed through the Assistant API.\n"
                "To test with an active Flash model, run:\n"
                "  python3 ge_api/discovery_engine/call_gemini_3_5_flash_lite.py \"your query\" gemini-3.5-flash\n"
                "Or to call gemini-3.5-flash-lite directly via Vertex AI, run:\n"
                "  python3 ge_api/call_gemini_3_5_flash_lite.py \"your query\"\n"
            )
        sys.exit(1)
