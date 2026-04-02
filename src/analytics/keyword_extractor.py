import re
from collections import Counter
from typing import List, Tuple
from config.settings import STOPWORDS

def extract_top_keywords(text: str, top_n: int = 12) -> List[Tuple[str, int]]:
    words = re.findall(r"\b[a-zA-Z]{4,}\b", text.lower())
    filtered = [
        word for word in words
        if word not in STOPWORDS and not word.isdigit()
    ]
    counter = Counter(filtered)
    return counter.most_common(top_n)