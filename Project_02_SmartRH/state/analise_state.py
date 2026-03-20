import reflex as rx
import PyPDF2
import io
from Project_02_SmartRH.models.job import Job
from Project_02_SmartRH.state.listjob_state import ListJobsState
from Project_02_SmartRH.services.firebase_service import FirebaseService
from Project_02_SmartRH.config.langchain_config import LangChainConfig
from Project_02_SmartRH.services.langchain_service import LangChainService


class AnaliseState(rx.State):
    resumo_cv: str = ""
    pontuacao_final: float = 0.0
    opiniao_gerada: str = ""
    vaga_atual: Job | None = None
    curriculo_texto: str = ""
    is_loading: bool = False

    async def carregar_vaga(self):
        estado_vaga = await self.get_state(ListJobsState)

        id_vaga = estado_vaga.vaga_selecionada_id

        if id_vaga:
            self.vaga_atual = FirebaseService().get_job(id_vaga)
        else:
            self.vaga_atual = None

    async def receber_e_processar_arquivo(self, files: list[rx.UploadFile]):
        self.is_loading = True

        yield

        if not files:
            self.is_loading = False
            return

        arquivo = files[0]

        dados_binarios = await arquivo.read()

        dados_io = io.BytesIO(dados_binarios)

        leitor = PyPDF2.PdfReader(dados_io)

        self.curriculo_texto = ""

        for pagina in leitor.pages:
            self.curriculo_texto += pagina.extract_text()

        if not self.curriculo_texto.strip():
            self.curriculo_texto = "Texto do currículo não pôde ser extraído."
            self.resumo_cv = "Nenhum resumo disponível devido à falha na extração do texto."
            self.pontuacao_final = 0.0
            self.opiniao_gerada = "Nenhuma opinião disponível devido à falha na extração do texto."
            self.is_loading = False
            return


        LLM = LangChainService(config_langchain=LangChainConfig())

        self.resumo_cv = LLM.resume_cv(self.curriculo_texto) #type: ignore

        self.pontuacao_final = LLM.generate_score(self.resumo_cv, self.vaga_atual) #type: ignore

        self.opiniao_gerada = LLM.generate_opinion(self.resumo_cv, self.vaga_atual) #type: ignore
        
        self.is_loading = False

    async def set_vaga_pelo_titulo(self, titulo_selecionado: str):
        estado_vaga = await self.get_state(ListJobsState)

        vaga_encontrada = next((vaga for vaga in estado_vaga.vagas if vaga.title == titulo_selecionado), None)

        if vaga_encontrada:
            self.vaga_atual = vaga_encontrada