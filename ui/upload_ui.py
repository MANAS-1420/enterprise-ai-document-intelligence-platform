import streamlit as st

def render_upload_section():
    st.markdown(
        """
        <div class="glass-card">
            <div class="section-title">📂 Upload Documents</div>
            <div class="small-note">Upload PDF, TXT, or DOCX files to build your document intelligence workspace.</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_files = st.file_uploader(
        "Upload PDF, TXT, DOCX files",
        type=["pdf", "txt", "docx"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )
    return uploaded_files
