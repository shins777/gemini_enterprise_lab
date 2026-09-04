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
* **[`EBNF.py`](EBNF.py)**: Standalone, zero-LLM search filter condition extractor and EBNF synthesizer.
  * Completely removes Gemini/LLM dependencies (runs purely in local Python, < 1ms latency, $0 cost).
  * Automatically extracts:
    - **Year / Date (년도)**: `2024년 이후` -> `year >= 2024`
    - **Document Type (문서 타입)**: `PDF 파일` -> `file_type = "pdf"`
    - **Document Topic (문서 주제)**: `재무 보고서` -> `category = "재무 보고서"`
    - **Author (작성자)**: `홍길동이 작성한` -> `author = "홍길동"`
  * Returns synthesized EBNF filter string conforming to Google Cloud Discovery Engine & AIP-160 specifications.
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
from ge_api import compose_ebnf_filter, compose_ebnf_filter_local, EBNFFilterBuilder

# 1. Pure Local Rule-Based Extraction (No Gemini/API call, < 1ms latency, $0 cost)
local_res = compose_ebnf_filter_local("2024년 이후에 작성된 재무 보고서 PDF 파일을 찾아줘")
print("Local Clean Query:", local_res.clean_query)  # "재무 보고서"
print("Local EBNF Filter:", local_res.ebnf_filter)  # "file_type = \"pdf\" AND year >= 2024"
print("Local Latency:", local_res.latency_seconds)  # ~0.001s

# 2. AI-Powered Extraction via Gemini 3.5 Flash Lite (Deep semantic parsing)
ai_res = compose_ebnf_filter("Find all security audit reports in HR or Legal from 2023 onwards by author John Doe")
print("AI EBNF Filter:", ai_res.ebnf_filter)
# "(department = \"HR\" OR department = \"Legal\") AND year >= 2023 AND author = \"John Doe\""

# 3. Fluent Programmatic Builder (from UI form controls, date pickers, dropdowns)
filter_str = (
    EBNFFilterBuilder()
    .equals("file_type", "pdf")
    .greater_or_equal("year", 2024)
    .text_match("department", "Finance")
    .any_of("tag", ["audit", "compliance"])
    .build()
)
print("Built EBNF Filter:", filter_str)
```

### 3. Gemini Enterprise Grounded Stream Assist
```bash
python3 ge_api/stream_assist/stream_assist.py "Summarize the latest quarterly reports"
```

### 4. Discovery Engine API with Custom Model Specification
```bash
python3 ge_api/discovery_engine/call_gemini_3_5_flash_lite.py "Introduce yourself in one sentence." gemini-3.5-flash
```

