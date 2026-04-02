from langchain_core.prompts import ChatPromptTemplate
from config.prompts import QUERY_REWRITE_PROMPT

def rewrite_query(user_query: str, llm) -> str:
    try:
        prompt = ChatPromptTemplate.from_messages([
            ("system", QUERY_REWRITE_PROMPT),
            ("human", "{question}")
        ])
        chain = prompt | llm
        response = chain.invoke({"question": user_query})
        return response.content.strip()
    except Exception:
        return user_query