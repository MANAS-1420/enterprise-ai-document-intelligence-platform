import streamlit as st

def render_sidebar():
    st.sidebar.markdown("## ⚙️ Configuration")

    llm_provider = st.sidebar.selectbox(
        "LLM Provider",
        ["Groq", "Gemini", "OpenAI"],
        index=0
    )

    vector_db = st.sidebar.selectbox(
        "Vector Store",
        ["FAISS", "Chroma"],
        index=0
    )

    top_k = st.sidebar.slider("Top K Retrieval", min_value=2, max_value=10, value=5)
    show_chunks = st.sidebar.checkbox("Show Retrieved Chunks", value=True)
    enable_query_rewrite = st.sidebar.checkbox("Enable Query Rewrite", value=True)

    st.sidebar.markdown("---")
    st.sidebar.info(
        "Recommended flow:\n"
        "1. Upload documents\n"
        "2. Build knowledge base\n"
        "3. Chat with documents\n"
        "4. Generate summary, risks, clauses, keywords, and report"
    )

    return {
        "llm_provider": llm_provider,
        "vector_db": vector_db,
        "top_k": top_k,
        "show_chunks": show_chunks,
        "enable_query_rewrite": enable_query_rewrite
    }