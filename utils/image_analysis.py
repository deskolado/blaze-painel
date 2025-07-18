import pytesseract
import cv2
import os
from model.predictor import prever_sinal
from utils.storage import salvar_dados
from model.trainer import treinar_modelo
import pandas as pd

def extrair_dados_da_imagem(caminho):
    imagem = cv2.imread(caminho)
    texto = pytesseract.image_to_string(imagem)

    linhas = texto.split('\n')
    dados = []
    for linha in linhas:
        if "-" in linha and any(c in linha for c in ['V', 'P', 'B']):
            partes = linha.strip().split()
            if len(partes) >= 2:
                horario = partes[0]
                cor = partes[1]
                dados.append((horario, cor))
    return dados

def analisar_imagem_e_gerar_sinal(caminho_imagem):
    try:
        dados = extrair_dados_da_imagem(caminho_imagem)
    except Exception as e:
        return {
            "erro": f"Erro ao extrair dados da imagem: {str(e)}",
            "cor": "Erro",
            "branco": "Erro",
            "assertividade": 0.0
        }

    df = pd.DataFrame(dados, columns=["horario", "cor"])
    if len(df) < 10:
        return {"erro": "Dados insuficientes para análise."}

    df.to_csv("model/dataset.csv", index=False)
    salvar_dados(df)
    treinar_modelo()

    return prever_sinal()
