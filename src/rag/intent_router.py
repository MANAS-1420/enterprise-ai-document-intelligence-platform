def classify_query_intent(query: str) -> str:
    q = query.lower().strip()

    comparison_words = ["compare", "difference", "differences", "vs", "versus"]
    summary_words = ["summary", "summarize", "summarise", "overview", "brief"]
    risk_words = ["risk", "risks", "issue", "issues", "warning", "liability", "fraud", "penalty"]
    clause_words = ["clause", "clauses", "terms", "agreement terms", "obligations", "payment terms"]
    search_words = ["find", "search", "locate", "look for"]

    if any(word in q for word in comparison_words):
        return "comparison"
    if any(word in q for word in summary_words):
        return "summary"
    if any(word in q for word in risk_words):
        return "risk_analysis"
    if any(word in q for word in clause_words):
        return "clause_extraction"
    if any(word in q for word in search_words):
        return "search"
    return "qa"