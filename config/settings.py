APP_TITLE = "Enterprise AI Document Intelligence Platform"
APP_SUBTITLE = (
    "Production-style multi-document RAG system for Q&A, summaries, risks, clauses, "
    "comparison, explainability, and business insights."
)

SUPPORTED_EXTENSIONS = [".pdf", ".txt", ".docx"]

DEFAULT_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_LLM_PROVIDER = "Groq"
DEFAULT_VECTOR_DB = "FAISS"

CHUNK_SIZE = 1200
CHUNK_OVERLAP = 180
TOP_K = 5
MAX_CONTEXT_CHUNKS = 6

RAW_DATA_DIR = "data/raw"
PROCESSED_DATA_DIR = "data/processed"
LOCAL_VECTORSTORE_DIR = "data/vectorstore"

RISK_KEYWORDS = [
    "penalty", "breach", "default", "delay", "termination", "fraud", "liability",
    "lawsuit", "non-compliance", "violation", "late payment", "risk", "obligation",
    "confidential", "indemnity", "dispute", "interest charge", "recovery", "warning"
]

CLAUSE_KEYWORDS = [
    "term", "termination", "payment", "liability", "warranty", "obligation",
    "confidentiality", "compliance", "notice", "renewal", "jurisdiction",
    "governing law", "indemnity", "service level", "scope", "fees"
]

STOPWORDS = {
    "the", "is", "a", "an", "and", "or", "to", "of", "for", "in", "on", "with", "by",
    "this", "that", "these", "those", "as", "are", "was", "were", "be", "been", "being",
    "at", "from", "it", "its", "into", "about", "their", "there", "if", "then", "than",
    "can", "could", "may", "might", "should", "would", "will", "shall", "not", "no",
    "such", "other", "any", "all", "also", "more", "most", "some", "our", "your", "you",
    "we", "they", "he", "she", "them", "his", "her", "but", "so", "do", "does", "did"
}