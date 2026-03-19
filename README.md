# Smart RH 💼

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Reflex](https://img.shields.io/badge/Reflex-Framework-black.svg)](https://reflex.dev/)
[![Firebase](https://img.shields.io/badge/Firebase-Admin-yellow.svg)](https://firebase.google.com/)

Sistema inteligente de recrutamento que conecta candidatos às melhores oportunidades utilizando processamento de linguagem natural para analisar currículos e vagas.

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Funcionalidades](#-funcionalidades)
- [Tecnologias](#-tecnologias)
- [Arquitetura](#-arquitetura)
- [Instalação](#-instalação)
- [Configuração](#-configuração)
- [Uso](#-uso)
- [Roadmap](#-roadmap)
- [Contribuição](#-contribuição)
- [Licença](#-licença)

## 🔍 Visão Geral

Smart RH é uma aplicação web desenvolvida com Reflex que auxilia profissionais de recrutamento e seleção a analisar currículos de forma inteligente, comparando-os com os requisitos das vagas cadastradas. O sistema utiliza o modelo Llama-3.3-70b para extrair informações relevantes dos currículos e calcular um score de compatibilidade com as vagas disponíveis.

## 🚀 Funcionalidades

- **🧠 Análise de Currículos com IA**: Upload e análise automática de currículos com algoritmos avançados de processamento de linguagem natural
- **📊 Compatibilidade Inteligente**: Score de 0-10 entre currículos e vagas cadastradas
- **📝 Cadastro Detalhado de Vagas**: Interface intuitiva para recrutar com informações completas sobre requisitos
- **📋 Gestão de Oportunidades**: Visualização organizada de todas as vagas disponíveis
- **📄 Extração Automática de Dados**: Identificação de habilidades, formação acadêmica, experiências e idiomas
- **💡 Insights Personalizados**: Recomendações para candidatos com base na análise do perfil

## 💻 Tecnologias

<p align="center">
  <img src="https://img.shields.io/badge/Backend-Python%20|%20Reflex-blue" alt="Backend"/>
  <img src="https://img.shields.io/badge/IA-LangChain%20|%20Llama--3.3--70b-green" alt="IA"/>
  <img src="https://img.shields.io/badge/Database-Firebase%20Realtime%20DB-yellow" alt="Database"/>
</p>

- **Frontend & Backend**: [Reflex](https://reflex.dev/) - Framework Python moderno para criação de aplicações web completas
- **Backend**: Python 3.9+ - Linguagem principal para lógica de negócio e processamento
- **Banco de Dados**: [Firebase Realtime Database](https://firebase.google.com/) - Armazenamento em tempo real na nuvem
- **NLP**: [LangChain](https://python.langchain.com/) com [Groq](https://groq.com/) - Framework para aplicações baseadas em LLMs
- **Modelo de IA**: Llama-3.3-70b - Modelo de linguagem de ponta
- **Parser de Documentos**: PyMuPDF, python-docx - Extração de texto de PDFs e DOCXs


## 🏗️ Arquitetura

O projeto foi refatorado para utilizar a arquitetura moderna baseada em **Componentes (Pages)** e **Estado (State)** adaptada para aplicações Reflex:

```text
Project-02-SmartRH/
├── rxconfig.py                      # Configurações gerais do app Reflex
└── Project_02_SmartRH/              # Diretório raiz do projeto principal
    ├── Project_02_SmartRH.py        # Ponto de entrada (Registro de Páginas/Rotas)
    ├── config/                      # Configurações e variáveis de ambiente
    │   ├── firebase_config.py
    │   └── langchain_config.py
    ├── models/                      # Estruturas de dados (Pydantic)
    │   ├── analysis.py
    │   ├── job.py
    │   └── resume.py
    ├── pages/                       # Componentes de UI e Telas
    │   ├── add_job.py
    │   ├── analisar_curriculo.py
    │   └── show_jobs_page.py
    ├── state/                       # Lógica de interface e estado global
    │   ├── analise_state.py
    │   └── listjob_state.py
    └── services/                    # Lógica de negócio, IA e integrações
        ├── analysis_extractor.py
        ├── firebase_service.py
        └── langchain_service.py
```

## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/smart-rh.git
   cd smart-rh
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## ⚙️ Configuração

1. Crie um projeto no [Firebase](https://console.firebase.google.com/)
2. Configure um Realtime Database e Storage
3. Gere uma chave privada para o SDK Admin
4. Crie um arquivo `.env` com as seguintes configurações:

```toml
[FIREBASE]
PROJECT_ID = "seu-projeto-id"
DATABASE_URL = "https://seu-projeto-id.firebaseio.com"
STORAGE_BUCKET = "seu-projeto-id.appspot.com"
CLIENT_EMAIL = "firebase-adminsdk-xxxx@seu-projeto-id.iam.gserviceaccount.com"
DATABASE_SECRET = "-----BEGIN PRIVATE KEY-----\nSua chave privada\n-----END PRIVATE KEY-----\n"

[LANGCHAIN_GROG]
API_KEY = "seu-api-key-groq"
```

## 🖥️ Uso

1. Inicie a aplicação:
   ```bash
   # Na pasta raiz onde está o rxconfig.py
   reflex run
   ```

2. Acesse a aplicação em seu navegador em `http://localhost:3000`

3. Fluxo básico:
   - Cadastre uma nova vaga em "Cadastrar Vaga"
   - Visualize as vagas em "Visualizar Vagas"
   - Faça upload de um currículo em "Análise com IA"
   - Receba a análise detalhada e o score de compatibilidade

## 👥 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas alterações (`git commit -am 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request
