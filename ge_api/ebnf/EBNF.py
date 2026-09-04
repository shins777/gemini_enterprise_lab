#!/usr/bin/env python3
"""EBNF Search Filter Extractor (Standalone / Zero-LLM).

Advanced rule-based and pattern extraction engine capable of handling diverse conversational,
multi-sentence, and colloquial queries (e.g. "세계 증시 보고서를 홍길동이 작성했어 2025년도에 그 문서를 찾아줘. 아마도 AI 팀이야.").
Synthesizes Extended Backus-Naur Form (EBNF) filters conforming to Google Cloud Discovery Engine & AIP-160.
"""

import re
import sys
import time
from typing import Any, Dict


def extract_ebnf_filter(query: str) -> Dict[str, Any]:
    """Extract search filter conditions and synthesize an EBNF filter string locally.

    Handles diverse query patterns:
    - Author (작성자): '홍길동이 작성했어', '홍길동이 썼어', '홍길동 작성', '작성자: 홍길동', 'by John Doe'
    - Department (부서/팀): '아마도 AI 팀이야', '소속은 AI팀', '인사팀에서', '개발본부', 'dept:Finance'
    - Year/Date (년도/일자): '2025년도에', '2024년 이후에', '2023년 이전에', '2022~2024년 사이', 'after 2024'
    - Document Topic (문서 주제/종류): '세계 증시 보고서', '재무 보고서', '보안 감사 보고서', '마케팅 기획서'
    - File Type (문서 타입): 'PDF 파일', '워드 문서(docx)', '엑셀(xlsx)', '파워포인트(pptx)', 'hwp'
    - Status & Negation (상태/제외): '초안 제외', 'not draft' -> NOT status = "draft"

    Args:
        query: Natural language query string (can be multi-sentence or conversational).

    Returns:
        Dictionary containing raw_query, clean_query, ebnf_filter, attributes, and latency_ms.
    """
    start = time.perf_counter()

    # Normalize whitespace, line breaks, and trailing spaces
    normalized = " ".join(query.split())
    working = normalized
    clause_dict = {}
    attributes = {}

    # 1. Search Operator Syntax (e.g. filetype:pdf, author:"홍길동", year:>=2025, dept:AI)
    op_pattern = re.compile(r'(?:(\b\w+):("([^"]+)"|(\S+)))')
    for m in list(op_pattern.finditer(working)):
        k, _, q_val, u_val = m.group(1).lower(), m.group(2), m.group(3), m.group(4)
        val = q_val if q_val is not None else u_val
        if k in ("filetype", "type", "ext", "format"):
            clause_dict["file_type"] = f'file_type = "{val.lower()}"'
            attributes["file_type"] = val.lower()
            working = working.replace(m.group(0), " ")
        elif k in ("author", "owner", "creator"):
            clause_dict["author"] = f'author = "{val}"'
            attributes["author"] = val
            working = working.replace(m.group(0), " ")
        elif k in ("dept", "department", "team"):
            clause_dict["department"] = f'department = "{val}"'
            attributes["department"] = val
            working = working.replace(m.group(0), " ")
        elif k in ("year", "date"):
            op = val[:2] if val.startswith((">=", "<=", "!=")) else (val[:1] if val.startswith(("<", ">")) else "=")
            num = val[len(op):].strip() if op != "=" else val.strip()
            clause_dict["year"] = f"year {op} {num}"
            attributes["year"] = f"{op} {num}"
            working = working.replace(m.group(0), " ")

    # 2. Year / Date Extraction (년도 / 기간)
    # Extracts year ranges, comparison operators, and exact years first to avoid collisions with other entities.
    year_range = re.search(
        r"(\d{4})\s*년도?\s*(?:~|-|부터|에서)\s*(\d{4})\s*년도?(?:\s*사이)?|\b(?:between)\s*(\d{4})\s*(?:and|-)\s*(\d{4})\b",
        working,
        re.I,
    )
    if year_range and "year" not in attributes:
        y1 = year_range.group(1) or year_range.group(3)
        y2 = year_range.group(2) or year_range.group(4)
        clause_dict["year"] = f"year >= {y1} AND year <= {y2}"
        attributes["year"] = f">= {y1} AND <= {y2}"
        working = working.replace(year_range.group(0), " ")
    elif "year" not in attributes:
        # 2b. Greater or equal: 2024년 이후, after 2024, since 2024
        year_gte = re.search(
            r"(\d{4})\s*년(?:도)?\s*(?:이후|부터|이상)(?:\s*에)?|\b(?:after|since|from)\s*(\d{4})\b",
            working,
            re.I,
        )
        if year_gte:
            y = year_gte.group(1) or year_gte.group(2)
            clause_dict["year"] = f"year >= {y}"
            attributes["year"] = f">= {y}"
            working = working.replace(year_gte.group(0), " ")
        else:
            # 2c. Less or equal: 2023년 이전, before 2023
            year_lte = re.search(
                r"(\d{4})\s*년(?:도)?\s*(?:이전|까지|이하)(?:\s*에)?|\b(?:before|prior to)\s*(\d{4})\b",
                working,
                re.I,
            )
            if year_lte:
                y = year_lte.group(1) or year_lte.group(2)
                clause_dict["year"] = f"year <= {y}"
                attributes["year"] = f"<= {y}"
                working = working.replace(year_lte.group(0), " ")
            else:
                # 2d. Exact year: 2025년도에, 2025년에, in 2025
                exact_y = re.search(r"\b(\d{4})\s*년(?:도)?(?:\s*에)?\b|\bin\s*(\d{4})\b", working, re.I)
                if exact_y:
                    y = exact_y.group(1) or exact_y.group(2)
                    clause_dict["year"] = f"year = {y}"
                    attributes["year"] = y
                    working = working.replace(exact_y.group(0), " ")

    # 3. Department / Team Extraction (부서 / 소속팀)
    # Handles: "아마도 AI 팀이야", "소속은 AI팀", "AI팀에서", "인사팀이고", "개발본부", "클라우드 사업부"
    dept_m = re.search(
        r"(?:아마도|아마|혹시)?\s*(?:소속은)?\s*([a-zA-Z0-9가-힣]+)\s*(팀|부서|본부|실|사업부|department|team)(?:이야|입니다|소속|인듯|같아|에서|의|이고|이며|은|는)?",
        working,
        re.I,
    )
    if dept_m and "department" not in attributes:
        d_name = dept_m.group(1).strip()
        d_suf = dept_m.group(2).strip()
        is_eng_abbr = d_name.isupper() or (len(d_name) <= 2 and d_name.isalpha() and ord(d_name[0]) < 128)
        full_dept = f"{d_name} {d_suf}" if is_eng_abbr else f"{d_name}{d_suf}"
        # Filter false positives
        if d_name not in ("이", "그", "저", "어느", "어떤", "해당", "관련"):
            clause_dict["department"] = f'department = "{full_dept}"'
            attributes["department"] = full_dept
            working = working.replace(dept_m.group(0), " ")

    # 4. Author Extraction (작성자)
    # Handles: "홍길동이 작성했어", "홍길동이 썼어", "홍길동이 등록했어", "작성자: 홍길동", "by John Doe"
    author_m = re.search(
        r"(?:(?:\s|^)([가-힣]{2,4}|[가-힣]\s+[가-힣]{1,3}|[A-Za-z\s]{2,15})(?:이|가|은|는)?\s*(작성했어|작성했음|작성함|작성한|만들었어|만듦|만든|썼어|쓴|등록했어|등록한|올렸어|올린|배포했어|배포한)|(?:작성자|글쓴이|작성인)\s*[:=은는이가]?\s*([가-힣a-zA-Z]+)|(?:by|authored by|written by)\s+([A-Za-z\s]+))",
        working,
    )
    if author_m and "author" not in attributes:
        raw_author = (author_m.group(1) or author_m.group(3) or author_m.group(4) or "").strip()
        author = "".join(raw_author.split()) if re.match(r"^[가-힣\s]+$", raw_author) else raw_author
        author = re.sub(r"(이|가|은|는|에|에서|의|로|으로)$", "", author).strip()
        stop_words = {
            "보고서", "문서", "파일", "pdf", "word", "excel", "ppt", "기획서",
            "계획서", "가이드", "매뉴얼", "규정", "자료", "리포트", "회의록", "명세서",
            "이후", "이전", "최근", "올해", "작년", "내년", "상반기", "하반기"
        }
        if author and author.lower() not in stop_words and not any(author.endswith(sw) for sw in stop_words):
            clause_dict["author"] = f'author = "{author}"'
            attributes["author"] = author
            working = working.replace(author_m.group(0), " ")

    # 5. File Type Extraction (문서 타입)
    ft_m = re.search(r"(?i)\b(pdf|docx?|xlsx?|pptx?|csv|txt|json|html|hwp)\b|(워드|엑셀|파워포인트|파포|한글)", working)
    if ft_m and "file_type" not in attributes:
        raw_ft = ft_m.group(0).lower()
        ft_map = {
            "워드": "docx",
            "word": "docx",
            "엑셀": "xlsx",
            "excel": "xlsx",
            "파워포인트": "pptx",
            "파포": "pptx",
            "ppt": "pptx",
            "한글": "hwp",
        }
        ft = ft_map.get(raw_ft, raw_ft)
        clause_dict["file_type"] = f'file_type = "{ft}"'
        attributes["file_type"] = ft
        working = re.sub(
            r"(?i)\b(pdf|docx?|xlsx?|pptx?|csv|txt|json|html|hwp)\s*(?:파일|문서)?|(워드|엑셀|파워포인트|파포|한글)\s*(?:파일|문서)?",
            " ",
            working,
        )

    # 6. Status & Negation (상태 및 제외)
    # Handles: "초안 제외", "초안 제외하고", "초안 빼고", "임시 문서 말고", "excluding draft"
    neg_m = re.search(
        r"(?:not|excluding|except)\s*(draft|archived|resolved)|\b(draft|초안|임시)\s*(?:제외(?:하고|한|하여)?|말고|아닌|빼고)?",
        working,
        re.I,
    )
    if neg_m and "status" not in attributes:
        s = neg_m.group(1) or neg_m.group(2)
        st = "draft" if s in ("초안", "임시", "draft") else s
        clause_dict["status"] = f'NOT status = "{st}"'
        attributes["status"] = f"NOT {st}"
        working = working.replace(neg_m.group(0), " ")

    # 7. Document Topic Extraction (문서 주제)
    # Matches document topics ending with 보고서, 기획서, 계획서, 계약서, 명세서, 가이드, 매뉴얼, etc.
    topic_m = re.search(
        r"([가-힣a-zA-Z0-9\s]{2,30}?(?:보고서|기획서|계획서|계약서|명세서|가이드|매뉴얼|규정|회의록|리포트|제안서|발표자료|설계서|검토서|문서|자료))",
        working,
        re.I,
    )
    if topic_m and "category" not in attributes:
        raw_topic = topic_m.group(1).strip()
        topic = " ".join(raw_topic.split())
        # Clean conversational verb prefixes, conjunctions, and postpositions
        topic = re.sub(r"^(작성된|생성된|등록된|배포된|출판된|그|해당|관련|이|저|하고|빼고|및|그리고|또한)\s*", "", topic).strip()
        topic = re.sub(r"^[에|에서|의|로|으로]\s*", "", topic).strip()
        topic = re.sub(r"(을|를|의|에|에서|으로|로|은|는)$", "", topic).strip()
        if topic and topic not in ("문서", "자료", "파일"):
            clause_dict["category"] = f'category = "{topic}"'
            attributes["category"] = topic
            working = working.replace(topic_m.group(0), " ")

    # 8. Clean query text
    clean = re.sub(r"\b(그|해당|관련|아마도|아마|혹시|좀)\b", " ", working)
    clean = re.sub(r"\b(찾아줘|검색해줘|보여줘|알려줘|작성된|생성된|등록된|배포된|문서|파일|find|show me|search for|look for)\b", " ", clean, flags=re.I)
    clean = re.sub(r"[에|에서|으로|로|을|를|의|은|는]\b", " ", clean)
    clean = re.sub(r"[\.?,!]", " ", clean)
    clean = re.sub(r"\s+", " ", clean).strip()

    final_clean = attributes.get("category", clean) or clean
    
    # Assemble EBNF filter clauses in canonical order
    canonical_order = ["department", "author", "year", "file_type", "status", "category"]
    clauses = [clause_dict[k] for k in canonical_order if k in clause_dict]
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
        f"│  • Input Query:    {res['raw_query'][:50]}",
        f"│  • Clean Query:    {res['clean_query'][:50]}",
        f"│  • EBNF Filter:    {res['ebnf_filter'] if res['ebnf_filter'] else '(None)'}",
        "├" + "─" * 68 + "┤",
        "│  • Extracted Filter Conditions (주어진 조건 필터):",
    ]
    labels = {
        "category": "문서주제 (Topic)",
        "author": "작성자 (Author)",
        "year": "년도 (Year)",
        "department": "부서 (Department)",
        "file_type": "문서타입 (File Type)",
        "status": "문서상태 (Status)",
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
    # Test query handling diverse conversational context
    target_query = (
        sys.argv[1]
        if len(sys.argv) > 1
        else "세계 증시 보고서를 홍길동이 작성했어 2025년도에 그 문서를 찾아줘. 아마도 AI 팀이야."
    )

    result = extract_ebnf_filter(target_query)
    print("\n" + format_filter_output(result) + "\n")
    print(f"👉 Return EBNF Filter String:\n{result['ebnf_filter']}\n")
