import os
import re
import uuid
from typing import List, Dict, Tuple
import pandas as pd

def ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)

def safe_filename(filename: str) -> str:
    filename = re.sub(r"[^\w\-. ]", "_", filename)
    return filename.strip().replace(" ", "_")

def save_uploaded_file(uploaded_file, target_dir: str) -> str:
    ensure_dir(target_dir)
    unique_name = f"{uuid.uuid4().hex}_{safe_filename(uploaded_file.name)}"
    file_path = os.path.join(target_dir, unique_name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    return file_path

def docs_to_dataframe(docs: List) -> pd.DataFrame:
    rows = []
    for i, doc in enumerate(docs, start=1):
        rows.append({
            "chunk_id": i,
            "content": doc.page_content,
            "source": doc.metadata.get("source", "unknown"),
            "document_name": doc.metadata.get("document_name", "unknown"),
            "page": doc.metadata.get("page", "NA"),
            "chunk_index": doc.metadata.get("chunk_index", "NA"),
        })
    return pd.DataFrame(rows)

def build_download_text(
    summary: str,
    insights: str,
    risks: str,
    clauses: str,
    doc_type: str,
    keywords: List[Tuple[str, int]]
) -> str:
    keywords_str = "\n".join([f"- {word}: {count}" for word, count in keywords]) if keywords else "Not generated."

    return f"""
ENTERPRISE AI DOCUMENT INTELLIGENCE REPORT
==========================================

DOCUMENT TYPE
-------------
{doc_type}

EXECUTIVE SUMMARY
-----------------
{summary or "Not generated."}

KEY INSIGHTS
------------
{insights or "Not generated."}

RISK ANALYSIS
-------------
{risks or "Not generated."}

CLAUSE EXTRACTION
-----------------
{clauses or "Not generated."}

TOP KEYWORDS
------------
{keywords_str}
""".strip()

def normalize_similarity_score(raw_score: float, vector_db_type: str) -> float:
    if raw_score is None:
        return 0.0

    if vector_db_type.lower() == "faiss":
        # FAISS often returns L2 distance. Lower is better.
        normalized = 1 / (1 + float(raw_score))
        return round(normalized, 4)

    if vector_db_type.lower() == "chroma":
        # Chroma often returns distance too.
        normalized = 1 / (1 + float(raw_score))
        return round(normalized, 4)

    return 0.0

def confidence_label_from_score(avg_score: float) -> str:
    if avg_score >= 0.80:
        return "High"
    if avg_score >= 0.60:
        return "Medium"
    return "Low"

def average_score(scores: List[float]) -> float:
    if not scores:
        return 0.0
    return round(sum(scores) / len(scores), 4)

def highlight_keywords_html(text: str, keywords: List[str]) -> str:
    highlighted = text
    unique_keywords = sorted(set([k for k in keywords if k]), key=len, reverse=True)

    for keyword in unique_keywords:
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        highlighted = pattern.sub(
            lambda m: f"<mark>{m.group(0)}</mark>",
            highlighted
        )

    return highlighted

def pretty_score(score: float) -> str:
    return f"{score:.2f}"

def keyword_search_dataframe(df: pd.DataFrame, keyword: str) -> pd.DataFrame:
    result = df[df["content"].str.contains(keyword, case=False, na=False)].copy()
    if result.empty:
        return result

    result["match_count"] = result["content"].str.lower().str.count(keyword.lower())
    result = result.sort_values("match_count", ascending=False)
    return result