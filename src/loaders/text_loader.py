from langchain_core.documents import Document as LCDocument

def load_text(file_path: str):
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()

    return [
        LCDocument(
            page_content=text,
            metadata={
                "source": file_path,
                "document_name": file_path.split("/")[-1].split("\\")[-1],
                "page": 1
            }
        )
    ]