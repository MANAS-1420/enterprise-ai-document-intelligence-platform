import os
import streamlit as st
import pandas as pd

from config.settings import APP_TITLE, APP_SUBTITLE, RAW_DATA_DIR
from src.utils.helpers import (
    ensure_dir,
    save_uploaded_file,
    docs_to_dataframe,
    build_download_text,
    highlight_keywords_html,
    pretty_score,
    keyword_search_dataframe
)
from src.utils.logger import get_logger
from src.utils.pdf_export import export_report_to_pdf

from src.loaders.pdf_loader import load_pdf
from src.loaders.docx_loader import load_docx
from src.loaders.text_loader import load_text

from src.preprocessing.cleaner import clean_documents
from src.preprocessing.chunker import chunk_documents

from src.embeddings.embedding_model import get_embedding_model
from src.vectorstore.vectordb import build_faiss_vectorstore, build_chroma_vectorstore

from src.rag.retriever import retrieve_with_scores
from src.rag.query_rewriter import rewrite_query
from src.rag.rag_chain import run_rag_query
from src.rag.intent_router import classify_query_intent

from src.llm.llm_provider import get_llm

from src.analytics.insights import generate_executive_summary, generate_key_insights
from src.analytics.risk_analyzer import detect_risks_rule_based
from src.analytics.clause_extractor import extract_clauses_rule_based
from src.analytics.document_classifier import detect_document_type
from src.analytics.keyword_extractor import extract_top_keywords
from src.analytics.followup_generator import generate_followup_questions
from src.comparison.compare_docs import compare_two_documents

from ui.sidebar import render_sidebar
from ui.upload_ui import render_upload_section
from ui.chat_ui import render_chat_history, append_chat
from ui.dashboard import render_dashboard_metrics
from ui.insights_ui import render_text_panel

logger = get_logger()

st.set_page_config(
    page_title="Enterprise AI Document Intelligence Platform",
    page_icon="📘",
    layout="wide"
)

def load_css():
    css_path = "assets/styles.css"
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def init_session():
    defaults = {
        "raw_docs": [],
        "chunks": [],
        "vectorstore": None,
        "knowledge_ready": False,
        "combined_text": "",
        "doc_names": [],
        "summary_text": "",
        "insights_text": "",
        "risks_text": "",
        "clauses_text": "",
        "comparison_text": "",
        "doc_type": "",
        "top_keywords": [],
        "chunks_df": pd.DataFrame(),
        "chat_history": [],
        "vector_db_type": "FAISS"
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def load_documents_from_paths(file_paths):
    all_docs = []

    for path in file_paths:
        ext = os.path.splitext(path)[1].lower()

        if ext == ".pdf":
            docs = load_pdf(path)
        elif ext == ".docx":
            docs = load_docx(path)
        elif ext == ".txt":
            docs = load_text(path)
        else:
            continue

        all_docs.extend(docs)

    return all_docs

@st.cache_resource(show_spinner=False)
def cached_embedding_model():
    return get_embedding_model()

def build_knowledge_base(uploaded_files, vector_db_choice, top_k):
    ensure_dir(RAW_DATA_DIR)

    saved_paths = []
    doc_names = []

    for uploaded_file in uploaded_files:
        saved_path = save_uploaded_file(uploaded_file, RAW_DATA_DIR)
        saved_paths.append(saved_path)
        doc_names.append(uploaded_file.name)

    raw_docs = load_documents_from_paths(saved_paths)
    raw_docs = clean_documents(raw_docs)
    chunks = chunk_documents(raw_docs)

    embedding_model = cached_embedding_model()

    if vector_db_choice == "FAISS":
        vectorstore = build_faiss_vectorstore(chunks, embedding_model)
    else:
        vectorstore = build_chroma_vectorstore(chunks, embedding_model)

    combined_text = "\n\n".join([doc.page_content for doc in raw_docs])
    chunks_df = docs_to_dataframe(chunks)
    doc_type = detect_document_type(combined_text)
    top_keywords = extract_top_keywords(combined_text, top_n=12)

    st.session_state.raw_docs = raw_docs
    st.session_state.chunks = chunks
    st.session_state.vectorstore = vectorstore
    st.session_state.knowledge_ready = True
    st.session_state.combined_text = combined_text
    st.session_state.doc_names = doc_names
    st.session_state.chunks_df = chunks_df
    st.session_state.doc_type = doc_type
    st.session_state.top_keywords = top_keywords
    st.session_state.vector_db_type = vector_db_choice

    logger.info("Knowledge base built successfully.")

def handle_chat_query(user_query: str, llm, config):
    intent = classify_query_intent(user_query)
    final_query = user_query

    if config["enable_query_rewrite"] and intent in ["qa", "search", "risk_analysis", "clause_extraction"]:
        final_query = rewrite_query(user_query, llm)

    append_chat("user", user_query)

    if intent == "summary":
        answer = st.session_state.summary_text
        if not answer:
            answer = generate_executive_summary(st.session_state.combined_text, llm)
            st.session_state.summary_text = answer

        append_chat("assistant", answer)
        return {
            "mode": "summary",
            "answer": answer,
            "source_docs": [],
            "confidence": "High",
            "explainability": ["Intent router detected a summary request."]
        }

    if intent == "risk_analysis":
        answer = detect_risks_rule_based(st.session_state.combined_text)
        st.session_state.risks_text = answer
        append_chat("assistant", answer)
        return {
            "mode": "risk_analysis",
            "answer": answer,
            "source_docs": [],
            "confidence": "Medium",
            "explainability": ["Intent router detected a risk analysis request."]
        }

    if intent == "clause_extraction":
        answer = extract_clauses_rule_based(st.session_state.combined_text)
        st.session_state.clauses_text = answer
        append_chat("assistant", answer)
        return {
            "mode": "clause_extraction",
            "answer": answer,
            "source_docs": [],
            "confidence": "Medium",
            "explainability": ["Intent router detected a clause extraction request."]
        }

    retrieval_result = retrieve_with_scores(
        vectorstore=st.session_state.vectorstore,
        query=final_query,
        top_k=config["top_k"],
        vector_db_type=st.session_state.vector_db_type
    )

    rag_result = run_rag_query(
        user_query=user_query,
        source_docs=retrieval_result["source_docs"],
        llm=llm,
        confidence=retrieval_result["confidence"]
    )

    append_chat("assistant", rag_result["answer"])

    return {
        "mode": "qa",
        "answer": rag_result["answer"],
        "source_docs": rag_result["source_docs"],
        "confidence": rag_result["confidence"],
        "explainability": rag_result["explainability"],
        "average_score": retrieval_result["average_score"]
    }

def main():
    load_css()
    init_session()

    st.markdown(
        f"""
        <div class="hero-card">
            <div class="main-title">{APP_TITLE}</div>
            <div class="sub-title">{APP_SUBTITLE}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    config = render_sidebar()
    uploaded_files = render_upload_section()

    col_a, col_b = st.columns([1.2, 2])

    with col_a:
        if st.button("🚀 Build Knowledge Base", use_container_width=True):
            if not uploaded_files:
                st.warning("Please upload at least one document first.")
            else:
                try:
                    with st.spinner("Building enterprise knowledge base..."):
                        build_knowledge_base(
                            uploaded_files=uploaded_files,
                            vector_db_choice=config["vector_db"],
                            top_k=config["top_k"]
                        )
                    st.success("Knowledge base built successfully.")
                except Exception as e:
                    logger.exception("Failed to build knowledge base.")
                    st.error("Unable to process uploaded documents. Please check document format and try again.")
                    st.exception(e)

    with col_b:
        if st.session_state.knowledge_ready:
            st.success(f"Knowledge base ready for {len(st.session_state.doc_names)} document(s).")
            st.caption("Uploaded: " + ", ".join(st.session_state.doc_names))

            st.markdown(
                f"""
                <span class="badge">Detected Type: {st.session_state.doc_type}</span>
                """,
                unsafe_allow_html=True
            )

            for kw, count in st.session_state.top_keywords[:6]:
                st.markdown(
                    f"""<span class="badge">{kw} ({count})</span>""",
                    unsafe_allow_html=True
                )

    if st.session_state.knowledge_ready:
        tabs = st.tabs([
            "💬 Chat",
            "🧾 Executive Summary",
            "🔍 Insights / Risks / Clauses",
            "⚖️ Compare Documents",
            "📊 Dashboard"
        ])

        llm = None
        try:
            llm = get_llm(provider=config["llm_provider"])
        except Exception as e:
            st.error(f"LLM initialization failed: {e}")

        with tabs[0]:
            render_chat_history()
            user_query = st.chat_input("Ask anything about the uploaded documents...")

            if user_query and llm:
                try:
                    with st.spinner("Analyzing your question..."):
                        result = handle_chat_query(user_query, llm, config)

                    with st.chat_message("assistant"):
                        st.markdown(result["answer"])

                        st.markdown("### ✅ Confidence")
                        avg_score = result.get("average_score", 0.0)
                        if avg_score:
                            st.markdown(f"**{result['confidence']}** | Avg relevance: **{pretty_score(avg_score)}**")
                        else:
                            st.markdown(f"**{result['confidence']}**")

                        st.markdown("### 🧠 Why this answer?")
                        for reason in result["explainability"]:
                            st.markdown(f"- {reason}")

                        if result["mode"] == "qa":
                            st.markdown("### 💡 Suggested Follow-up Questions")
                            followups = generate_followup_questions(user_query, result["answer"], llm)
                            st.markdown(followups)

                    if config["show_chunks"] and result.get("source_docs"):
                        st.markdown("### 📚 Source Chunks")
                        highlight_terms = ["risk", "penalty", "fraud", "termination", "liability", "payment"]

                        for i, doc in enumerate(result["source_docs"], start=1):
                            score = doc.metadata.get("retrieval_score", 0.0)
                            highlighted_text = highlight_keywords_html(doc.page_content[:900], highlight_terms)

                            st.markdown(
                                f"""
                                <div class="source-box">
                                    <b>Chunk {i}</b><br>
                                    <b>Document:</b> {doc.metadata.get('document_name', 'unknown')}<br>
                                    <b>Page:</b> {doc.metadata.get('page', 'NA')}<br>
                                    <b>Chunk Index:</b> {doc.metadata.get('chunk_index', 'NA')}<br>
                                    <b>Relevance Score:</b> {pretty_score(score)}<br><br>
                                    {highlighted_text}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                except Exception as e:
                    logger.exception("Chat query failed.")
                    st.error("Error while answering query. Please try a different question.")
                    st.exception(e)

        with tabs[1]:
            st.markdown("### 🧾 Executive Summary")
            if st.button("Generate Executive Summary", use_container_width=True) and llm:
                try:
                    with st.spinner("Generating executive summary..."):
                        summary = generate_executive_summary(st.session_state.combined_text, llm)
                        st.session_state.summary_text = summary
                except Exception as e:
                    logger.exception("Summary generation failed.")
                    st.error("Failed to generate summary.")
                    st.exception(e)

            if st.session_state.summary_text:
                render_text_panel("Executive Summary", st.session_state.summary_text)

        with tabs[2]:
            c1, c2, c3 = st.columns(3)

            with c1:
                if st.button("Generate Insights", use_container_width=True) and llm:
                    try:
                        with st.spinner("Extracting insights..."):
                            st.session_state.insights_text = generate_key_insights(
                                st.session_state.combined_text, llm
                            )
                    except Exception as e:
                        st.error("Insights generation failed.")
                        st.exception(e)

            with c2:
                if st.button("Analyze Risks", use_container_width=True):
                    st.session_state.risks_text = detect_risks_rule_based(
                        st.session_state.combined_text
                    )

            with c3:
                if st.button("Extract Clauses", use_container_width=True):
                    st.session_state.clauses_text = extract_clauses_rule_based(
                        st.session_state.combined_text
                    )

            if st.session_state.insights_text:
                render_text_panel("Key Insights", st.session_state.insights_text)

            if st.session_state.risks_text:
                render_text_panel("Risk Analysis", st.session_state.risks_text)

            if st.session_state.clauses_text:
                render_text_panel("Clause Extraction", st.session_state.clauses_text)

            st.markdown("### 🔑 Top Keywords")
            if st.session_state.top_keywords:
                keyword_lines = "\n".join([f"- {kw}: {count}" for kw, count in st.session_state.top_keywords])
                render_text_panel("Top Keywords", keyword_lines)

            if any([
                st.session_state.summary_text,
                st.session_state.insights_text,
                st.session_state.risks_text,
                st.session_state.clauses_text
            ]):
                report_text = build_download_text(
                    summary=st.session_state.summary_text,
                    insights=st.session_state.insights_text,
                    risks=st.session_state.risks_text,
                    clauses=st.session_state.clauses_text,
                    doc_type=st.session_state.doc_type,
                    keywords=st.session_state.top_keywords
                )

                st.download_button(
                    label="⬇️ Download TXT Report",
                    data=report_text,
                    file_name="enterprise_doc_intelligence_report.txt",
                    mime="text/plain"
                )

                if st.button("📄 Generate PDF Report", use_container_width=True):
                    try:
                        with st.spinner("Generating PDF report..."):
                            pdf_path = export_report_to_pdf(
                                doc_type=st.session_state.doc_type,
                                summary=st.session_state.summary_text,
                                insights=st.session_state.insights_text,
                                risks=st.session_state.risks_text,
                                clauses=st.session_state.clauses_text,
                                comparison=st.session_state.comparison_text
                            )
                        with open(pdf_path, "rb") as pdf_file:
                            st.download_button(
                                label="⬇️ Download PDF Report",
                                data=pdf_file,
                                file_name="enterprise_doc_intelligence_report.pdf",
                                mime="application/pdf"
                            )
                    except Exception as e:
                        st.error("PDF report generation failed.")
                        st.exception(e)

        with tabs[3]:
            st.markdown("### ⚖️ Compare Documents")
            doc_names = st.session_state.doc_names

            if len(doc_names) < 2:
                st.info("Upload at least 2 documents to use comparison.")
            elif llm:
                doc_a = st.selectbox("Select Document A", doc_names, index=0)
                doc_b = st.selectbox("Select Document B", doc_names, index=1)

                if st.button("Compare Selected Documents", use_container_width=True):
                    try:
                        with st.spinner("Comparing selected documents..."):
                            docs_map = {}
                            for doc in st.session_state.raw_docs:
                                name = doc.metadata.get("document_name")
                                docs_map.setdefault(name, []).append(doc.page_content)

                            text_a = "\n".join(docs_map.get(doc_a, []))
                            text_b = "\n".join(docs_map.get(doc_b, []))

                            comparison_result = compare_two_documents(text_a, text_b, llm)
                            st.session_state.comparison_text = comparison_result

                        render_text_panel("Document Comparison Result", comparison_result)
                    except Exception as e:
                        st.error("Comparison failed.")
                        st.exception(e)

        with tabs[4]:
            render_dashboard_metrics(st.session_state.chunks_df, st.session_state.top_keywords)

            if not st.session_state.chunks_df.empty:
                st.markdown("### 🔎 Search Inside Chunks")
                keyword = st.text_input("Enter keyword to search in processed chunks")

                if keyword:
                    filtered = keyword_search_dataframe(st.session_state.chunks_df, keyword)
                    st.dataframe(filtered, use_container_width=True)

if __name__ == "__main__":
    main()