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
* **[`ebnf`](ebnf/)**: EBNF Search Filter Parsing Engine for Discovery Engine & AIP-160 (Detailed documentation: [README.md](ebnf/README.md)).
  * **[`EBNF.py`](ebnf/EBNF.py)**: Standalone, zero-LLM search filter condition extractor and EBNF synthesizer (< 5ms latency, $0 cost). Handles complex multi-sentence queries and diverse conditions (year, category, author, department, status, file_type).
  * **[`EBNF_LLM.py`](ebnf/EBNF_LLM.py)**: Ultra-fast Gemini 3.5 Flash Lite extractor optimized for sub-second (< 1.0s) response times via client singleton, compact prompting, zero-token local post-processing, and connection warm-up.

---

## 🚀 Quick Usage

### 1. Standalone Zero-LLM EBNF Filter Extraction (`ebnf/EBNF.py`)
```bash
# Pure local rule-based extraction (Zero Gemini calls, < 5ms latency, $0 cost)
python3 ge_api/ebnf/EBNF.py "세계 증시 보고서를 신항식이 작성했어 2025년도에 그 문서를 찾아줘. 아마도 AI 팀이야."
```

### 2. Direct Vertex AI Call with AI EBNF Filter Synthesis (`ebnf/EBNF_LLM.py`)
```bash
# Sub-second Gemini 3.5 Flash Lite extraction (< 1.0s SLA)
python3 ge_api/ebnf/EBNF_LLM.py "2024년 이후에 작성된 재무 보고서 PDF 파일을 찾아줘"
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

