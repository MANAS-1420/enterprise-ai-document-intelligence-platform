from langchain_core.prompts import ChatPromptTemplate
from config.prompts import DOC_COMPARE_PROMPT

def compare_two_documents(doc_text_a: str, doc_text_b: str, llm) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", DOC_COMPARE_PROMPT),
        ("human", "Document A:\n{doc_a}\n\nDocument B:\n{doc_b}")
    ])
    chain = prompt | llm
    response = chain.invoke({
        "doc_a": doc_text_a[:18000],
        "doc_b": doc_text_b[:18000]
    })
    return response.content