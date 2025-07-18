import joblib
import numpy as np
import os

def prever_sinal(ultimos_resultados):
    if not os.path.exists("model/modelo.pkl"):
        return {
            "cor": "Indefinido",
            "branco": "Indefinido",
            "assertividade": 0.0
        }

    modelo, le = joblib.load("model/modelo.pkl")

    numeros = [r['numero'] for r in ultimos_resultados[-1:]]
    X = np.array(numeros).reshape(-1, 1)
    previsao = modelo.predict(X)[0]
    probas = modelo.predict_proba(X)[0]
    cor = le.inverse_transform([previsao])[0]

    return {
        "cor": cor.capitalize(),
        "branco": "Sim" if cor == "branco" else "Não",
        "assertividade": round(np.max(probas) * 100, 2)
    }
