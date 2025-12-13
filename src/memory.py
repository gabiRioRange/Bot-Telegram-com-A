import lancedb
import google.generativeai as genai
from src.config import log, GOOGLE_API_KEY

# --- 1. Configurações ---
genai.configure(api_key=GOOGLE_API_KEY)

# Conecta ao LanceDB (cria a pasta automaticamente)
db = lancedb.connect("data/lancedb-store")
TABLE_NAME = "pdf_memory"

# Modelo de Embedding do Google
EMBEDDING_MODEL = "models/text-embedding-004"

# --- 2. Funções Auxiliares ---

def get_google_embedding(text, task_type="retrieval_document"):
    """Gera o vetor usando a API do Google (Nuvem)"""
    try:
        result = genai.embed_content(
            model=EMBEDDING_MODEL,
            content=text,
            task_type=task_type
        )
        return result['embedding']
    except Exception as e:
        log.error(f"Erro Embedding Google: {e}")
        return None

def get_table():
    """Pega ou cria a tabela no LanceDB"""
    try:
        # Tenta abrir a tabela existente
        return db.open_table(TABLE_NAME)
    except:
        # Se não existir, retornamos None (será criada no primeiro salvamento)
        return None

# --- 3. Funções Principais ---

def salvar_memoria_lancedb(user_id, text):
    try:
        # Quebra o texto em pedaços (Chunks) de 1000 caracteres
        chunk_size = 1000
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
        data_to_add = []
        
        # Gera vetores para cada pedaço
        for chunk in chunks:
            vector = get_google_embedding(chunk, "retrieval_document")
            if not vector: continue
            
            # Formato dos dados para o LanceDB
            data_to_add.append({
                "vector": vector,
                "text": chunk,
                "user_id": str(user_id)
            })

        if not data_to_add:
            return False

        # Salva no LanceDB
        tbl = get_table()
        if tbl:
            tbl.add(data_to_add)
        else:
            # Cria a tabela na primeira vez (o LanceDB infere o esquema sozinho!)
            db.create_table(TABLE_NAME, data=data_to_add)
            
        log.info(f"💾 {len(data_to_add)} chunks salvos no LanceDB para user {user_id}")
        return True
    except Exception as e:
        log.error(f"Erro LanceDB Add: {e}")
        return False

def buscar_memoria_lancedb(user_id, query):
    try:
        tbl = get_table()
        if not tbl: return None # Se não tem tabela, não tem memória

        # 1. Vetoriza a pergunta
        query_vector = get_google_embedding(query, "retrieval_query")
        if not query_vector: return None

        # 2. Busca no LanceDB (Busca Vetorial + Filtro SQL na mesma linha!)
        results = tbl.search(query_vector) \
            .where(f"user_id = '{user_id}'") \
            .limit(3) \
            .to_list()
        
        # 3. Formata o contexto
        if results:
            contexto = "\n\n".join([r["text"] for r in results])
            return contexto
        return None
    except Exception as e:
        log.error(f"Erro LanceDB Search: {e}")
        return None