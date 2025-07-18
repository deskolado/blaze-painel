import cv2
import pytesseract
import re
from model.trainer import treinar_modelo
from model.predictor import prever_sinal
from utils.storage import salvar_dados

def extrair_dados_da_imagem(image_path):
    imagem = cv2.imread(image_path)
    imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
    texto = pytesseract.image_to_string(imagem_rgb)

    padrao = r"(\d{2}:\d{2})\s+(\d+)\s+(vermelho|preto|branco)"
    encontrados = re.findall(padrao, texto.lower())

    dados = []
    for horario, numero, cor in encontrados:
        dados.append({
            "horario": horario,
            "numero": int(numero),
            "cor": cor
        })

    return dados

def analisar_imagem_e_gerar_sinal(image_path):
    try:
        dados = extrair_dados_da_imagem(image_path)
    except Exception as e:
        return {
            "erro": f"Erro ao extrair dados da imagem: {str(e)}",
            "cor": "Erro",
            "branco": "Erro",
            "assertividade": 0.0
        }

    if not dados or len(dados) < 20:
        return {
            "erro": "Imagem com poucos dados. Envie uma imagem com pelo menos 20 resultados.",
            "cor": "Indefinido",
            "branco": "Indefinido",
            "assertividade": 0.0
        }

    salvar_dados(dados)
    treinar_modelo()
    return prever_sinal(dados)
