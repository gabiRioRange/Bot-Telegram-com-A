# Importa o bot configurado
from src.config import bot, log
# Importa os handlers para registrá-los no bot
import src.handlers 

if __name__ == "__main__":
    print("""
    🤖 BOT INICIADO (Modo Modular)
    ------------------------------
    A estrutura agora é profissional.
    Logs sendo salvos em bot.log
    """)
    bot.infinity_polling()