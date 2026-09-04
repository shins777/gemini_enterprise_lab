# 🌐 Gemini Enterprise API Suite (`ge_api`)

This directory contains production-grade client libraries, utilities, and CLI tools for programmatic integration with **Gemini Enterprise** and **Google Cloud Discovery Engine** services.

---

## 📦 Modules

* **[`stream_assist`](stream_assist/)**: Client library and CLI for the Gemini Enterprise `streamAssist` API (`AssistantService.StreamAssist`).
  * Real-time streaming answer generation
  * Enterprise data grounding and document retrieval (Google Drive, BigQuery, Jira, Confluence, DataStores)
  * Grounding references, URIs, and source citations extraction
  * Model reasoning / thoughts trace inspection
  * Multi-turn session management
* **[`discovery_engine`](discovery_engine/)**: Discovery Engine API caller targeting `AssistantService.StreamAssist` with customizable `generationSpec.modelId` (e.g. `gemini-3.5-flash-lite`, `gemini-3.5-flash`).
  * Explicit `generationSpec.modelId` configuration
  * Grounded retrieval and real-time streaming
* **[`call_gemini_3_5_flash_lite.py`](call_gemini_3_5_flash_lite.py)**: Direct caller for the `gemini-3.5-flash-lite` foundation model on Vertex AI using the official `google-genai` SDK.
  * Sub-2-second latency direct generation
  * Real-time streaming output (`stream_content()`)
  * Non-streaming execution with token usage telemetry (`generate_content()`)

---

## 🚀 Quick Usage

### 1. Direct Vertex AI Model Call (`gemini-3.5-flash-lite`)
```bash
python3 ge_api/call_gemini_3_5_flash_lite.py "Summarize the benefits of lightweight LLMs."
```

### 2. Gemini Enterprise Grounded Stream Assist
```bash
python3 ge_api/stream_assist/stream_assist.py "Summarize the latest quarterly reports"
```

### 3. Discovery Engine API with Custom Model Specification
```bash
python3 ge_api/discovery_engine/call_gemini_3_5_flash_lite.py "Introduce yourself in one sentence." gemini-3.5-flash
```

