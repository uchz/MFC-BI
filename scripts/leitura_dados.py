import pandas as pd
from glob import glob

import pandas as pd
from glob import glob

def carregar_dados(caminho="MFC/pedidos/geral_pedidos.csv"):
    arquivos = glob(caminho)
    df = pd.concat(
        [pd.read_csv(a, sep=";", on_bad_lines="skip", engine="python") for a in arquivos],
        ignore_index=True
    )
    return df


def carregar_order(caminho="MFC/pedidos/*.csv"):
    arquivos = glob(caminho)
    df = pd.concat(
        [pd.read_csv(a, sep=";", on_bad_lines="skip", engine="python") for a in arquivos],
        ignore_index=True
    )
    return df