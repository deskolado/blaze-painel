import cv2
import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta
from model.predictor import prever_sinal
from model.trainer import treinar_modelo

def extrair_dados_da_imagem(filepath):
    # Função básica para detectar bolinhas vermelhas, pretas, brancas e horários
    # Aqui você deve evoluir com extração por OCR e mais precisão
    # Retorno simulado:
    dados = []
    for i in range(30):
        dados.append({
            "horario": (datetime.now() - timedelta(minutes=i)).strftime("%H:%M"),
            "numero": np.random.randint(0, 15),
            "cor": np.random.choice(["vermelho", "preto", "branco"])
        })
    return dados[::-1]  # Do mais antigo ao mais recente

def analisar_imagem_e_gerar_sinal(filepath):
    dados = extrair_dados_da_imagem(filepath)

    # Salvar dados extraídos para treino
    df = pd.DataFrame(dados)
    if not os.path.exists("model/dataset.csv"):
        df.to_csv("model/dataset.csv", index=False)
    else:
        df.to_csv("model/dataset.csv", mode='a', header=False, index=False)

    # Treinar a IA com todos os dados disponíveis
    treinar_modelo()

    # Prever a entrada para 2 minutos à frente
    previsao = prever_sinal(dados[-10:])  # usa os últimos 10 registros

    return {
        "cor": previsao["cor"],
        "branco": previsao["branco"],
        "assertividade": previsao["assertividade"],
        "status": "Entrada gerada",
        "horario": (datetime.now() + timedelta(minutes=2)).strftime("%H:%M")
    }
