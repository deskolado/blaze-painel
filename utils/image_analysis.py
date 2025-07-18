import pytesseract
import cv2
import pandas as pd
import os
from model.trainer import treinar_modelo
from model.predictor import prever_sinal
from utils.storage import salvar_dados

def extrair_dados_da_imagem(caminho):
    imagem = cv2.imread(caminho)
    texto = pytesseract.image_to_string(imagem)
    linhas = texto.split('\n')
    dados = []
    for linha in linhas:
        if "-" in linha and any(c in linha for c in ['V', 'P', 'B']):
            partes = linha.strip().split()
            if len(partes) >= 2:
                horario, cor = partes[0], partes[1]
                dados.append((horario, cor))
    return dados

def analisar_imagem_e_gerar_sinal(caminho):
    try:
        dados = extrair_dados_da_imagem(caminho)
    except Exception as e:
        return {"erro": f"Erro na leitura da imagem: {str(e)}", "cor": "Erro", "branco": "Erro", "assertividade": 0.0}

    if len(dados) < 10:
        return {"erro": "Dados insuficientes para treinar", "cor": "N/A", "branco": "N/A", "assertividade": 0.0}

    df = pd.DataFrame(dados, columns=["horario", "cor"])
    salvar_dados(df)
    treinar_modelo()
    return prever_sinal()
