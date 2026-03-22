# SmartRH

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Reflex-0.8.28-111827?style=for-the-badge" alt="Reflex" />
  <img src="https://img.shields.io/badge/Firebase-Realtime%20DB-FFCA28?style=for-the-badge&logo=firebase&logoColor=black" alt="Firebase" />
  <img src="https://img.shields.io/badge/LangChain-Groq-0B3B2E?style=for-the-badge" alt="LangChain Groq" />
</p>

<p align="center">
  Plataforma de recrutamento inteligente com análise de currículos por IA, score de aderência e histórico de avaliações.
</p>

---

## Sumário

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Stack](#stack)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Instalação](#instalação)
- [Configuração de Ambiente](#configuração-de-ambiente)
- [Executando o Projeto](#executando-o-projeto)
- [Fluxo Recomendado](#fluxo-recomendado)
- [Observações](#observações)
- [Contribuição](#contribuição)

## Visão Geral

O SmartRH automatiza parte do processo de triagem de currículos com base nos requisitos de cada vaga.

Objetivos principais:
- centralizar vagas e critérios de seleção
- comparar currículos com vagas usando score de compatibilidade (0 a 10)
- gerar resumo estruturado e recomendações via LLM
- manter histórico consultável de análises

## Funcionalidades

### Cadastro de vagas
- título, atividades principais, pré-requisitos e diferenciais
- contagem automática de requisitos (`requirements_count`)

### Página de vagas (UX aprimorada)
- busca por termo (título, atividade ou requisito)
- filtro por status
- cards com preview de conteúdo
- modal com detalhes completos
- ação rápida: `Analisar CV desta vaga`

### Análise de currículo com IA
- upload de currículo em PDF
- seleção da vaga alvo
- score de compatibilidade
- resumo estruturado e recomendações
- opção de salvar ou limpar análise

### Histórico de análises
- listagem de análises anteriores
- modal com dados estruturados (educação, skills e idiomas)

### Front-end
- tema dark responsivo
- componentes construídos com `rx.*`

## Stack

- **Python**
- **Reflex** (`reflex~=0.8.28`)
- **Firebase Admin SDK** (Realtime Database + Storage)
- **LangChain + Groq** (`langchain-groq`)
- **PyPDF2 / pdfminer / python-docx**

## Estrutura do Projeto

```text
Project-02-SmartRH/
├── rxconfig.py
├── requirements.txt
├── README.md
└── Project_02_SmartRH/
    ├── Project_02_SmartRH.py          # Registro de rotas/páginas
    ├── components/
    │   └── layout.py                  # Layout base e navegação
    ├── config/
    │   ├── firebase_config.py
    │   └── langchain_config.py
    ├── models/
    │   ├── analysis.py
    │   ├── job.py
    │   └── resume.py
    ├── pages/
    │   ├── homepage.py
    │   ├── add_job.py
    │   ├── show_jobs_page.py
    │   ├── analisar_curriculo.py
    │   └── historico_page.py
    ├── services/
    │   ├── firebase_service.py
    │   ├── langchain_service.py
    │   └── analysis_extractor.py
    └── state/
        ├── job_state.py
        ├── listjob_state.py
        ├── analise_state.py
        └── historico_state.py
```

## Instalação

```bash
git clone <url-do-repositorio>
cd Project-02-SmartRH
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Configuração de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
FIREBASE_PROJECT_ID=seu-projeto-id
FIREBASE_DATABASE_URL=https://seu-projeto-default-rtdb.firebaseio.com
FIREBASE_STORAGE_BUCKET=seu-projeto.appspot.com
FIREBASE_CLIENT_EMAIL=firebase-adminsdk-xxxx@seu-projeto.iam.gserviceaccount.com
FIREBASE_DATABASE_SECRET="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"

LANGCHAIN_GROQ_API_KEY=sua-chave-groq
```

## Executando o Projeto

```bash
reflex run
```

Abra no navegador: `http://localhost:3000`

## Fluxo Recomendado

1. Cadastre uma vaga em `Adicionar Vaga`.
2. Localize a vaga em `Vagas` usando busca/filtro.
3. Clique em `Analisar CV desta vaga`.
4. Envie o PDF e rode a análise.
5. Salve o resultado no histórico.
6. Consulte os detalhes em `Histórico de Análises`.

## Observações

- Persistência em Firebase Realtime Database.
- Registros antigos podem não ter campos novos; existe fallback para `requirements_count` na listagem de vagas.

## Contribuição

1. Crie uma branch para sua alteração.
2. Faça commit das mudanças.
3. Abra um Pull Request.
