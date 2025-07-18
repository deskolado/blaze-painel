import joblib
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder
from datetime import datetime

def preprocessar_para_previsao(ultimos):
    df = pd.DataFrame(ultimos)
    df['minuto'] = pd.to_datetime(df['horario'], format='%H:%M').dt.minute
    df['hora'] = pd.to_datetime(df['horario'], format='%H:%M').dt.hour
    df['momento'] = df['hora'].apply(lambda h: 'madrugada' if h < 6 else 'manha' if h < 12 else 'tarde' if h < 18 else 'noite')
    df['momento_cod'] = LabelEncoder().fit_transform(df['momento'])
    df['freq_vermelho'] = (df['cor'] == 'vermelho').rolling(20).sum().fillna(0)
    df['freq_preto'] = (df['cor'] == 'preto').rolling(20).sum().fillna(0)
    df['dist_ultimo_branco'] = df['cor'][::-1].eq('branco').cumsum().where(df['cor'] == 'branco').ffill().fillna(0)
    df = df.dropna()

    X = df[['numero', 'minuto', 'hora', 'momento_cod', 'freq_vermelho', 'freq_preto', 'dist_ultimo_branco']]
    return X.iloc[-1:]

def prever_sinal(ultimos_resultados):
    if not os.path.exists("model/modelo.pkl"):
        return {
            "cor": "Indefinido",
            "branco": "Indefinido",
            "assertividade": 0.0
        }

    modelo_cor, modelo_branco = joblib.load("model/modelo.pkl")
    X = preprocessar_para_previsao(ultimos_resultados)

    cor_pred = modelo_cor.predict(X)[0]
    branco_pred = modelo_branco.predict(X)[0]
    proba = modelo_cor.predict_proba(X)[0]
    conf = round(np.max(proba) * 100, 2)

    cor_label = ['branco', 'preto', 'vermelho'][cor_pred] if cor_pred in [0, 1, 2] else 'Indefinido'
    return {
        "cor": cor_label.capitalize(),
        "branco": "Sim" if branco_pred == 1 else "Não",
        "assertividade": conf
    }
