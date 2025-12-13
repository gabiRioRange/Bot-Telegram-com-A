import os
import telebot
from src.config import bot, log
from src.database import registrar_usuario, log_msg
from src.services import get_gemini_response, processar_pdf, processar_audio, obter_cotacao_dolar
from src.memory import buscar_memoria_lancedb
from src.services import get_gemini_response, processar_pdf, processar_audio, obter_cotacao_dolar, processar_imagem

def enviar_seguro(chat_id, texto, reply_to=None):
    try:
        bot.send_message(chat_id, texto, reply_to_message_id=reply_to, parse_mode="Markdown")
    except:
        bot.send_message(chat_id, texto, reply_to_message_id=reply_to)

# --- COMANDOS ESPECIAIS (Vêm Primeiro!) ---
@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    registrar_usuario(message.from_user.id, message.from_user.username)
    enviar_seguro(message.chat.id, "🤖 **Bot Atualizado!**\n\n- Diga 'Oi' para testar\n- Use /dolar para cotação\n- Envie PDF para estudar")

@bot.message_handler(commands=['dolar', 'cotacao'])
def handler_cotacao(message):
    registrar_usuario(message.from_user.id, message.from_user.username)
    log_msg(message.from_user.id, "/dolar")
    msg = bot.reply_to(message, "🔍 Buscando valor...")
    valor = obter_cotacao_dolar()
    bot.edit_message_text(valor, message.chat.id, msg.message_id, parse_mode="Markdown")

# --- ARQUIVOS ---
@bot.message_handler(content_types=['document'])
def on_document(message):
    if message.document.mime_type == 'application/pdf':
        msg = bot.reply_to(message, "🧠 Lendo PDF...")
        file_info = bot.get_file(message.document.file_id)
        downloaded = bot.download_file(file_info.file_path)
        resumo, erro = processar_pdf(downloaded, message.from_user.id)
        if erro: bot.reply_to(message, f"Erro: {erro}")
        else: bot.edit_message_text(f"✅ Lido!\n{resumo}", message.chat.id, msg.message_id)

@bot.message_handler(content_types=['voice', 'audio'])
def on_audio_msg(message):
    msg = bot.reply_to(message, "🎧 Ouvindo...")
    file_id = message.voice.file_id if message.voice else message.audio.file_id
    file_info = bot.get_file(file_id)
    downloaded = bot.download_file(file_info.file_path)
    with open("temp.mp3", "wb") as f: f.write(downloaded)
    resp = processar_audio("temp.mp3")
    bot.edit_message_text(resp, message.chat.id, msg.message_id)
    if os.path.exists("temp.mp3"): os.remove("temp.mp3")

# --- HANDLER DE IMAGEM/FOTO ---
@bot.message_handler(content_types=['photo'])
def on_photo_msg(message):
    registrar_usuario(message.from_user.id, message.from_user.username)
    log_msg(message.from_user.id, "[Envia Imagem]", "photo")

    msg = bot.reply_to(message, "👀 Analisando imagem...")
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        # O Telegram manda várias versões da foto (pequena, média, grande).
        # Pegamos a última [-1], que é a maior resolução.
        photo_info = message.photo[-1]
        file_info = bot.get_file(photo_info.file_id)
        downloaded = bot.download_file(file_info.file_path)
        
        # Pega a legenda que o usuário escreveu (se houver)
        legenda = message.caption
        
        # Processa
        resp = processar_imagem(downloaded, legenda)
        
        # Responde
        enviar_seguro(message.chat.id, resp, reply_to=message.message_id)
        # Apaga a mensagem de "Analisando..."
        bot.delete_message(message.chat.id, msg.message_id)
        
    except Exception as e:
        bot.edit_message_text(f"Erro na imagem: {e}", message.chat.id, msg.message_id)

# --- CHAT GERAL INTELIGENTE (Vem por Último) ---
@bot.message_handler(func=lambda m: True)
def on_chat(message):
    user_id = message.from_user.id
    texto = message.text.strip() # Remove espaços extras
    registrar_usuario(user_id, message.from_user.username)
    
    # --- FILTRO ANTI-CHATICE ---
    # Se o usuário disser algo simples, o bot responde normal SEM ler PDF
    frases_simples = ['oi', 'ola', 'olá', 'chat', 'teste', 'tudo bem', 'bom dia', 'boa tarde', 'sai dessa', 'obrigado', 'valeu']
    
    # Verifica se alguma dessas palavras está na mensagem
    if any(palavra in texto.lower() for palavra in frases_simples):
        bot.reply_to(message, "Opa! 👋 Eu sou o Bot do Gabriel. \n\nAtualmente estou treinado para responder sobre o currículo dele, mas se quiser ver a cotação do dólar digite /dolar!")
        return
    # ---------------------------

    # Se passou do filtro, aí sim ele busca no RAG
    bot.send_chat_action(message.chat.id, 'typing')
    contexto = buscar_memoria_lancedb(user_id, texto)
    
    # Se não achou nada no PDF e a pergunta for curta, avisa
    if not contexto and len(texto) < 10:
        bot.reply_to(message, "Não encontrei nada sobre isso no documento. Tente ser mais específico.")
        return

    resp = get_gemini_response(texto, context=contexto)
    enviar_seguro(message.chat.id, resp)