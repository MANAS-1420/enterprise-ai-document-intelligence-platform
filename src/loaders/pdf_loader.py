from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    for doc in docs:
        doc.metadata["source"] = file_path
        doc.metadata["document_name"] = file_path.split("/")[-1].split("\\")[-1]

    return docs