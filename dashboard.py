import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import plotly.graph_objects as go
import time

# Configuração da Página (Layout Wide ocupa a tela toda)
st.set_page_config(
    page_title="Bot Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS Customizado para deixar mais bonito
st.markdown("""
<style>
    .metric-card {
        background-color: #0E1117;
        border: 1px solid #30333F;
        border-radius: 10px;
        padding: 15px;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 Painel de Controle: Telegram Bot AI")

# Conexão Banco de Dados
@st.cache_resource
def get_connection():
    return create_engine('sqlite:///bot_database.db')

engine = get_connection()

# Função de Carregamento com tratamento de datas
def load_data():
    try:
        users = pd.read_sql("SELECT * FROM users", engine)
        logs = pd.read_sql("SELECT * FROM logs", engine)
        
        # Converte coluna de texto para Data
        if not logs.empty:
            logs['timestamp'] = pd.to_datetime(logs['timestamp'])
            
        return users, logs
    except Exception as e:
        st.error(f"Erro ao ler banco de dados: {e}")
        return pd.DataFrame(), pd.DataFrame()

# Sidebar (Barra Lateral)
st.sidebar.header("⚙️ Filtros e Opções")
if st.sidebar.button('🔄 Atualizar Dados Agora'):
    st.rerun()

users_df, logs_df = load_data()

if not users_df.empty and not logs_df.empty:
    
    # --- BLOCO 1: KPIs (Indicadores Chave) ---
    col1, col2, col3, col4 = st.columns(4)
    
    total_msgs = len(logs_df)
    total_users = len(users_df)
    msgs_hoje = len(logs_df[logs_df['timestamp'].dt.date == pd.Timestamp.now().date()])
    active_today = logs_df[logs_df['timestamp'].dt.date == pd.Timestamp.now().date()]['user_id'].nunique()

    col1.metric("Total de Usuários", total_users, delta=f"+{active_today} hoje")
    col2.metric("Total Mensagens", total_msgs)
    col3.metric("Mensagens Hoje", msgs_hoje)
    col4.metric("Comando Mais Usado", logs_df['command'].mode()[0])

    st.markdown("---")

    # --- BLOCO 2: Gráficos Interativos ---
    c1, c2 = st.columns([2, 1]) # Coluna da esquerda maior que a direita

    with c1:
        st.subheader("📈 Atividade ao Longo do Tempo")
        # Agrupa por hora
        logs_df['hour'] = logs_df['timestamp'].dt.floor('H')
        activity_over_time = logs_df.groupby('hour').size().reset_index(name='counts')
        
        fig_line = px.line(activity_over_time, x='hour', y='counts', 
                           title='Fluxo de Mensagens (Hora a Hora)',
                           markers=True, template="plotly_dark")
        st.plotly_chart(fig_line, use_container_width=True)

    with c2:
        st.subheader("🍕 Distribuição de Comandos")
        # Filtra comandos para não poluir o gráfico com 'text'
        command_counts = logs_df['command'].value_counts().reset_index()
        command_counts.columns = ['Comando', 'Uso']
        
        fig_pie = px.pie(command_counts, values='Uso', names='Comando', 
                         title='Tipos de Interação',hole=0.4, template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- BLOCO 3: Detalhamento de Logs ---
    st.markdown("---")
    st.subheader("📝 Histórico Recente de Mensagens")
    
    # Filtro de Usuário na Tabela
    user_filter = st.multiselect("Filtrar por Usuário (ID)", logs_df['user_id'].unique())
    
    if user_filter:
        display_df = logs_df[logs_df['user_id'].isin(user_filter)]
    else:
        display_df = logs_df

    # Mostra os últimos 50 logs formatados
    st.dataframe(
        display_df[['timestamp', 'user_id', 'command', 'text']].sort_values(by='timestamp', ascending=False).head(50),
        use_container_width=True,
        hide_index=True
    )

else:
    st.warning("📭 Nenhum dado encontrado ainda. Inicie o bot e mande um '/start'!")

# Rodapé
st.sidebar.markdown("---")
st.sidebar.info(f"Bot Status: **Ativo** 🟢")
st.sidebar.text("v2.1 - Gabriel Dashboard")