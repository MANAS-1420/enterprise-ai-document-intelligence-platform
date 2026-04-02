import streamlit as st

def render_upload_section():
    st.markdown("### 📂 Upload Documents")
    uploaded_files = st.file_uploader(
        "Upload PDF, TXT, DOCX files",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True
    )
    return uploaded_files
