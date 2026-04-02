def detect_document_type(text: str) -> str:
    t = text.lower()

    legal_keywords = [
        "agreement", "contract", "jurisdiction", "indemnity", "confidentiality",
        "termination", "liability", "governing law", "clause"
    ]
    financial_keywords = [
        "balance sheet", "revenue", "profit", "loss", "ebitda", "income statement",
        "financial year", "expense", "cash flow", "shareholder"
    ]
    research_keywords = [
        "abstract", "methodology", "literature review", "results", "conclusion",
        "dataset", "experiment", "hypothesis"
    ]
    policy_keywords = [
        "policy", "compliance", "guidelines", "framework", "regulation", "standards"
    ]

    legal_score = sum(1 for kw in legal_keywords if kw in t)
    financial_score = sum(1 for kw in financial_keywords if kw in t)
    research_score = sum(1 for kw in research_keywords if kw in t)
    policy_score = sum(1 for kw in policy_keywords if kw in t)

    scores = {
        "Legal / Contract Document": legal_score,
        "Financial / Report Document": financial_score,
        "Research / Academic Document": research_score,
        "Policy / Compliance Document": policy_score
    }

    best_type = max(scores, key=scores.get)
    if scores[best_type] == 0:
        return "Generic Business Document"
    return best_type