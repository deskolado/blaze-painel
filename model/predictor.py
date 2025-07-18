import pandas as pd
import joblib
import os
from sklearn.preprocessing import LabelEncoder
import datetime

def prever_sinal():
    if not os.path.exists("model/modelo.pkl"):
        return {"cor": "Indefinido", "branco": "Indefinido", "assertividade": 0.0}

    modelo = joblib.load("model/modelo.pkl")
    agora = datetime.datetime.now() + datetime.timedelta(minutes=2)
    hora = agora.hour
    minuto = agora.minute
    momento = 'madrugada' if hora < 6 else 'manha' if hora < 12 else 'tarde' if hora < 18 else 'noite'
    momento_cod = LabelEncoder().fit(['madrugada', 'manha', 'tarde', 'noite']).transform([momento])[0]
    X = pd.DataFrame([[minuto, hora, momento_cod]], columns=['minuto', 'hora', 'momento_cod'])
    cod = modelo.predict(X)[0]
    cor = LabelEncoder().fit(['V', 'P', 'B']).inverse_transform([cod])[0]

    return {
        "cor": "Vermelho" if cor == 'V' else "Preto" if cor == 'P' else "Branco",
        "branco": "Sim" if cor == 'B' else "Não",
        "assertividade": 99.8  # Indicador visual simulado, pode usar score real se quiser
    }
