from config.langchain_config import LangChainConfig
from typing import Optional
import logging
import re

logger = logging.getLogger(__name__)

class LangChainService():
    def __init__(self, config_langchain: LangChainConfig):
        self.llm = config_langchain

    def resume_cv(self, cv: str) -> Optional[str]:
        
        prompt = self._build_prompt(cv)
        
        try:
            result_raw = self.llm.generate_response(prompt)

            result = result_raw.split('```markdown')[1]
        except:
            result = result_raw

            print(result)
        
        return result

    def _build_prompt(self, cv: str) -> str:
        return f"""
        Extraia informações do currículo abaixo seguindo EXATAMENTE este formato:

        ```markdown
        ## Nome Completo
        [Nome completo do candidato]

        ## Habilidades Técnicas
        - [Pelo menos 3 habilidades técnicas]
        - [Ou "Nenhuma habilidade técnica especificada"]

        ## Formação Acadêmica
        - [Curso] na [Instituição] ([Ano])
        - [Ou "Formação não especificada"]

        ## Idiomas
        - [Idioma] ([Nível])
        - [Ou "Idiomas não especificados"]
        ```

        Regras obrigatórias:
        1. Mantenha todas as seções mesmo sem dados
        2. Use marcadores '-' para listas
        3. Priorize informações técnicas

        Dados do currículo:
        {cv[:8000]}
        """
    
    def generate_score(self, cv, job, max_attempts=10):
        # Criar o prompt para calcular a pontuação do currículo com base na vaga
        prompt = f'''
            **Objetivo:** Avaliar um currículo com base em uma vaga específica e calcular a pontuação final. A nota máxima é 10.0.

            **Instruções:**

            1. **Experiência (Peso: 30%)**: Avalie a relevância da experiência em relação à vaga.
            2. **Habilidades Técnicas (Peso: 25%)**: Verifique o alinhamento das habilidades técnicas com os requisitos da vaga.
            3. **Educação (Peso: 10%)**: Avalie a relevância da formação acadêmica para a vaga.
            4. **Idiomas (Peso: 10%)**: Avalie os idiomas e sua proficiência em relação à vaga.
            5. **Pontos Fortes (Peso: 15%)**: Avalie a relevância dos pontos fortes para a vaga.
            6. **Pontos Fracos (Desconto de até 10%)**: Avalie a gravidade dos pontos fracos em relação à vaga.
            
            Curriculo do candidato
            
            {cv}
            
            Vaga que o candidato está se candidatando
            
            {job}

            **Formato Exigido:**
            A resposta DEVE conter APENAS:
            ``` 
            Pontuação Final: X.X 
            ```
            Onde X.X é um número entre 0.0 e 10.0

            **Atenção:** Seja rigoroso ao atribuir as notas. A nota máxima é 10.0, e o output deve conter apenas "Pontuação Final: x.x".
            '''
        
        for attempt in range(max_attempts):
            try:
                result_raw = self.llm.generate_response(prompt=prompt)
                score = self.extract_score_from_result(result_raw)
                
                if score is not None:
                    return score
                    
            except Exception as e:
                logger.error(f"Tentativa {attempt+1} falhou: {str(e)}")
        
        # Fallback se todas as tentativas falharem
        return 0.0
    
    def extract_score_from_result(self, result_raw: str) -> Optional[float]:
        '''Extrai a pontuação final com tratamento robusto'''
        patterns = [
            r"(?i)Pontuação Final\s*:\s*([0-9]+\.[0-9])",
            r"(?i)Score\s*:\s*([0-9]\.[0-9])",             
            r"\b([0-9]\.[0-9])/10",                       
            r"\b(\d{1,2})\s*/\s*10"                       
        ]
        
        for pattern in patterns:
            match = re.search(pattern, result_raw or "")
            if match:
                try:
                    score_str = match.group(1).replace(',', '.')
                    score = float(score_str)
                    
                    # Garante que a pontuação está entre 0 e 10
                    if 0 <= score <= 10:
                        return round(score, 1)
                        
                except (ValueError, TypeError):
                    continue
                    
        return None
    
    def generate_opnion(self, cv, job):
        prompt = f"""
        Gere uma análise detalhada em formato Markdown contendo:

        ### Pontos Fortes
        - Liste 3-5 pontos positivos relevantes para a vaga

        ### Pontos a Desenvolver  
        - Liste 2-3 áreas de melhoria

        ### Recomendações
        - Sugira cursos ou certificações úteis

        Baseado no currículo:
        {cv[:8000]}

        E nos requisitos da vaga:
        {job[:2000]}
        """
        response = self.llm.generate_response(prompt)
        return response if response else "*Análise não disponível*"