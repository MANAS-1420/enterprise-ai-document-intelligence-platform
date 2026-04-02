import pandas as pd
import plotly.express as px
import streamlit as st

def render_dashboard_metrics(chunks_df: pd.DataFrame, top_keywords=None):
    st.markdown('<div class="section-title">📊 Document Dashboard</div>', unsafe_allow_html=True)

    total_chunks = len(chunks_df)
    total_docs = chunks_df["document_name"].nunique() if not chunks_df.empty else 0
    avg_chunk_len = int(chunks_df["content"].str.len().mean()) if not chunks_df.empty else 0

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Documents</div>
                <div class="metric-value">{total_docs}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Chunks</div>
                <div class="metric-value">{total_chunks}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">Avg Chunk Length</div>
                <div class="metric-value">{avg_chunk_len}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

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
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(17,24,39,0.0)",
            font=dict(color="#e5e7eb"),
            title_font=dict(size=18),
            xaxis_title="Document",
            yaxis_title="Chunk Count"
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
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(17,24,39,0.0)",
            font=dict(color="#e5e7eb"),
            title_font=dict(size=18),
            xaxis_title="Keyword",
            yaxis_title="Frequency"
        )
        st.plotly_chart(fig2, use_container_width=True)
