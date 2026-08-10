#!/usr/bin/env python3
import os
import vertexai
from vertexai.agent_engines import AdkApp
from vertexai.preview import reasoning_engines
from agent import root_agent

def main():
    PROJECT_ID = os.getenv("GCP_PROJECT", "explore-ai-47e29c5f")
    LOCATION = os.getenv("GCP_LOCATION", "us-central1")
    STAGING_BUCKET = os.getenv("GCS_STAGING_BUCKET", "gs://run-sources-explore-ai-47e29c5f-us-central1")

    print(f"Initializing Vertex AI with project='{PROJECT_ID}', location='{LOCATION}', staging_bucket='{STAGING_BUCKET}'...")
    vertexai.init(
        project=PROJECT_ID,
        location=LOCATION,
        staging_bucket=STAGING_BUCKET
    )

    print("Creating AdkApp instance for root_agent...")
    app = AdkApp(agent=root_agent)

    print("Deploying A2A-compatible agent.py to Agent Engine (Reasoning Engine)...")
    remote_engine = reasoning_engines.ReasoningEngine.create(
        app,
        requirements=[
            "google-adk[a2a]",
            "a2a-sdk",
            "sse-starlette",
            "google-cloud-aiplatform[adk,agent_engines]",
        ],
        display_name="Search Agent Engine (A2A)",
        description="A2A-compatible Search Assistant Agent powered by Google ADK and Gemini with Google Search tool."
    )

    print("\n==========================================")
    print("Agent Engine Deployment Successful!")
    print(f"Project ID: {PROJECT_ID}")
    print(f"Resource Name: {remote_engine.resource_name}")
    print("==========================================")

    return remote_engine

if __name__ == "__main__":
    main()
