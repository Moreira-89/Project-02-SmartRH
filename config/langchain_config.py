from langchain_groq import ChatGroq
import streamlit as st
from typing import Optional

class LangChainConfig():
    def __init__(self, model_id: str = "llama-3.3-70b-versatile"):
        try:
            self.model_id = model_id
            self.client = ChatGroq(
                api_key=st.secrets["LANGCHAIN_GROG"]["API_KEY"],
                model=self.model_id
            )
        except Exception as e:
            raise RuntimeError(f"Erro na configuração do LangChain: {str(e)}")

    def generate_response(self, prompt: str) -> Optional[str]:
        try:
            response = self.client.invoke(prompt)
            return response.content
        except Exception as e:
            print(f"Erro na geração de resposta: {str(e)}")
            return None