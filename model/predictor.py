import pandas as pd
import joblib
import datetime
import os
from sklearn.preprocessing import LabelEncoder

def prever_sinal():
    if not os.path.exists("model/modelo.pkl"):
        return {
            "cor": "Indefinido",
            "branco": "Indefinido",
            "assertividade": 0.0
        }

    modelo = joblib.load("model/modelo.pkl")
    agora = datetime.datetime.now()
    hora = agora.hour
    minuto = agora.minute + 2  # Previsão para 2 minutos à frente

    if minuto >= 60:
        minuto -= 60
        hora += 1
        if hora >= 24:
            hora = 0

    momento = 'madrugada' if hora < 6 else 'manha' if hora < 12 else 'tarde' if hora < 18 else 'noite'
    momento_cod = LabelEncoder().fit(['madrugada', 'manha', 'tarde', 'noite']).transform([momento])[0]
    X = pd.DataFrame([[minuto, hora, momento_cod]], columns=['minuto', 'hora', 'momento_cod'])

    cor_cod = modelo.predict(X)[0]
    cor = LabelEncoder().fit(['V', 'P', 'B']).inverse_transform([cor_cod])[0]

    return {
        "cor": "Vermelho" if cor == 'V' else "Preto" if cor == 'P' else "Branco",
        "branco": "Sim" if cor == 'B' else "Não",
        "assertividade": 99.9  # Simulado, ajustável
    }
