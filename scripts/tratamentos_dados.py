import pandas as pd

def ajustar_data_operacional(df, coluna_datahora):
    # Converte a coluna para datetime
    df[coluna_datahora] = pd.to_datetime(df[coluna_datahora], dayfirst=True)

    # Define os limites de horário
    hora_inicio = pd.to_datetime("19:00:00").time()
    hora_fim = pd.to_datetime("06:00:00").time()

    # Filtra apenas os horários entre 18:00 e 23:59 ou entre 00:00 e 06:00
    df_filtrado = df[
        (df[coluna_datahora].dt.time >= hora_inicio) | 
        (df[coluna_datahora].dt.time <= hora_fim)
    ].copy()

    # Cria nova coluna com data ajustada
    df_filtrado['Data Operacional'] = df_filtrado[coluna_datahora].apply(
        lambda x: x.date() if x.time() >= hora_inicio else (x - pd.Timedelta(days=1)).date()
    )

    return df_filtrado


def drop_date(df, coluna="Data Operacional"):
    """
    Remove a primeira (mais antiga) data operacional do DataFrame.
    
    Parâmetros:
        df (pd.DataFrame): DataFrame contendo a coluna de data operacional.
        coluna (str): Nome da coluna de data. Padrão = 'Data Operacional'.
    
    Retorna:
        pd.DataFrame: DataFrame sem a data operacional mais antiga.
    """
    drop = df[coluna].sort_values(ascending=True).unique()[0]
    df_filtrado = df[df[coluna] != drop]
    return df_filtrado



def status_picking(situacoes):
    if all(s == "F" for s in situacoes):
        return "F"
    elif all(s == "I" for s in situacoes):
        return "I"
    else:
        return "P"
    
