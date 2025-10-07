#%%
import pandas as pd
from scripts.tratamentos_dados import ajustar_data_operacional, status_picking

# %%
df = pd.read_excel('Base PBI/Geral Pedidos MFC.xlsx')

# %%


#------------------- CÁLCULO DE APANHAS --------------------- #
df_apanhas = df.drop_duplicates(subset=['Cod. SKU', 'Num. Pedido'])

# --- Cálculos principais ---
total_apanhas = df_apanhas['Situação'].count()
apanhas_realizadas = df_apanhas['Situação'].value_counts().get('F', 0)
apanhas_pendentes = total_apanhas - apanhas_realizadas
total_caixas = df['Num. Picking'].nunique()

#%%
# --------------------- Apanhas p/ Posto -----------------------#

apanhas_posto = df_apanhas['Num. Posto'].value_counts().reset_index()
apanhas_posto.columns = ['Posto', 'Apanhas']


# %%
#-------------------- CÁLCULO VOLUMES ---------------------#
df_status = df.groupby("Num. Picking")["Situação"].apply(status_picking).reset_index()
status_counts = df_status['Situação'].value_counts().reset_index()
status_counts.columns = ['Situação', 'Contagem']
status_counts

#%%


# ---------------- EFICIÊNCIA DA BALANÇA --------------- # 

eficiencia = df[(df['Situação'] == 'F') & (df['Situação Conferência'] == 'F')]
eficiencia = eficiencia.drop_duplicates(subset='Num. Picking')

balanca = eficiencia[eficiencia['Usuário Conferência'] == 'CHECK_WEIGHT']
reconf = eficiencia[eficiencia['Usuário Conferência'] != 'CHECK_WEIGHT']

total_bal = balanca['Usuário Conferência'].count()
total_reconf = reconf['Usuário Conferência'].count()

total = total_bal + total_reconf

perc_bal = (total_bal / total) * 100
perc_reconf = (total_reconf / total) * 100

df_eficiencia = pd.DataFrame({
    'Métrica': ['Balança', 'Reconf.'],
    'Quantidade': [total_bal, total_reconf],
    'Percentual': [perc_bal, perc_reconf]
})

# %%


output_path = 'Base PBI/PBI/'

# Salvar cada análise separadamente
df_apanhas.to_excel(f'{output_path}apanhas.xlsx', index=False)
apanhas_posto.to_excel(f'{output_path}apanhas_por_posto.xlsx', index=False)
status_counts.to_excel(f'{output_path}status_counts.xlsx', index=False)
df_eficiencia.to_excel(f'{output_path}eficiencia_balanca.xlsx', index=False)
# %%
