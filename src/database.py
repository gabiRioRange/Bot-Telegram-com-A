from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from src.config import log

Base = declarative_base()

# --- Modelos (Tabelas) ---
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(String, unique=True)
    username = Column(String)
    first_seen = Column(DateTime, default=datetime.now)
    is_vip = Column(Integer, default=0)

class MessageLog(Base):
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    command = Column(String)
    text = Column(Text)
    timestamp = Column(DateTime, default=datetime.now)

# --- Configuração ---
# check_same_thread=False é necessário apenas para SQLite
engine = create_engine('sqlite:///bot_database.db', connect_args={'check_same_thread': False})
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# --- Funções Úteis ---
def registrar_usuario(user_id, username):
    try:
        user = session.query(User).filter_by(telegram_id=str(user_id)).first()
        if not user:
            new_user = User(telegram_id=str(user_id), username=username)
            session.add(new_user)
            session.commit()
            log.info(f"🆕 Novo usuário: {username}")
    except Exception as e:
        log.error(f"Erro Banco (Registro): {e}")

def log_msg(user_id, text, command="text"):
    try:
        new_log = MessageLog(user_id=str(user_id), command=command, text=text or "[Mídia]")
        session.add(new_log)
        session.commit()
    except Exception as e:
        log.error(f"Erro Banco (Log): {e}")