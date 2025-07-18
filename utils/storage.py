import pandas as pd
import os

def salvar_dados(df):
    path = "model/dataset.csv"
    if os.path.exists(path):
        df_antigo = pd.read_csv(path)
        df_novo = pd.concat([df_antigo, df], ignore_index=True)
    else:
        df_novo = df
    df_novo.to_csv(path, index=False)
