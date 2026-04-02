from langchain_core.prompts import ChatPromptTemplate
from config.prompts import EXEC_SUMMARY_PROMPT, KEY_INSIGHTS_PROMPT

def generate_executive_summary(text: str, llm) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", EXEC_SUMMARY_PROMPT),
        ("human", "{text}")
    ])
    chain = prompt | llm
    return chain.invoke({"text": text[:25000]}).content

def generate_key_insights(text: str, llm) -> str:
    prompt = ChatPromptTemplate.from_messages([
        ("system", KEY_INSIGHTS_PROMPT),
        ("human", "{text}")
    ])
    chain = prompt | llm
    return chain.invoke({"text": text[:25000]}).content