#!/usr/bin/env python3
import os
import uvicorn
from agent import root_agent
from google.adk.a2a.utils.agent_to_a2a import to_a2a

def main():
    host = os.getenv("A2A_HOST", "0.0.0.0")
    port = int(os.getenv("A2A_PORT", "8000"))

    print(f"Starting A2A Server for '{root_agent.name}' on http://{host}:{port}...")
    print(f"Agent Card URL: http://localhost:{port}/.well-known/agent-card.json")

    app = to_a2a(root_agent, host=host, port=port)
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    main()
