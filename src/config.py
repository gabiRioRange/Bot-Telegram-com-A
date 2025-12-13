import os
import logging
import telebot
from dotenv import load_dotenv
from rich.logging import RichHandler

# Carrega variáveis
load_dotenv()

# Configuração de Logs
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True), logging.FileHandler("bot.log", encoding='utf-8')]
)
log = logging.getLogger("rich")

# Validação das Chaves
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not TELEGRAM_TOKEN or not GOOGLE_API_KEY:
    log.critical("❌ ERRO: Chaves não encontradas no .env")
    exit()

# Instância do Bot (exportada para outros arquivos usarem)
bot = telebot.TeleBot(TELEGRAM_TOKEN)