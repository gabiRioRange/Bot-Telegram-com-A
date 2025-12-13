# 🤖 Bot Supremo: Telegram + Gemini 1.5 + RAG (LanceDB)

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![LanceDB](https://img.shields.io/badge/VectorDB-LanceDB-F7931A?style=for-the-badge&logo=database&logoColor=white)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Gemini](https://img.shields.io/badge/AI-Gemini_1.5_Flash-8E75B2?style=for-the-badge&logo=google&logoColor=white)

Um assistente virtual de **nível empresarial** para Telegram. Este projeto utiliza uma **arquitetura modular** para integrar Visão Computacional, Análise de Documentos (RAG) e finanças, com um dashboard de monitoramento em tempo real.

---

## ✨ Funcionalidades Avançadas

### 🧠 1. Inteligência Multimodal (Gemini 1.5)
- **Texto:** Conversa natural e inteligente.
- **Visão:** Envie **fotos** e o bot descreverá ou analisará o conteúdo.
- **Audição:** Envie **áudios** e o bot transcreverá ou responderá falado.
- **Resiliência:** Sistema de *Auto-Retry* (espera automática) caso a API do Google atinja o limite de cota (Erro 429).

### 📚 2. RAG (Retrieval-Augmented Generation)
- **Chat com PDF:** Envie qualquer arquivo PDF. O bot indexa o conteúdo no **LanceDB** (banco vetorial local) e permite que você faça perguntas específicas sobre o documento.
- **Memória Persistente:** Os vetores são salvos em disco, não se perdem ao reiniciar.

### 📊 3. Dashboard Analytics
- Interface gráfica rodando em **Streamlit**.
- Monitore logs, usuários ativos e erros em tempo real via navegador.

### 💰 4. Utilitários
- **/dolar:** Cotação em tempo real via API externa.
- **Filtro Inteligente:** Distingue saudações ("Oi") de perguntas técnicas, evitando leituras desnecessárias do banco de dados.

---

## 🚀 Como Rodar (Recomendado: Docker Compose 🐳)

A forma mais fácil de subir o **Bot** e o **Dashboard** juntos.

1. **Clone o repositório:**
   bash

         git clone [https://github.com/gabiRioRange/bot-telegram-gemini.git](https://github.com/gabiRioRange/bot-telegram-gemini.git)
         cd bot-telegram-gemini

2.   Crie o arquivo de senhas (.env): Crie um arquivo chamado .env na raiz e coloque suas chaves:
Ini, TOML

         TELEGRAM_TOKEN=seu_token_do_botfather
         GOOGLE_API_KEY=sua_chave_do_google_ai_studio

Suba os serviços:
Bash

    docker-compose up --build

   O que vai acontecer?

   O Bot iniciará no terminal.

   O Dashboard ficará acessível em: http://localhost:8501

## 💻 Como Rodar (Modo Manual / Desenvolvimento)

Se preferir rodar sem Docker no seu Python local (Requer Python 3.12+):

   Crie o ambiente virtual:
    Bash

      python -m venv .venv
# Windows:
      .\.venv\Scripts\Activate
# Linux/Mac:
      source .venv/bin/activate

Instale as dependências:
Bash

      pip install -r requirements.txt

Execute:
Bash

   # Terminal 1 (Bot):
    python run.py

   # Terminal 2 (Dashboard):
    streamlit run dashboard.py

## 📂 Estrutura Profissional

O projeto segue o padrão MVC (Model-View-Controller) adaptado:
Plaintext

      bot-telegram-gemini/
      │
      ├── src/                    # 🧠 Código Fonte Modular
      │   ├── config.py           # Configurações globais
      │   ├── database.py         # Logs e usuários (SQLite)
      │   ├── handlers.py         # Comandos do Telegram (A "View")
      │   ├── memory.py           # Gerenciamento do LanceDB (RAG)
      │   └── services.py         # Lógica de IA, Visão e APIs
      │
      ├── data/                   # 💾 Persistência do LanceDB (ignorado no git)
      ├── bot_database.db         # Banco SQL de Logs
      ├── dashboard.py            # Painel Streamlit
      ├── docker-compose.yml      # Orquestrador dos containers
      ├── Dockerfile              # Receita da imagem
      ├── requirements.txt        # Dependências
      ├── run.py                  # Ponto de entrada
      └── README.md               # Documentação

## 📝 Licença

Desenvolvido por Gabriel de Souza Vieira. Projeto de portfólio demonstrando uso de GenAI, Engenharia de Dados (Vetorial) e DevOps.
