import re
from typing import List

def clean_text(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\u0000", "", text)
    return text.strip()

def clean_documents(docs: List):
    for doc in docs:
        doc.page_content = clean_text(doc.page_content)
    return docs