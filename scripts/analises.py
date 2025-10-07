
import pandas as pd
from scripts.leitura_dados import carregar_dados
from scripts.tratamentos_dados import ajustar_data_operacional, drop_date, status_picking


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

df_status = df.groupby("Num. Picking")["Situação"].apply(status_picking).reset_index()
status_counts = df_status['Situação'].value_counts()
caixas_pendentes = status_counts.get('P', 0)
pendentes_inducao = status_counts.get('I', 0)
