# 🤖 Bot Híbrido: Telegram + Google Gemini AI

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![Telegram API](https://img.shields.io/badge/Telegram_Bot-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![Google Gemini](https://img.shields.io/badge/AI-Google_Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white)

Um assistente virtual robusto para Telegram. Este projeto utiliza uma **arquitetura híbrida** que une automação de tarefas (finanças, github) com a inteligência artificial do **Google Gemini (Flash Latest)**.

Agora com suporte nativo a **Docker** para deploy fácil em qualquer ambiente.

---

## ✨ Funcionalidades

### 🧠 Inteligência Artificial
- **Conversa Natural:** Responde a qualquer pergunta usando o modelo `gemini-flash-latest`.
- **Modo Professor:** Comando `/cripto` aciona uma aula didática sobre Blockchain.
- **Segurança:** Filtros ativos contra linguagem tóxica e spam.

### 💰 Ferramentas Financeiras
- **/cotacao:** Painel em tempo real com **Dólar (USD)**, **Euro (EUR)** e **Bitcoin (BTC)**.

### 🛠️ Utilitários
- **/github:** Exibe automaticamente o perfil do criador (`gabiRioRange`).
- **/github [usuario]:** Busca dados públicos de qualquer conta do GitHub.
- **/piada:** Gera piadas tech com IA.

### 🎨 Monitoramento
- **Logs Coloridos:** Interface de terminal moderna usando a lib `Rich`.
- **Histórico:** Salva logs de execução em `bot_gemini.log`.

---

## 🚀 Como Rodar (Opção 1: Docker 🐳)
*Recomendado para manter o ambiente limpo.*

1. **Construa a imagem:**
   ```bash
   docker build -t bot-gemini .
   Execute o container: (Certifique-se de ter o arquivo .env criado na pasta)
Bash

      docker run --env-file .env --name meu-bot bot-gemini

Parar o bot:
Bash

    docker stop meu-bot

💻 Como Rodar (Opção 2: Manual)
Pré-requisitos

    Python 3.10+

    Conta no Telegram e chave do Google AI Studio.

Instalação

    Clone o repositório
    Bash

      git clone [https://github.com/gabiRioRange/bot-telegram-gemini.git](https://github.com/gabiRioRange/bot-telegram-gemini.git)
      cd bot-telegram-gemini

Configure o ambiente
Bash

# Linux/Mac
      python3 -m venv venv
      source venv/bin/activate

# Windows
      python -m venv venv
      venv\Scripts\activate

Instale as dependências
Bash

      pip install -r requirements.txt

<p>Configuração (.env) Crie um arquivo .env na raiz e preencha:
Ini, TOML</p>

      TELEGRAM_TOKEN=seu_token_aqui
   
      GOOGLE_API_KEY=sua_chave_aqui

Executar
Bash

    python bot.py

## 📂 Estrutura do Projeto
Plaintext

      bot-telegram-gemini/
      │
      ├── Dockerfile          # Configuração da imagem Docker
      ├── .dockerignore       # Arquivos ignorados pelo Docker
      ├── .env                # Chaves de API (NÃO COMITAR)
      ├── bot.py              # Código principal
      ├── requirements.txt    # Dependências
      └── README.md           # Documentação

## 📝 Licença

Desenvolvido por Gabriel para fins de estudo e portfólio.
