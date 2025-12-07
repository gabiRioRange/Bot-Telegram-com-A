import os
import logging
import telebot
import requests
import google.generativeai as genai
from dotenv import load_dotenv
from rich.logging import RichHandler
from rich.console import Console

# --- 1. Configurações e Variáveis ---
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[
        RichHandler(rich_tracebacks=True), 
        logging.FileHandler("bot_gemini.log", encoding='utf-8')
    ]
)

log = logging.getLogger("rich")

# Inicialização
try:
    if not TELEGRAM_TOKEN or not GOOGLE_API_KEY:
        log.critical("[bold red]ERRO: Chaves não encontradas no .env[/]", extra={"markup": True})
        exit()

    bot = telebot.TeleBot(TELEGRAM_TOKEN)
    genai.configure(api_key=GOOGLE_API_KEY)
    
    # ✅ MODELO CORRETO (Confirmado na sua lista)
    NOME_MODELO = 'gemini-flash-latest' 
    
    model = genai.GenerativeModel(NOME_MODELO)
    
    log.info(f"[bold green]🤖 Bot iniciado com modelo: {NOME_MODELO}[/]", extra={"markup": True})
except Exception as e:
    log.critical(f"Erro crítico na inicialização: {e}")
    exit()

# --- 2. Funções de Lógica ---

def filtro_seguranca(texto):
    """Filtra palavras proibidas."""
    if not texto: return False
    termos_proibidos = ["golpe", "crime", "violência explícita", "hackear"]
    if any(termo in texto.lower() for termo in termos_proibidos):
        return False
    return True

def consultar_multicocoes():
    """Busca Dólar, Euro e Bitcoin de uma vez."""
    try:
        url = "https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL"
        response = requests.get(url, timeout=5)
        data = response.json()
        
        dolar = data['USDBRL']
        euro = data['EURBRL']
        btc = data['BTCBRL']

        texto = (
            "📊 *Painel Financeiro*\n\n"
            f"🇺🇸 *Dólar:* R$ {dolar['bid'][:4]}\n"
            f"🇪🇺 *Euro:* R$ {euro['bid'][:4]}\n"
            f"🪙 *Bitcoin:* R$ {btc['bid']}\n\n"
            f"_Atualizado em: {dolar['create_date']}_"
        )
        return texto
    except Exception as e:
        log.error(f"Erro Cotação: {e}")
        return "⚠️ Erro ao buscar dados financeiros."

def consultar_github(user):
    try:
        url = f"https://api.github.com/users/{user}"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            bio = data.get('bio') if data.get('bio') else "Sem bio"
            return (f"🐙 *Perfil GitHub: {data.get('login')}*\n"
                    f"📝 Bio: {bio}\n"
                    f"📂 Repos: {data.get('public_repos')}\n"
                    f"👥 Seguidores: {data.get('followers')}\n"
                    f"🔗 [Ver Perfil]({data.get('html_url')})")
        return "❌ Usuário não encontrado."
    except Exception as e:
        log.error(f"Erro GitHub: {e}")
        return "Erro ao consultar GitHub."

def get_gemini_response(prompt_usuario, sistema="Seja útil e breve."):
    try:
        response = model.generate_content(f"{sistema}\nUser: {prompt_usuario}")
        return response.text
    except Exception as e:
        log.error(f"Erro Gemini ({NOME_MODELO}): {e}")
        return "A IA está indisponível no momento (Verifique o log)."

# --- 3. Comandos Automáticos ---

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    menu = (
        "🤖 *Bot do Gabriel*\n\n"
        "💸 *Finanças:*\n"
        "/cotacao → Ver Dólar, Euro e Bitcoin\n"
        "/cripto → Entender Criptomoedas\n\n"
        "🛠 *Ferramentas:*\n"
        "/github → Meu Perfil (Gabriel)\n"
        "/github [user] → Buscar outro dev\n"
        "/piada → Pedir piada pra IA\n\n"
        "💬 *Fale com a IA:* Digite qualquer coisa!"
    )
    bot.reply_to(message, menu, parse_mode="Markdown")

@bot.message_handler(commands=['cotacao'])
def command_cotacao(message):
    bot.send_chat_action(message.chat.id, 'typing')
    bot.reply_to(message, consultar_multicocoes(), parse_mode="Markdown")

@bot.message_handler(commands=['cripto'])
def command_cripto(message):
    bot.send_chat_action(message.chat.id, 'typing')
    prompt = "Explique o que são criptomoedas e blockchain de forma simples, resumida e didática para um iniciante."
    explicacao = get_gemini_response(prompt, sistema="Você é um professor de finanças experiente.")
    bot.reply_to(message, f"🎓 *Aula Relâmpago:*\n\n{explicacao}", parse_mode="Markdown")

@bot.message_handler(commands=['github'])
def command_github(message):
    try:
        args = message.text.split(maxsplit=1)
        if len(args) > 1:
            user = args[1]
            log.info(f"🔍 Consultando GitHub de: {user}")
        else:
            user = "gabiRioRange"
            log.info(f"🔍 Consultando GitHub do Criador: {user}")
            
        bot.reply_to(message, consultar_github(user), parse_mode="Markdown")
        
    except Exception as e:
        bot.reply_to(message, "Erro ao processar comando.")

@bot.message_handler(commands=['piada'])
def command_piada(message):
    bot.send_chat_action(message.chat.id, 'typing')
    piada = get_gemini_response("Conte uma piada curta de programador.")
    bot.reply_to(message, f"🤡 {piada}")

# --- 4. Camada de Inteligência ---

@bot.message_handler(func=lambda message: True)
def responder_ia(message):
    user_msg = message.text
    # Pega nome ou primeiro nome se não tiver username
    user_name = message.from_user.username or message.from_user.first_name

    if not filtro_seguranca(user_msg):
        log.warning(f"🚫 Bloqueio: {user_name}")
        bot.reply_to(message, "⚠️ Mensagem bloqueada.")
        return

    log.info(f"💬 {user_name}: {user_msg}")
    bot.send_chat_action(message.chat.id, 'typing')

    resposta = get_gemini_response(user_msg)
    
    try:
        bot.reply_to(message, resposta, parse_mode="Markdown")
    except Exception:
        bot.reply_to(message, resposta)

if __name__ == "__main__":
    bot.infinity_polling()