from config.settings import CLAUSE_KEYWORDS

def extract_clauses_rule_based(text: str) -> str:
    sentences = [s.strip() for s in text.replace("\n", ". ").split(".") if s.strip()]
    clause_hits = []

    for sentence in sentences:
        low = sentence.lower()
        if any(keyword in low for keyword in CLAUSE_KEYWORDS):
            clause_hits.append(sentence)

    if not clause_hits:
        return "No major clause-like sentences detected through rule-based extraction."

    unique_hits = []
    seen = set()
    for hit in clause_hits:
        if hit not in seen:
            unique_hits.append(hit)
            seen.add(hit)

    result = ["Important clause-like sections:"]
    for item in unique_hits[:15]:
        result.append(f"- {item}")

    return "\n".join(result)