#!/usr/bin/env python3
"""EBNF Search Filter Extractor (Standalone / Zero-LLM).

This module extracts search condition filters (Year, Document Topic, File Type, Author, etc.)
from natural language queries and synthesizes an Extended Backus-Naur Form (EBNF) filter
conforming to Google Cloud Discovery Engine & AIP-160 filter specifications without calling Gemini.
"""

import re
import sys
import time
from typing import Any, Dict


def extract_ebnf_filter(query: str) -> Dict[str, Any]:
    """Extract search filter conditions and synthesize an EBNF filter string locally.

    Supports:
    - Year (년도): '2024년 이후', '2024년 부터', '2022~2024년', 'since 2024', 'year:>=2024'
    - Document Topic (문서 주제): '재무 보고서', '보안 감사 보고서', '마케팅 기획서', '계약서', etc.
    - File Type (문서 타입): 'PDF', '워드(docx)', '엑셀(xlsx)', '파워포인트(pptx)', 'filetype:pdf'
    - Author (작성자): '작성자: 홍길동', '홍길동이 작성한', 'by John Doe', 'author:"Jane"'
    - Department (부서): 'HR or Legal', '인사 또는 법무', 'dept:Finance'

    Args:
        query: User input query string.

    Returns:
        Dictionary containing:
        - raw_query: Original user input query
        - clean_query: Semantic search query stripped of filter keywords
        - ebnf_filter: Synthesized EBNF filter string (Discovery Engine syntax)
        - attributes: Extracted filter conditions by category
        - latency_ms: Execution time in milliseconds
    """
    start = time.perf_counter()
    text = query.strip()
    clauses = []
    attributes = {}

    # 1. Search Operator Syntax (e.g. filetype:pdf, author:"John Doe", year:>=2024)
    op_pattern = re.compile(r'(?:(\b\w+):("([^"]+)"|(\S+)))')
    for m in list(op_pattern.finditer(text)):
        k, _, q_val, u_val = m.group(1).lower(), m.group(2), m.group(3), m.group(4)
        val = q_val if q_val is not None else u_val
        if k in ("filetype", "type", "ext"):
            clauses.append(f'file_type = "{val.lower()}"')
            attributes["file_type"] = val.lower()
            text = text.replace(m.group(0), " ")
        elif k in ("author", "owner"):
            clauses.append(f'author = "{val}"')
            attributes["author"] = val
            text = text.replace(m.group(0), " ")
        elif k in ("year", "date"):
            op = val[:2] if val.startswith((">=", "<=", "!=")) else (val[:1] if val.startswith(("<", ">")) else "=")
            num = val[len(op):].strip() if op != "=" else val.strip()
            clauses.append(f"year {op} {num}")
            attributes["year"] = f"{op} {num}"
            text = text.replace(m.group(0), " ")

    # 2. Author extraction (작성자)
    author_m = re.search(
        r"(?:작성자\s*[:=]?\s*([가-힣a-zA-Z]+)|([가-힣a-zA-Z]+?)(?:이|가)\s*작성한|(?:by|authored by)\s+([A-Za-z\s]+))",
        text,
    )
    if author_m and "author" not in attributes:
        author = (author_m.group(1) or author_m.group(2) or author_m.group(3) or "").strip()
        if author and author.lower() not in ("pdf", "word", "excel"):
            clauses.append(f'author = "{author}"')
            attributes["author"] = author
            text = text.replace(author_m.group(0), " ")

    # 3. Year / Date extraction (년도 / 기간)
    year_range = re.search(
        r"(\d{4})\s*년?\s*(?:~|-|부터|에서)\s*(\d{4})\s*년?(?:\s*사이)?|\b(?:between)\s*(\d{4})\s*(?:and|-)\s*(\d{4})\b",
        text,
        re.I,
    )
    if year_range and "year" not in attributes:
        y1 = year_range.group(1) or year_range.group(3)
        y2 = year_range.group(2) or year_range.group(4)
        clauses.append(f"year >= {y1} AND year <= {y2}")
        attributes["year"] = f">= {y1} AND <= {y2}"
        text = text.replace(year_range.group(0), " ")
    elif "year" not in attributes:
        year_gte = re.search(r"(\d{4})\s*년?\s*(?:이후|부터|이상)(?:\s*에)?|\b(?:after|since|from)\s*(\d{4})\b", text, re.I)
        if year_gte:
            y = year_gte.group(1) or year_gte.group(2)
            clauses.append(f"year >= {y}")
            attributes["year"] = f">= {y}"
            text = text.replace(year_gte.group(0), " ")
        else:
            year_lte = re.search(r"(\d{4})\s*년?\s*(?:이전|까지|이하)(?:\s*에)?|\b(?:before|prior to)\s*(\d{4})\b", text, re.I)
            if year_lte:
                y = year_lte.group(1) or year_lte.group(2)
                clauses.append(f"year <= {y}")
                attributes["year"] = f"<= {y}"
                text = text.replace(year_lte.group(0), " ")
            else:
                exact_y = re.search(r"\b(\d{4})\s*년(?:\s*에)?\b", text)
                if exact_y:
                    y = exact_y.group(1)
                    clauses.append(f"year = {y}")
                    attributes["year"] = y
                    text = text.replace(exact_y.group(0), " ")

    # 4. File Type extraction (문서 타입)
    ft_m = re.search(r"(?i)\b(pdf|docx?|xlsx?|pptx?|csv|txt|json|html)\b|(워드|엑셀|파워포인트)", text)
    if ft_m and "file_type" not in attributes:
        val = ft_m.group(0).lower()
        mapping = {"워드": "docx", "엑셀": "xlsx", "파워포인트": "pptx"}
        ft = mapping.get(val, val)
        clauses.append(f'file_type = "{ft}"')
        attributes["file_type"] = ft
        text = re.sub(r"(?i)\b(pdf|docx?|xlsx?|pptx?|csv|txt|json|html)\s*(?:파일|문서)?|(워드|엑셀|파워포인트)\s*(?:파일|문서)?", " ", text)

    # 5. Remove conversational search / verb particles
    text = re.sub(r"\b(작성된|생성된|등록된|배포된|출판된|문서|파일)\b", " ", text)
    text = re.sub(r"\b(find|search for|show me|look for|get me)\b", " ", text, flags=re.I)

    # 6. Document Topic extraction (문서 주제)
    topic_m = re.search(
        r"([가-힣a-zA-Z0-9\s]+?(?:보고서|기획서|계약서|명세서|가이드|매뉴얼|규정|회의록|리포트|report))",
        text,
        re.I,
    )
    if topic_m and "category" not in attributes:
        topic = topic_m.group(1).strip()
        topic = re.sub(r"^[에|에서|의|로|으로]\s*", "", topic).strip()
        topic = re.sub(r"(을|를|의|에|에서|으로|로)$", "", topic).strip()
        if topic:
            clauses.append(f'category = "{topic}"')
            attributes["category"] = topic
            text = text.replace(topic_m.group(0), " ")

    # 7. Clean up remaining conversational postpositions
    clean = re.sub(r"\b(에|에서|으로|로|을|를|의|찾아줘|검색해줘|보여줘|알려줘)\b", " ", text)
    clean = re.sub(r"\s+", " ", clean).strip()
    final_clean = attributes.get("category", clean) or clean

    # 8. Synthesize final EBNF filter
    ebnf_filter = " AND ".join(clauses)
    elapsed_ms = (time.perf_counter() - start) * 1000

    return {
        "raw_query": query,
        "clean_query": final_clean,
        "ebnf_filter": ebnf_filter,
        "attributes": attributes,
        "latency_ms": round(elapsed_ms, 3),
    }


def format_filter_output(res: Dict[str, Any]) -> str:
    """Format the extracted filter result into a clear, visual summary."""
    lines = [
        "┌" + "─" * 68 + "┐",
        "│ 🧩 EBNF Filter Extraction Result (Zero-LLM / Local Execution)     │",
        "├" + "─" * 68 + "┤",
        f"│  • Input Query:    {res['raw_query']}",
        f"│  • Clean Query:    {res['clean_query']}",
        f"│  • EBNF Filter:    {res['ebnf_filter'] if res['ebnf_filter'] else '(None)'}",
        "├" + "─" * 68 + "┤",
        "│  • Extracted Filter Conditions (주어진 조건 필터):",
    ]
    labels = {
        "year": "년도 (Year)",
        "category": "문서주제 (Topic)",
        "file_type": "문서타입 (File Type)",
        "author": "작성자 (Author)",
        "department": "부서 (Department)",
    }
    for k, v in res["attributes"].items():
        label = labels.get(k, k)
        lines.append(f"│     - {label:18}: {v}")
    lines.extend([
        "├" + "─" * 68 + "┤",
        f"│  • Execution Time: {res['latency_ms']:.3f} ms (Pure local, 0 API calls)    │",
        "└" + "─" * 68 + "┘",
    ])
    return "\n".join(lines)


if __name__ == "__main__":
    # Target test query specified by user
    target_query = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "2024년 이후에 작성된 재무 보고서 PDF 파일을 찾아줘"
    )

    result = extract_ebnf_filter(target_query)
    print("\n" + format_filter_output(result) + "\n")
    print(f"👉 Return EBNF Filter String:\n{result['ebnf_filter']}\n")
