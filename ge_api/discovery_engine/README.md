# Discovery Engine API - Gemini 3.5 Flash Lite Caller

This module demonstrates calling the **Google Cloud Discovery Engine API** with `generationSpec.modelId` configured to `gemini-3.5-flash-lite`.

---

## 🚀 Quick Start

### 1. Terminal Execution

```bash
# Execute with default model (gemini-3.5-flash-lite)
python3 ge_api/discovery_engine/call_gemini_3_5_flash_lite.py "Introduce yourself."

# Or override model on CLI (e.g. gemini-3.5-flash)
python3 ge_api/discovery_engine/call_gemini_3_5_flash_lite.py "Introduce yourself." gemini-3.5-flash
```

### 2. Python Code Usage

```python
from ge_api.discovery_engine import call_discovery_engine, call_discovery_engine_stream

# Option A: Real-time streaming
for chunk in call_discovery_engine_stream("What are our Q3 business goals?"):
    for reply in chunk.get("answer", {}).get("replies", []):
        text = reply.get("groundedContent", {}).get("content", {}).get("text", "")
        if text:
            print(text, end="", flush=True)

# Option B: Complete aggregated response with latency metrics
result = call_discovery_engine("Summarize our cloud architecture.")
print("Response:\n", result["text"])
print("Latency:", result["latency"])
print("Retrieved Documents:", len(result["documents"]))
```

---

## ⚙️ Configuration & Model Status

| Parameter | Description | Default |
| :--- | :--- | :--- |
| `GCP_PROJECT` | Google Cloud Project ID | `ai-hangsik` |
| `GCP_LOCATION` | Location / Region | `global` |
| `GE_ENGINE_ID` | Discovery Engine ID | `gemini-enterprise-july-202_1782612363846` |
| `GE_MODEL_ID` | Foundation model in `generationSpec` | `gemini-3.5-flash-lite` |

> [!NOTE]
> In Discovery Engine's Assistant API, `gemini-3.5-flash-lite` may return an `INVALID_ARGUMENT` if your organization/backend policy has not yet mapped the lite model to the Assistant gateway. If that occurs:
> * You can use **`gemini-3.5-flash`** (active and supported in Discovery Engine).
> * Or call **`gemini-3.5-flash-lite` directly on Vertex AI** using [`ge_api/call_gemini_3_5_flash_lite.py`](../call_gemini_3_5_flash_lite.py).
