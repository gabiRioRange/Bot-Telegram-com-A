import google.generativeai as genai
import time
import io
import requests # <--- Importante para o dólar
from pypdf import PdfReader
from src.config import GOOGLE_API_KEY, log
from src.memory import salvar_memoria_lancedb 

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

def processar_imagem(file_bytes, caption):
    """Prepara a imagem para o Gemini analisar"""
    try:
        # O Gemini precisa saber o tipo do arquivo.
        # Fotos do Telegram geralmente são JPEG.
        image_data = {
            'mime_type': 'image/jpeg',
            'data': file_bytes
        }
        
        # Se o usuário não escreveu legenda, usamos um prompt padrão
        prompt = caption if caption else "Descreva detalhadamente o que você vê nesta imagem."

        # Reusa a nossa função principal (que já tem retry automático!)
        return get_gemini_response(prompt, imagem_ou_audio=image_data)
    except Exception as e:
        log.error(f"Erro Imagem: {e}")
        return f"Erro ao processar a imagem: {e}"

def obter_cotacao_dolar():
    """Busca dólar na API AwesomeAPI"""
    try:
        url = "https://economia.awesomeapi.com.br/last/USD-BRL"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            dados = response.json()['USDBRL']
            valor = float(dados['bid'])
            data = dados['create_date']
            return f"💵 **Dólar Comercial**\n💰 R$ {valor:.2f}\n📅 {data}"
        return "❌ API de cotação indisponível."
    except Exception as e:
        log.error(f"Erro Cotação: {e}")
        return "⚠️ Erro de conexão."

def get_gemini_response(prompt, context=None, imagem_ou_audio=None):
    max_retries = 3
    attempt = 0
    while attempt < max_retries:
        try:
            prompt_final = prompt
            if context:
                prompt_final = (
                    f"Use APENAS o contexto abaixo para responder.\n"
                    f"--- CONTEXTO ---\n{context}\n------\n"
                    f"Pergunta: {prompt}"
                )
            
            if imagem_ou_audio:
                response = model.generate_content([prompt_final, imagem_ou_audio])
            else:
                response = model.generate_content(prompt_final)
            return response.text

        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "quota" in error_msg.lower():
                wait_time = 60 
                log.warning(f"⏳ Cota atingida. Esperando {wait_time}s...")
                time.sleep(wait_time)
                attempt += 1
            else:
                log.error(f"Erro Gemini: {e}")
                return "Erro técnico na IA."
    return "Servidor ocupado. Tente em 1 minuto."

def processar_pdf(file_bytes, user_id):
    try:
        pdf_file = io.BytesIO(file_bytes)
        reader = PdfReader(pdf_file)
        text = ""
        for i, page in enumerate(reader.pages):
            if i >= 30: break 
            text += page.extract_text() + "\n"
        if len(text) < 50: return None, "PDF vazio."
        salvar_memoria_lancedb(user_id, text)
        return "PDF indexado!", None
    except Exception as e:
        return None, str(e)

def processar_audio(file_path):
    try:
        audio_file = genai.upload_file(file_path)
        while audio_file.state.name == "PROCESSING":
            time.sleep(1)
            audio_file = genai.get_file(audio_file.name)
        return get_gemini_response("Responda/Transcreva.", imagem_ou_audio=audio_file)
    except:
        return "Erro audio."
    
    