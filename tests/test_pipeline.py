from src.preprocessing.cleaner import clean_text
from src.analytics.document_classifier import detect_document_type
from src.analytics.keyword_extractor import extract_top_keywords


def test_clean_text():
    raw_text = "Hello   \n\n world \u0000"
    cleaned = clean_text(raw_text)
    assert cleaned == "Hello world"


def test_detect_document_type_legal():
    text = "This agreement includes liability, indemnity, confidentiality and termination clause."
    doc_type = detect_document_type(text)
    assert doc_type == "Legal / Contract Document"


def test_detect_document_type_financial():
    text = "The revenue, profit, expense and cash flow increased in this financial year."
    doc_type = detect_document_type(text)
    assert doc_type == "Financial / Report Document"


def test_extract_top_keywords():
    text = "payment payment penalty penalty penalty agreement agreement clause clause liability"
    keywords = extract_top_keywords(text, top_n=3)

    assert isinstance(keywords, list)
    assert len(keywords) > 0
    assert keywords[0][0] == "penalty"