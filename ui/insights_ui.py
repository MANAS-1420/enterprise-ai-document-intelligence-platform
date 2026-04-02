import streamlit as st

def render_text_panel(title: str, content: str):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(
        f"""
        <div class="panel-card">
            <pre style="white-space: pre-wrap; font-family: Inter, Segoe UI, sans-serif; color: #e5e7eb;">{content}</pre>
        </div>
        """,
        unsafe_allow_html=True
    )
