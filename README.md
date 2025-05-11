# Smart RH 💼

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39.0-FF4B4B.svg)](https://streamlit.io/)
[![Firebase](https://img.shields.io/badge/Firebase-Admin-yellow.svg)](https://firebase.google.com/)

Sistema inteligente de recrutamento que conecta candidatos às melhores oportunidades utilizando processamento de linguagem natural para analisar currículos e vagas. Clique [aqui]("https://smart-rh.streamlit.app/") para acessar a aplicação web!

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

Smart RH é uma aplicação web desenvolvida com Streamlit que auxilia profissionais de recrutamento e seleção a analisar currículos de forma inteligente, comparando-os com os requisitos das vagas cadastradas. O sistema utiliza o modelo Llama-3.3-70b para extrair informações relevantes dos currículos e calcular um score de compatibilidade com as vagas disponíveis.

## 🚀 Funcionalidades

- **🧠 Análise de Currículos com IA**: Upload e análise automática de currículos com algoritmos avançados de processamento de linguagem natural
- **📊 Compatibilidade Inteligente**: Score de 0-10 entre currículos e vagas cadastradas
- **📝 Cadastro Detalhado de Vagas**: Interface intuitiva para recrutar com informações completas sobre requisitos
- **📋 Gestão de Oportunidades**: Visualização organizada de todas as vagas disponíveis
- **📄 Extração Automática de Dados**: Identificação de habilidades, formação acadêmica, experiências e idiomas
- **💡 Insights Personalizados**: Recomendações para candidatos com base na análise do perfil

## 💻 Tecnologias

<p align="center">
  <img src="https://img.shields.io/badge/Backend-Python%20|%20Streamlit-blue" alt="Backend"/>
  <img src="https://img.shields.io/badge/IA-LangChain%20|%20Llama--3.3--70b-green" alt="IA"/>
  <img src="https://img.shields.io/badge/Database-Firebase%20Realtime%20DB-yellow" alt="Database"/>
</p>

- **Frontend**: [Streamlit](https://streamlit.io/) - Framework Python para criação de aplicações web de dados
- **Backend**: Python 3.9+ - Linguagem principal para lógica de negócio e processamento
- **Banco de Dados**: [Firebase Realtime Database](https://firebase.google.com/) - Armazenamento em tempo real na nuvem
- **NLP**: [LangChain](https://python.langchain.com/) com [Groq](https://groq.com/) - Framework para aplicações baseadas em LLMs
- **Modelo de IA**: Llama-3.3-70b - Modelo de linguagem de ponta
- **Parser de Documentos**: PyMuPDF, python-docx - Extração de texto de PDFs e DOCXs


## 🏗️ Arquitetura

O projeto segue uma arquitetura MVC (Model-View-Controller) adaptada para aplicações Streamlit:

```
smart_rh/
├── app.py                  # Ponto de entrada da aplicação
├── config/                 # Configurações (Firebase, LangChain)
│   ├── __init__.py
│   ├── firebase_config.py  # Configuração do Firebase
│   └── langchain_config.py # Configuração do LangChain
├── controllers/            # Controladores da aplicação
│   ├── __init__.py
│   ├── job_controller.py   # Controlador de vagas
│   └── resume_controller.py # Controlador de currículos
├── models/                 # Modelos de dados (Pydantic)
│   ├── __init__.py
│   ├── analysis.py         # Modelo de análise
│   ├── job.py              # Modelo de vaga
│   └── resume.py           # Modelo de currículo
├── services/               # Serviços de negócio
│   ├── __init__.py
│   ├── analysis_extractor.py # Extração de dados de currículos
│   ├── firebase_service.py   # Serviço Firebase (DB e Storage)
│   └── langchain_service.py  # Serviço de IA
└── views/                  # Interfaces Streamlit
    ├── __init__.py
    ├── analysis_ia_page.py   # Página de análise IA
    ├── show_job_form.py      # Formulário de vagas
    ├── show_job_upload_file.py # Upload de currículos
    └── show_jobs_page.py     # Página de visualização de vagas
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
4. Crie um arquivo `.streamlit/secrets.toml` com as seguintes configurações:

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
   cd smart_rh
   streamlit run app.py
   ```

2. Acesse a aplicação em seu navegador em `http://localhost:8501`

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