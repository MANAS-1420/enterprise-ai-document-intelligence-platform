import streamlit as st

def render_text_panel(title: str, content: str):
    st.markdown(f"### {title}")
    st.markdown(
        f"""
        <div class="panel-card">
            <pre style="white-space: pre-wrap; font-family: inherit;">{content}</pre>
        </div>
        """,
        unsafe_allow_html=True
    )