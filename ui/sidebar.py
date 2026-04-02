import streamlit as st

def render_sidebar():
    st.sidebar.markdown("## ⚙️ Workspace Settings")
    st.sidebar.markdown(
        '<p class="small-note">Configure your model, retrieval, and display settings.</p>',
        unsafe_allow_html=True
    )

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
    st.sidebar.markdown("### 🚀 Workflow")
    st.sidebar.markdown(
        """
        1. Upload documents  
        2. Build knowledge base  
        3. Chat with documents  
        4. Generate summaries and reports
        """
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🧠 Project Mode")
    st.sidebar.info("Enterprise AI Document Intelligence Platform")

    return {
        "llm_provider": llm_provider,
        "vector_db": vector_db,
        "top_k": top_k,
        "show_chunks": show_chunks,
        "enable_query_rewrite": enable_query_rewrite
    }
