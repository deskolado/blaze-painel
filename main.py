from flask import Flask, render_template, request
from PIL import Image
import io
import os
from werkzeug.utils import secure_filename
import datetime
from utils.image_analysis import analisar_imagem_e_gerar_sinal

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    if request.method == 'POST':
        if 'imagem' not in request.files:
            return render_template('index.html', erro='Nenhuma imagem enviada.')

        file = request.files['imagem']
        if file.filename == '':
            return render_template('index.html', erro='Nome de arquivo inválido.')

        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            resultado = analisar_imagem_e_gerar_sinal(filepath)
        except Exception as e:
            resultado = {'erro': f'Erro ao processar a imagem: {str(e)}'}

    return render_template('index.html', resultado=resultado)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
