from Project_02_SmartRH.config.langchain_config import LangChainConfig
from typing import Optional, Any
import logging
import re
import textwrap

logger = logging.getLogger(__name__)

# Constantes para prompts
RESUME_PROMPT_TEMPLATE = textwrap.dedent("""
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
    1. Mantenha todas as seções mesmo sem dados.
    2. Use marcadores '-' para listas.
    3. Priorize informações técnicas.

    Dados do currículo:
    {cv}
""")

SCORE_PROMPT_TEMPLATE = textwrap.dedent("""
    **Objetivo:** Avaliar um currículo com base em uma vaga específica e calcular a pontuação final. A nota máxima é 10.0.

    **Instruções:**

    1. **Experiência (Peso: 30%)**: Avalie a relevância da experiência em relação à vaga.
    2. **Habilidades Técnicas (Peso: 25%)**: Verifique o alinhamento das habilidades técnicas com os requisitos da vaga.
    3. **Educação (Peso: 10%)**: Avalie a relevância da formação acadêmica para a vaga.
    4. **Idiomas (Peso: 10%)**: Avalie os idiomas e sua proficiência em relação à vaga.
    5. **Pontos Fortes (Peso: 15%)**: Avalie a relevância dos pontos fortes para a vaga.
    6. **Pontos Fracos (Desconto de até 10%)**: Avalie a gravidade dos pontos fracos em relação à vaga.
    
    **Curriculo do candidato:**
    {cv}
    
    **Vaga que o candidato está se candidatando:**
    Título da Vaga: {job_title}
    Atividades Principais: {job_main_activity}
    Pré-requisitos: {job_prerequisites}
    Diferenciais: {job_differentials}

    **Formato Exigido:**
    A resposta DEVE conter APENAS:
    ``` 
    Pontuação Final: X.X 
    ```
    Onde X.X é um número entre 0.0 e 10.0.

    **Atenção:** Seja rigoroso ao atribuir as notas. A nota máxima é 10.0, e o output deve conter apenas "Pontuação Final: x.x".
""")

OPINION_PROMPT_TEMPLATE = textwrap.dedent("""
    Gere uma análise detalhada em formato Markdown contendo:

    ### Pontos Fortes
    - Liste 3-5 pontos positivos relevantes para a vaga.

    ### Pontos a Desenvolver  
    - Liste 2-3 áreas de melhoria.

    ### Recomendações
    - Sugira cursos ou certificações úteis.

    Baseado no currículo:
    {cv}

    E nos requisitos da vaga:
    {job_prerequisites}
""")

SCORE_EXTRACTION_PATTERNS = [
    r"(?i)Pontuação Final\s*:\s*([0-9]+[.,]?[0-9]*)",
    r"(?i)Score\s*:\s*([0-9]+[.,]?[0-9]*)",
    r"\b([0-9]+[.,]?[0-9]*)\s*/\s*10",
]

class LangChainService():
    def __init__(self, config_langchain: LangChainConfig):
        self.llm = config_langchain

    def resume_cv(self, cv: str) -> Optional[str]:
        """Resume um CV usando o LLM, extraindo o conteúdo de um bloco markdown."""
        prompt = RESUME_PROMPT_TEMPLATE.format(cv=cv[:8000])
        try:
            result_raw = self.llm.generate_response(prompt)
            # Extrai o conteúdo dentro do bloco de código markdown
            match = re.search(r"```markdown\n(.*?)\n```", result_raw, re.DOTALL)# type: ignore
            if match:
                return match.group(1).strip()
            return result_raw # Retorna o resultado bruto se o formato não for encontrado
        except Exception as e:
            logger.error(f"Erro ao resumir CV: {e}")
            return None

    def generate_score(self, cv: str, job: Any, max_attempts: int = 10) -> float:
        """Calcula a pontuação de um CV em relação a uma vaga, com múltiplas tentativas."""
        prompt = SCORE_PROMPT_TEMPLATE.format(
            cv=cv,
            job_title=job.title if job else "Não informado",
            job_main_activity=job.main_activity if job else "Não informado",
            job_prerequisites=job.prerequisites if job else "Não informado",
            job_differentials=job.differentials if job and job.differentials else "Nenhum",
        )
        for attempt in range(max_attempts):
            try:
                result_raw = self.llm.generate_response(prompt=prompt)
                score = self.extract_score_from_result(result_raw)
                
                if score is not None:
                    return score
            except Exception as e:
                logger.warning(f"Tentativa {attempt + 1}/{max_attempts} para gerar pontuação falhou: {e}")
        
        logger.error(f"Todas as {max_attempts} tentativas de gerar pontuação falharam.")
        return 0.0
    
    def extract_score_from_result(self, result_raw: Optional[str]) -> Optional[float]:
        """Extrai a pontuação final da resposta do LLM de forma robusta."""
        if not result_raw:
            return None

        for pattern in SCORE_EXTRACTION_PATTERNS:
            match = re.search(pattern, result_raw or "")
            if match:
                try:
                    score_str = match.group(1).replace(',', '.')
                    score = float(score_str)
                    
                    if 0 <= score <= 10:
                        return round(score, 1)
                except (ValueError, TypeError):
                    continue
                    
        return None
    
    def generate_opinion(self, cv: str, job: Any) -> str:
        """Gera uma análise qualitativa (pontos fortes, a desenvolver, etc.) sobre o candidato."""
        prompt = OPINION_PROMPT_TEMPLATE.format(
            cv=cv[:8000],
            job_prerequisites=job.prerequisites if job else "Não informado"
        )
        try:
            response = self.llm.generate_response(prompt)
            return response if response else "*Análise não disponível*"
        except Exception as e:
            logger.error(f"Erro ao gerar opinião sobre o CV: {e}")
            return "*Ocorreu um erro ao gerar a análise.*"