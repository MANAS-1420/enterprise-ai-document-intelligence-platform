from typing import Dict, Any, List
from src.utils.helpers import normalize_similarity_score, average_score, confidence_label_from_score

def retrieve_with_scores(vectorstore, query: str, top_k: int = 5, vector_db_type: str = "FAISS") -> Dict[str, Any]:
    results = vectorstore.similarity_search_with_score(query, k=top_k)

    source_docs = []
    scores = []

    for doc, raw_score in results:
        normalized = normalize_similarity_score(raw_score, vector_db_type)
        doc.metadata["retrieval_score"] = normalized
        source_docs.append(doc)
        scores.append(normalized)

    avg = average_score(scores)
    confidence = confidence_label_from_score(avg)

    return {
        "source_docs": source_docs,
        "scores": scores,
        "average_score": avg,
        "confidence": confidence
    }