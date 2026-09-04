# Gemini Enterprise Stream Assist (`stream_assist.py`)

A lightweight, standalone Python script to retrieve data and stream responses from **Google Cloud Gemini Enterprise** (`AssistantService.StreamAssist`).

---

## 🚀 Quick Start

### 1. Run via Terminal
```bash
export GCP_PROJECT="explore-ai-aa934711"
python3 ge_api/stream_assist/stream_assist.py "Summarize our latest enterprise AI strategy"
```

### 2. Python Code Usage

```python
from ge_api.stream_assist import stream_assist, retrieve_data

# Option A: Real-time streaming
for chunk in stream_assist("What is Agentic AI?"):
    for reply in chunk.get("answer", {}).get("replies", []):
        text = reply.get("groundedContent", {}).get("content", {}).get("text", "")
        if text:
            print(text, end="", flush=True)

# Option B: Complete data & grounded documents retrieval with latency
data = retrieve_data("What are the company's Q3 goals?")
print("Answer:", data["text"])
print("Retrieved Documents:", data["documents"])
print("Latency:", data["latency"])
# Output: {'time_to_first_token_seconds': 1.12, 'total_latency_seconds': 3.45}
```

---

## ⚙️ Environment Variables

| Variable | Description | Default |
| :--- | :--- | :--- |
| `GCP_PROJECT` | Target GCP Project ID | `explore-ai-aa934711` |
| `GCP_LOCATION` | Region / Location | `global` |
| `GE_ENGINE_ID` | Discovery Engine ID | `default_engine` |
| `GE_ASSISTANT_ID` | Assistant ID | `default_assistant` |
| `GE_MODEL_ID` | Generative Foundation Model in `generationSpec` | `gemini-2.5-flash` |
| `CLOUDSDK_AUTH_ACCESS_TOKEN` | (Optional) Access token override | Resolved via ADC / `gcloud` |
