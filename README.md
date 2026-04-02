# 🚀 Enterprise AI Document Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![GenAI](https://img.shields.io/badge/GenAI-Project-purple)

---

## 📌 Overview

An **enterprise-grade GenAI application** that enables intelligent analysis of business documents using **Retrieval-Augmented Generation (RAG)**.

This project goes beyond a simple “chat with PDF” — it provides:
- 📊 Business insights  
- ⚠️ Risk analysis  
- 📜 Clause extraction  
- ⚖️ Document comparison  
- 🧠 Explainable AI outputs  

Built with a **production-style architecture** and deployed using **Streamlit Cloud**.

---

## ✨ Features

### 🧠 Core AI Capabilities
- Multi-document upload (PDF, DOCX, TXT)
- RAG-based question answering
- Query rewriting for better retrieval
- Source-grounded responses
- Confidence scoring + explainability

### 📊 Business Intelligence
- Executive summary generation
- Key insights extraction
- Risk detection (fraud, penalties, breach, etc.)
- Clause extraction (payment, liability, termination)
- Document type detection

### ⚖️ Advanced Features
- Multi-document comparison
- Follow-up question generation
- Keyword extraction
- Search inside document chunks
- Downloadable TXT & PDF reports

### 🎨 UI & Experience
- Premium dark SaaS-style UI
- Interactive dashboard with Plotly
- Chunk-level source visualization
- Clean modular frontend (Streamlit)

---

## 🏗️ Architecture

```text
Document → Loader → Cleaner → Chunking → Embeddings → Vector DB
         → Retriever → LLM → Structured Answer + Insights
