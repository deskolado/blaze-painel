from flask import Flask, render_template, request
from utils.image_analysis import analisar_imagem_e_gerar_sinal
import os

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    if request.method == "POST":
        imagem = request.files["imagem"]
        caminho = os.path.join("static", "upload.png")
        imagem.save(caminho)
        resultado = analisar_imagem_e_gerar_sinal(caminho)
    return render_template("index.html", resultado=resultado)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
