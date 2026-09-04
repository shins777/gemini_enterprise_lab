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
* **[`EBNF_LLM.py`](EBNF_LLM.py)** (formerly `call_gemini_3_5_flash_lite.py`): Direct caller for the `gemini-3.5-flash-lite` foundation model on Vertex AI using the official `google-genai` SDK with **AI-Powered Extended Backus-Naur Form (EBNF) Filter Synthesis**.
  * **Automated EBNF Filter Composition**: Analyzes natural language queries and synthesizes valid Discovery Engine / AIP-160 EBNF filter strings (e.g. `year >= 2024 AND file_type = "pdf"`).
  * **Programmatic Filter Builder (`EBNFFilterBuilder`)**: Fluent interface for constructing EBNF filter syntax programmatically.
  * **Low Latency (<2s)**: Ultra-fast query analysis and streaming responses.
  * **Real-time streaming output (`stream_content()`)** and non-streaming execution (`generate_content()`).

---

## 🚀 Quick Usage

### 1. Standalone Zero-LLM EBNF Filter Extraction (`EBNF.py`)
```bash
# Pure local rule-based extraction (Zero Gemini calls, < 1ms latency, $0 cost)
python3 ge_api/EBNF.py "2024년 이후에 작성된 재무 보고서 PDF 파일을 찾아줘"

# With author and different doc types
python3 ge_api/EBNF.py "홍길동이 작성한 2023년 보안 감사 보고서 워드 문서를 찾아줘"
```

### 2. Direct Vertex AI Call with AI EBNF Filter Synthesis (`EBNF_LLM.py`)
```bash
python3 ge_api/EBNF_LLM.py "2024년 이후에 작성된 재무 보고서 PDF 파일을 찾아줘"
```

### 3. Programmatic EBNF Filter Composition in Python
```python
from ge_api import extract_ebnf_filter, extract_ebnf_with_llm

query = "2024년 이후에 작성된 재무 보고서 PDF 파일을 찾아줘"

# 1. Standalone Zero-LLM Extraction (Local Python, < 1ms, $0 cost)
local_res = extract_ebnf_filter(query)
print("Local Filter:", local_res["ebnf_filter"])
# 'year >= 2024 AND file_type = "pdf" AND category = "재무 보고서"'
print("Local Attributes:", local_res["attributes"])
# {'year': '>= 2024', 'file_type': 'pdf', 'category': '재무 보고서'}

# 2. AI-Powered Extraction via Gemini 3.5 Flash Lite
llm_res = extract_ebnf_with_llm(query)
print("LLM Filter:", llm_res["ebnf_filter"])
# 'category = "재무 보고서" AND file_type = "pdf" AND year >= 2024'
print("Extracted Info:", llm_res["extracted_info"])
# {'문서종류': '재무 보고서', '문서 타입': 'pdf', '작성자': None, '작성 일자': '2024년 이후'}
```

### 3. Gemini Enterprise Grounded Stream Assist
```bash
python3 ge_api/stream_assist/stream_assist.py "Summarize the latest quarterly reports"
```

### 4. Discovery Engine API with Custom Model Specification
```bash
python3 ge_api/discovery_engine/call_gemini_3_5_flash_lite.py "Introduce yourself in one sentence." gemini-3.5-flash
```

