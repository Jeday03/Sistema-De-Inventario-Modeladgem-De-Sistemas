from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import random
import os

app = Flask(__name__)
CORS(app)


'''
Função teste de GET
'''
@app.route('/random', methods=['GET'])
def get_random_number():
    random_number = random.randint(1, 10)
    return jsonify({'random_number': random_number})


'''
O método POST é usado para enviar dados para o servidor.
Daí, conseguimos pegar o usuário e senha, da mesma forma que fizemos no app cliente.
RETIRAR O ADMIN, ISSO FOI SÓ PRA TESTE
'''
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['usuario']
    password = data['senha']
    if username == 'admin' and password == 'admin':
        return jsonify({'message': 'Login efetuado'})
    else:
        return jsonify({'message': 'Informações inválidas'})


'''
Muito importante usar o absolute_path, se não dá erro 500.
O send_file é outro módulo do Flask, não esquecer de importar.
Verifiquem a existência do arquivo e se ele é do tipo esperado, daí mandem o print. Alterem o valor da response também.
'''
@app.route('/get_image', methods=['GET'])
def get_image():
    image_path = "placeholder/evolucao.png"
    absolute_path = os.path.abspath(image_path)
    if os.path.exists(absolute_path) and absolute_path.endswith('.png'):
        print("Encontrei a imagem")
        return send_file(image_path, mimetype='image/png'), 200
    else:
        print("Imagem não encontrada")
        return jsonify({'message': 'Imagem não encontrada'}), 404

if __name__ == '__main__':
    app.run(debug=True)