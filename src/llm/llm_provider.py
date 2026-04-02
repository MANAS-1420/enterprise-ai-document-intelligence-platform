import os

def _get_secret(key: str) -> str:
    try:
        import streamlit as st
        if key in st.secrets:
            return st.secrets[key]
    except Exception:
        pass

    return os.getenv(key, "")

def get_llm(provider: str = "Groq", temperature: float = 0.2):
    provider = provider.strip().lower()

    if provider == "gemini":
        google_api_key = _get_secret("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY not found in Streamlit secrets or environment.")

        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=google_api_key,
            temperature=temperature
        )

    if provider == "openai":
        openai_api_key = _get_secret("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in Streamlit secrets or environment.")

        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-4o-mini",
            api_key=openai_api_key,
            temperature=temperature
        )

    if provider == "groq":
        groq_api_key = _get_secret("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY not found in Streamlit secrets or environment.")

        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="llama-3.3-70b-versatile",
            api_key=groq_api_key,
            base_url="https://api.groq.com/openai/v1",
            temperature=temperature
        )

    raise ValueError(f"Unsupported provider: {provider}")