from flask import Flask, jsonify, request
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)

@app.route('/random', methods=['GET'])
def get_random_number():
    random_number = random.randint(1, 10)
    return jsonify({'random_number': random_number})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['usuario']
    password = data['senha']
    if username == 'admin' and password == 'admin':
        return jsonify({'message': 'Login efetuado'})
    else:
        return jsonify({'message': 'Informações inválidas'})

@app.route('/get_image', methods=['POST'])
def get_image():
    image_path = "placeholder/evolucao.png"
    if os.path.exists(image_path) and image_path.endswith('.png'):
        return send_file(image_path, mimetype='image/png')
    else:
        print("Imagem não encontrada")
        return jsonify({'message': 'Imagem não encontrada'})

if __name__ == '__main__':
    app.run(debug=True)