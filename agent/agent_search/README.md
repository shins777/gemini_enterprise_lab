# A2A-Compatible Search Agent (Agent Engine)

A premium, Agent-to-Agent (A2A) compatible Search Assistant Agent powered by the **Google ADK (Agent Development Kit)** and the stable, high-performance **Gemini 2.5 Flash** model. This agent is equipped with Google Search capabilities to dynamically find, synthesize, and report on the latest web-based developments for any user query.

---

## 📂 Project Structure

The project has been organized with a minimalist, clean, and production-ready structure:

```tree
agent_search/
├── .env                  # Configuration variables for GCP project & location
├── agent.py              # Main Agent definition (Google ADK & A2A wrapper)
├── deploy.py             # Script to package and deploy agent to Vertex AI Agent Engine
├── query_agent.py        # Streamlined testing client to query the deployed engine
├── a2a_server.py         # Local server utility for hosting the A2A API endpoint
├── requirements.txt      # Python dependencies
└── README.md             # This comprehensive guide
```

---

## ⚙️ Configuration Setup

Verify that the `.env` file matches your target GCP environment specifications:

```ini
GOOGLE_GENAI_USE_VERTEXAI=1
GOOGLE_CLOUD_PROJECT=explore-ai-47e29c5f
GOOGLE_CLOUD_LOCATION=us-central1
```

### Install Dependencies
To install the required SDK packages locally:
```bash
pip install -r requirements.txt
```

---

## 🚀 Deployed Resource Info

The active production deployment on **Vertex AI Agent Engine (Reasoning Engine)** is:
- **Project ID**: `explore-ai-47e29c5f`
- **Location**: `us-central1`
- **Reasoning Engine Resource Name**: 
  `projects/729463364663/locations/us-central1/reasoningEngines/4569827061002141696`

---

## 🛠️ Usage Guide

### 1. Run the Query Client
To run a streaming session against the active Reasoning Engine deployment:
```bash
python3 query_agent.py
```

### 2. Deploy/Redeploy the Agent
To package, upload, and provision a new instance of your A2A-compatible Agent Engine:
```bash
python3 deploy.py
```

### 3. Run the Local A2A Server
To spin up a local FastAPI/Uvicorn server hosting the agent for local orchestration:
```bash
python3 a2a_server.py
```
- Local URL: `http://localhost:8000`
- Well-known Agent Card URL: `http://localhost:8000/.well-known/agent-card.json`
