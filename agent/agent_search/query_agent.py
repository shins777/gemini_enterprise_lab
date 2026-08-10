#!/usr/bin/env python3
import os
import json
import vertexai
from vertexai.preview import reasoning_engines

DEFAULT_RESOURCE_NAME = "projects/729463364663/locations/us-central1/reasoningEngines/4569827061002141696"

def query_agent(message: str, user_id: str = "user_1"):
    resource_name = os.getenv("REASONING_ENGINE_RESOURCE_NAME", DEFAULT_RESOURCE_NAME)
    project_id = os.getenv("GCP_PROJECT", "explore-ai-47e29c5f")
    location = os.getenv("GCP_LOCATION", "us-central1")

    vertexai.init(project=project_id, location=location)
    engine = reasoning_engines.ReasoningEngine(resource_name)

    session = engine.create_session(user_id=user_id)
    session_id = session["id"]

    print(f"Session Created (ID: {session_id})")
    print(f"User Query: {message}\n")

    response_chunks = engine.execution_api_client.stream_query_reasoning_engine(
        request={
            "name": engine.resource_name,
            "class_method": "stream_query",
            "input": {
                "user_id": user_id,
                "session_id": session_id,
                "message": message
            }
        }
    )

    for chunk in response_chunks:
        data = json.loads(chunk.data.decode("utf-8"))
        if "content" in data and "parts" in data["content"]:
            for part in data["content"]["parts"]:
                if "text" in part:
                    print(part["text"])

if __name__ == "__main__":
    query_agent("Summarize the latest developments in AI agents.")
