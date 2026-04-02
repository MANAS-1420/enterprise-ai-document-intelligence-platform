from config.settings import RISK_KEYWORDS

def detect_risks_rule_based(text: str) -> str:
    text_lower = text.lower()
    found = [kw for kw in RISK_KEYWORDS if kw in text_lower]

    if not found:
        return "No obvious high-risk keywords detected through rule-based scan."

    lines = ["Potential risk indicators found:"]
    for kw in found:
        lines.append(f"- {kw}")

    if any(k in found for k in ["fraud", "breach", "lawsuit", "termination", "default"]):
        lines.append("\nOverall Risk Level: High")
    elif len(found) >= 3:
        lines.append("\nOverall Risk Level: Medium")
    else:
        lines.append("\nOverall Risk Level: Low to Medium")

    return "\n".join(lines)