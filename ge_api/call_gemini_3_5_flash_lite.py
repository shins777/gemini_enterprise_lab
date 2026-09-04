#!/usr/bin/env python3
"""Direct Vertex AI Gemini 3.5 Flash Lite Caller.

Calls the `gemini-3.5-flash-lite` foundation model directly on Google Cloud Vertex AI
using the official `google-genai` SDK with streaming, latency benchmarking, and auto-authentication.
"""

import os
import subprocess
import sys
import time
from typing import Generator, Optional
from google import genai
from google.genai import types
from google.oauth2.credentials import Credentials

# Configuration defaults
DEFAULT_PROJECT = os.getenv("GCP_PROJECT", "ai-hangsik")
DEFAULT_LOCATION = os.getenv("GEMINI_LOCATION", "global")  # gemini-3.5-flash-lite is hosted in 'global'
DEFAULT_MODEL = "gemini-3.5-flash-lite"


def get_credentials() -> Optional[Credentials]:
    """Resolve valid Google Cloud OAuth2 credentials."""
    token = os.getenv("CLOUDSDK_AUTH_ACCESS_TOKEN") or os.getenv("GOOGLE_ACCESS_TOKEN")
    if token:
        return Credentials(token=token.strip())
    try:
        token = subprocess.check_output(["gcloud", "auth", "print-access-token"], text=True).strip()
        if token:
            return Credentials(token=token)
    except Exception:
        pass
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
    # Fall back to default ADC if no token was resolved
    return genai.Client(
        vertexai=True,
        project=project_id,
        location=location,
    )


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
    """Stream Gemini 3.5 Flash Lite responses chunk-by-chunk in real-time."""
    client = get_genai_client(project_id=project_id, location=location)

    config = types.GenerateContentConfig(
        temperature=temperature,
    )

    response_stream = client.models.generate_content_stream(
        model=model,
        contents=prompt,
        config=config,
    )

    for chunk in response_stream:
        if chunk.text:
            yield chunk.text


if __name__ == "__main__":
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Introduce yourself and describe your key strengths."

    print("=" * 65)
    print(f"🚀 Calling {DEFAULT_MODEL} Directly (Location: {DEFAULT_LOCATION})")
    print(f"Prompt: {prompt}")
    print("=" * 65 + "\n")

    start_time = time.perf_counter()
    first_token_time = None

    print("Response: ", end="", flush=True)
    try:
        for text_chunk in stream_content(prompt):
            if first_token_time is None:
                first_token_time = time.perf_counter() - start_time
            print(text_chunk, end="", flush=True)

        total_time = time.perf_counter() - start_time
        ttft = first_token_time if first_token_time is not None else total_time

        print("\n\n" + "-" * 45)
        print("⏱️  Latency Metrics:")
        print(f"  • Time to First Token (TTFT): {ttft:.3f}s")
        print(f"  • Total Stream Latency:      {total_time:.3f}s")
        print("-" * 45 + "\n")

    except Exception as e:
        print(f"\n\n❌ Error calling {DEFAULT_MODEL}: {e}", file=sys.stderr)
        sys.exit(1)
