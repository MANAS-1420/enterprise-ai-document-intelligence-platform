from langchain_core.prompts import ChatPromptTemplate
from config.prompts import FOLLOWUP_PROMPT

def generate_followup_questions(question: str, answer: str, llm) -> str:
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", FOLLOWUP_PROMPT),
            ("human", "Question: {question}\n\nAnswer: {answer}")
        ])
        chain = prompt | llm
        return chain.invoke({"question": question, "answer": answer[:4000]}).content
    except Exception:
        return (
            "- What are the key obligations?\n"
            "- Are there any major risks?\n"
            "- Which clauses matter most?\n"
            "- What action should be taken next?"
        )