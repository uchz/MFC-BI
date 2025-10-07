# main.py
import pandas as pd
from sqlalchemy import create_engine
from scripts.leitura_dados import carregar_dados
from scripts.tratamentos_dados import ajustar_data_operacional, drop_date, status_picking

# --- 1. Carregar e tratar dados ---
df = carregar_dados()
df = ajustar_data_operacional(df, 'Data Início')
df = drop_date(df)

# ---------- Verificar total de apanhas -------------------#
df_apanhas = df.drop_duplicates(subset=['Cod. SKU', 'Num. Pedido'])

# --- Cálculos principais ---
total_apanhas = df_apanhas['Situação'].count()
apanhas_realizadas = df_apanhas['Situação'].value_counts().get('F', 0)
apanhas_pendentes = total_apanhas - apanhas_realizadas
total_caixas = df['Num. Picking'].nunique()

# ------------------- VERIFICAR TOTAL DE CAIXAS -------------------- #
df_status = df.groupby("Num. Picking")["Situação"].apply(status_picking).reset_index()
status_counts = df_status['Situação'].value_counts().reset_index()
status_counts.columns = ['Situação', 'Contagem']
caixas_pendentes = status_counts.get('P', 0)


# ---------------- EFICIÊNCIA DA BALANÇA --------------- # 

eficiencia = df[(df['Situação'] == 'F') & (df['Situação Conferência'] == 'F')]
eficiencia = eficiencia.drop_duplicates(subset='Num. Picking')

balanca = eficiencia[eficiencia['Usuário Conferência'] == 'CHECK_WEIGHT']
reconf = eficiencia[eficiencia['Usuário Conferência'] != 'CHECK_WEIGHT']


total_bal = balanca['Usuário Conferência'].count()
total_reconf = reconf['Usuário Conferência'].count()




# --- 1.1 Garantir UTF-8 nas colunas de texto ---
def fix_utf8(obj):
    if isinstance(obj, pd.DataFrame):
        for col in obj.select_dtypes(include=['object']).columns:
            obj.loc[:, col] = obj[col].astype(str).apply(lambda x: x.encode('utf-8', errors='ignore').decode('utf-8'))
        return obj
    elif isinstance(obj, pd.Series):
        return obj.astype(str).apply(lambda x: x.encode('utf-8', errors='ignore').decode('utf-8'))
    else:
        # Se for outro tipo, retorna sem alterações
        return obj

df_apanhas = fix_utf8(df_apanhas)
df_status = fix_utf8(df_status)
status_counts = fix_utf8(status_counts)


# --- 2. Conectar no banco ---
engine = create_engine(
    "postgresql+psycopg2://postgres:134769@localhost:5432/mfc_logistica",
    connect_args={"client_encoding": "utf8"}
)

# --- 3. Enviar para o banco ---
df_status.to_sql('status_picking', engine, if_exists='replace', index=False)
df_apanhas.to_sql('apanhas', engine, if_exists='replace', index=False)
status_counts.to_sql('status_count', engine, if_exists='replace', index=False)


df_lido = pd.read_sql("SELECT * FROM status_count", engine)
print(df_lido.head())



print("Dados enviados com sucesso!")
