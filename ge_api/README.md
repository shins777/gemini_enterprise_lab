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
* **[`call_gemini_3_5_flash_lite.py`](call_gemini_3_5_flash_lite.py)**: Direct caller for the `gemini-3.5-flash-lite` foundation model on Vertex AI using the official `google-genai` SDK with **Extended Backus-Naur Form (EBNF) Filter Synthesis**.
  * **Automated EBNF Filter Composition**: Analyzes natural language queries and synthesizes valid Discovery Engine / AIP-160 EBNF filter strings (e.g. `year >= 2024 AND file_type = "pdf"`).
  * **Programmatic Filter Builder (`EBNFFilterBuilder`)**: Fluent interface for constructing EBNF filter syntax programmatically.
  * **Low Latency (<2s)**: Ultra-fast query analysis and streaming responses.
  * **Real-time streaming output (`stream_content()`)** and non-streaming execution (`generate_content()`).

---

## 🚀 Quick Usage

### 1. Direct Vertex AI Call with Automatic EBNF Filter Synthesis
```bash
# Analyze query and auto-synthesize EBNF filter (Korean)
python3 ge_api/call_gemini_3_5_flash_lite.py "2024년 이후에 작성된 재무 보고서 PDF 파일을 찾아줘"

# Complex search with multiple metadata filters (English)
python3 ge_api/call_gemini_3_5_flash_lite.py "Find all security audit reports in HR or Legal from 2023 onwards by author John Doe"
```

### 2. Programmatic EBNF Filter Composition in Python
```python
from ge_api import compose_ebnf_filter, EBNFFilterBuilder

# 1. Automatic synthesis via Gemini 3.5 Flash Lite
result = compose_ebnf_filter("2024년 이후에 작성된 재무 보고서 PDF 파일을 찾아줘")
print("Clean Query:", result.clean_query)  # "재무 보고서"
print("EBNF Filter:", result.ebnf_filter)  # "year >= 2024 AND file_type = \"pdf\""

# 2. Fluent programmatic builder
filter_str = (
    EBNFFilterBuilder()
    .equals("file_type", "pdf")
    .greater_or_equal("year", 2024)
    .text_match("department", "Finance")
    .any_of("tag", ["audit", "compliance"])
    .build()
)
print("EBNF Filter:", filter_str)
```

### 3. Gemini Enterprise Grounded Stream Assist
```bash
python3 ge_api/stream_assist/stream_assist.py "Summarize the latest quarterly reports"
```

### 4. Discovery Engine API with Custom Model Specification
```bash
python3 ge_api/discovery_engine/call_gemini_3_5_flash_lite.py "Introduce yourself in one sentence." gemini-3.5-flash
```

