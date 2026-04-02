# Enterprise AI Document Intelligence Platform

A production-style **multi-document RAG-based GenAI application** built using **Python, Streamlit, LangChain, HuggingFace embeddings, FAISS/Chroma, and Gemini/OpenAI/Groq**.

This is not just a “chat with PDF” app. It is designed as an **enterprise AI document intelligence system** with business-focused analysis features.

---

## Features

### Core RAG Features
- Upload and analyze multiple documents
- Supports PDF, TXT, DOCX
- Intelligent chunking
- HuggingFace embeddings
- FAISS or Chroma vector database
- Source-grounded Q&A
- Chunk-level retrieval relevance score
- Query rewriting
- Session chat history

### Advanced Enterprise Features
- Executive summary generation
- Key insights extraction
- Risk analysis
- Clause extraction
- Query intent routing
- Explainability layer: “Why this answer?”
- Document type detection
- Keyword extraction
- Follow-up question suggestions
- Multi-document comparison
- Search inside processed chunks
- TXT report download
- PDF report export
- Plotly dashboard
- Premium Streamlit UI

---

## Tech Stack

- Python
- Streamlit
- LangChain
- HuggingFace Embeddings
- FAISS / Chroma
- Groq / Gemini / OpenAI
- Pandas
- Plotly
- PyPDF / DOCX / TXT loaders
- FPDF

---

## Setup

### 1. Create virtual environment
```bash
python -m venv venv