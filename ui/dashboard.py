import pandas as pd
import plotly.express as px
import streamlit as st

def render_dashboard_metrics(chunks_df: pd.DataFrame, top_keywords=None):
    st.markdown("### 📊 Document Dashboard")

    total_chunks = len(chunks_df)
    total_docs = chunks_df["document_name"].nunique() if not chunks_df.empty else 0
    avg_chunk_len = int(chunks_df["content"].str.len().mean()) if not chunks_df.empty else 0

    c1, c2, c3 = st.columns(3)
    c1.metric("Documents", total_docs)
    c2.metric("Chunks", total_chunks)
    c3.metric("Avg Chunk Length", avg_chunk_len)

    if not chunks_df.empty:
        dist_df = (
            chunks_df.groupby("document_name")
            .size()
            .reset_index(name="chunk_count")
            .sort_values("chunk_count", ascending=False)
        )

        fig = px.bar(
            dist_df,
            x="document_name",
            y="chunk_count",
            title="Chunks per Document"
        )
        st.plotly_chart(fig, use_container_width=True)

    if top_keywords:
        keyword_df = pd.DataFrame(top_keywords, columns=["keyword", "count"])
        fig2 = px.bar(
            keyword_df,
            x="keyword",
            y="count",
            title="Top Keywords"
        )
        st.plotly_chart(fig2, use_container_width=True)