import os

from langchain_openai import ChatOpenAI


def get_llm():
    api_key = os.environ.get('OPENAI_API_KEY', '')
    model = os.environ.get('OPENAI_MODEL', 'gpt-4.1-nano')

    if not api_key:
        return None

    return ChatOpenAI(api_key=api_key, model=model, temperature=0.3)
