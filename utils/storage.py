import os
import pandas as pd

def salvar_dados(dados):
    os.makedirs("model", exist_ok=True)
    path = "model/dataset.csv"

    df_novo = pd.DataFrame(dados)

    if os.path.exists(path):
        df_antigo = pd.read_csv(path)
        df_total = pd.concat([df_antigo, df_novo], ignore_index=True)
    else:
        df_total = df_novo

    df_total.to_csv(path, index=False)
