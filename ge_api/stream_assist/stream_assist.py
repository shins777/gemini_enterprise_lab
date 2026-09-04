#!/usr/bin/env python3
"""Gemini Enterprise Stream Assist Client.

Retrieves streaming answers and grounded enterprise data from Google Cloud
Gemini Enterprise (Discovery Engine AssistantService.StreamAssist API).
"""

import json
import os
import subprocess
import time
import requests

# Automatically load .env configuration if present
_env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(_env_path):
    try:
        from dotenv import load_dotenv
        load_dotenv(_env_path)
    except ImportError:
        with open(_env_path, "r") as _f:
            for _line in _f:
                _line = _line.strip()
                if _line and not _line.startswith("#") and "=" in _line:
                    _k, _v = _line.split("=", 1)
                    os.environ.setdefault(_k.strip(), _v.strip().strip("'\""))

DEFAULT_PROJECT = os.getenv("GCP_PROJECT", "explore-ai-aa934711")
DEFAULT_LOCATION = os.getenv("GCP_LOCATION", "global")
DEFAULT_COLLECTION = os.getenv("GE_COLLECTION_ID", "default_collection")
DEFAULT_ENGINE = os.getenv("GE_ENGINE_ID", "default_engine")
DEFAULT_ASSISTANT = os.getenv("GE_ASSISTANT_ID", "default_assistant")
DEFAULT_MODEL_ID = os.getenv("GE_MODEL_ID", "gemini-3.5-flash")


def get_access_token() -> str:
    """Get Google Cloud OAuth2 access token from env or gcloud CLI."""
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


def stream_assist(
    query: str,
    project_id: str = DEFAULT_PROJECT,
    location: str = DEFAULT_LOCATION,
    collection_id: str = DEFAULT_COLLECTION,
    engine_id: str = DEFAULT_ENGINE,
    assistant_id: str = DEFAULT_ASSISTANT,
    model_id: str = DEFAULT_MODEL_ID,
    session_id: str = None,
):
    """Call Gemini Enterprise streamAssist API and yield response chunks in real-time."""
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
        "toolsSpec": {"webGroundingSpec": {}, "vertexAiSearchSpec": {}},
    }
    if model_id:
        payload["generationSpec"] = {"modelId": model_id}

    if session_id:
        payload["session"] = (
            session_id
            if "/" in session_id
            else f"projects/{project_id}/locations/{location}/collections/{collection_id}/engines/{engine_id}/sessions/{session_id}"
        )

    start_time = time.perf_counter()
    response = requests.post(url, headers=headers, json=payload, stream=True, timeout=120)
    if response.status_code != 200:
        raise RuntimeError(f"Gemini Enterprise API Error [{response.status_code}]: {response.text}")

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


def retrieve_data(query: str, **kwargs) -> dict:
    """Retrieve full answer text and grounded enterprise documents with latency metrics."""
    start_time = time.perf_counter()
    first_token_time = None
    text_parts = []
    documents = []
    session_id = None

    for chunk in stream_assist(query, **kwargs):
        # Extract session ID
        if "sessionInfo" in chunk and "session" in chunk["sessionInfo"]:
            session_id = chunk["sessionInfo"]["session"].split("/")[-1]

        # Extract answer and references
        answer = chunk.get("answer", {})
        for reply in answer.get("replies", []):
            grounded = reply.get("groundedContent", {})
            content = grounded.get("content", {})
            if "text" in content and not content.get("thought", False):
                if first_token_time is None:
                    first_token_time = time.perf_counter() - start_time
                text_parts.append(content["text"])

            # Extract grounded documents/references
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
        "documents": documents,
        "session_id": session_id,
        "latency": {
            "time_to_first_token_seconds": round(first_token_time, 3) if first_token_time else round(total_time, 3),
            "total_latency_seconds": round(total_time, 3),
        },
    }


if __name__ == "__main__":
    import sys

    user_query = sys.argv[1] if len(sys.argv) > 1 else "Summarize latest enterprise AI trends"
    print(f"Querying Gemini Enterprise (Model: {DEFAULT_MODEL_ID}): {user_query}\n")

    start_time = time.perf_counter()
    first_token_time = None

    # Stream real-time text output
    print("Response: ", end="", flush=True)
    for chunk in stream_assist(user_query):
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

