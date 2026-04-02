from typing import Dict, Any, List
from langchain_core.prompts import ChatPromptTemplate
from config.prompts import SYSTEM_RAG_PROMPT

def format_context(docs: List) -> str:
    context_parts = []
    for i, doc in enumerate(docs, start=1):
        source = doc.metadata.get("document_name", "unknown")
        page = doc.metadata.get("page", "NA")
        chunk_index = doc.metadata.get("chunk_index", "NA")
        score = doc.metadata.get("retrieval_score", 0.0)

        context_parts.append(
            f"[Chunk {i} | Source: {source} | Page: {page} | Chunk ID: {chunk_index} | Score: {score}]\n"
            f"{doc.page_content}"
        )

    return "\n\n".join(context_parts)

def extract_retrieval_reasons(user_query: str, docs: List) -> List[str]:
    query_terms = [word.strip().lower() for word in user_query.split() if len(word.strip()) > 3]
    matched_terms = set()

    for doc in docs:
        content_lower = doc.page_content.lower()
        for term in query_terms:
            if term in content_lower:
                matched_terms.add(term)

    reasons = []
    if matched_terms:
        reasons.append("Retrieved chunks contain matching query terms: " + ", ".join(sorted(list(matched_terms))[:8]))
    if len(docs) > 1:
        reasons.append("Multiple chunks contributed to the answer.")
    scores = [doc.metadata.get("retrieval_score", 0.0) for doc in docs]
    if scores:
        reasons.append(f"Average retrieval relevance is {sum(scores)/len(scores):.2f}.")
    return reasons

def run_rag_query(user_query: str, source_docs: List, llm, confidence: str) -> Dict[str, Any]:
    context = format_context(source_docs)

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_RAG_PROMPT),
        ("human", "Question: {question}\n\nContext:\n{context}")
    ])

    chain = prompt | llm
    response = chain.invoke({
        "question": user_query,
        "context": context
    })

    explainability = extract_retrieval_reasons(user_query, source_docs)

    return {
        "answer": response.content,
        "source_docs": source_docs,
        "confidence": confidence,
        "explainability": explainability
    }