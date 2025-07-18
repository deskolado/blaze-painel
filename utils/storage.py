import pandas as pd
import os

def salvar_dados(df):
    path = "model/dataset.csv"
    if os.path.exists(path):
        antigo = pd.read_csv(path)
        df = pd.concat([antigo, df], ignore_index=True)
    df.to_csv(path, index=False)
