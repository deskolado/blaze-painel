import pandas as pd
import os
from datetime import datetime, timedelta
from model.predictor import prever_sinal
from model.trainer import treinar_modelo

def extrair_dados_da_imagem(filepath):
    # Simulado (substitua por OCR futuro)
    dados = []
    for i in range(40):
        dados.append({
            "horario": (datetime.now() - timedelta(minutes=i)).strftime("%H:%M"),
            "numero": int(14 * abs((i*17 % 20) % 1)),  # pseudo aleatório
            "cor": ["vermelho", "preto", "branco"][i % 3]
        })
    return dados[::-1]

def analisar_imagem_e_gerar_sinal(filepath):
    dados = extrair_dados_da_imagem(filepath)

    # Armazena para treino
    df = pd.DataFrame(dados)
    if not os.path.exists("model/dataset.csv"):
        df.to_csv("model/dataset.csv", index=False)
    else:
        df.to_csv("model/dataset.csv", mode='a', header=False, index=False)

    treinar_modelo()

    ultimos = dados[-20:]
    previsao = prever_sinal(ultimos)

    return {
        "cor": previsao["cor"],
        "branco": previsao["branco"],
        "assertividade": previsao["assertividade"],
        "status": "Entrada gerada com IA",
        "horario": (datetime.now() + timedelta(minutes=2)).strftime("%H:%M")
    }
