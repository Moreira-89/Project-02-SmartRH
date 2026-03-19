from langchain_groq import ChatGroq
from typing import Optional
from dotenv import load_dotenv
from pydantic import SecretStr
import os


class LangChainConfig():
    def __init__(self, model_id: str = "llama-3.3-70b-versatile"):
        try:
            load_dotenv()
            self.model_id = model_id
            self.client = ChatGroq(
                api_key=SecretStr(os.getenv("LANGCHAIN_GROQ_API_KEY", "")),
                model=self.model_id
            )
        except Exception as e:
            raise RuntimeError(f"Erro na configuração do LangChain: {str(e)}")

    def generate_response(self, prompt: str) -> Optional[str]:
        try:
            response = self.client.invoke(prompt)
            content = response.content
            if isinstance(content, list):
                return str(content)
            return content
        except Exception as e:
            print(f"Erro na geração de resposta: {str(e)}")
            return None