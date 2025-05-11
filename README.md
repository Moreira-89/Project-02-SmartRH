# Smart RH 💼

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.39.0-FF4B4B.svg)](https://streamlit.io/)
[![Firebase](https://img.shields.io/badge/Firebase-Admin-yellow.svg)](https://firebase.google.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

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

Smart RH é uma aplicação web desenvolvida com Streamlit que auxilia profissionais de recrutamento e seleção a analisar currículos de forma inteligente, comparando-os com os requisitos das vagas cadastradas. O sistema utiliza processamento o modelo Llama-3.3-70b natural para extrair informações relevantes dos currículos e calcular um score de compatibilidade com as vagas disponíveis.

## 🚀 Funcionalidades

- **Cadastro de Vagas**: Interface intuitiva para adicionar novas oportunidades com descrição detalhada, requisitos e diferenciais.
- **Visualização de Vagas**: Listagem de todas as vagas cadastradas no sistema com detalhes expansíveis.
- **Análise de Currículos com IA**: Upload de currículos em formato PDF/DOCX e análise automática com algoritmos de processamento de linguagem natural.
- **Score de Compatibilidade**: Cálculo automático da pontuação de compatibilidade entre currículos e vagas (0-10).
- **Análise Detalhada**: Extração de informações como habilidades técnicas, formação acadêmica e idiomas.
- **Recomendações Personalizadas**: Sugestões de melhorias para os candidatos com base na análise do currículo.

## 💻 Tecnologias

- **Frontend**: Streamlit
- **Backend**: Python
- **Banco de Dados**: Firebase Realtime Database
- **Processamento de Linguagem Natural**: LangChain com Groq
- **Extração de Texto**: PyMuPDF

## 🏗️ Arquitetura

O projeto segue uma arquitetura MVC (Model-View-Controller) adaptada:

```
smart_rh/
├── app.py                  # Ponto de entrada da aplicação
├── config/                 # Configurações do Firebase e LangChain
├── controllers/            # Controladores da aplicação
├── models/                 # Modelos de dados (Pydantic)
├── services/               # Serviços de negócio e integração
└── views/                  # Interfaces visuais do Streamlit
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

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---
