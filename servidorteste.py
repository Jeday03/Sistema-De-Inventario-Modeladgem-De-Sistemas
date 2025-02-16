from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import random
import os
import base64

app = Flask(__name__)
CORS(app)

#region Teste de GET
'''
Função teste de GET
'''
@app.route('/random', methods=['GET'])
def get_random_number():
    random_number = random.randint(1, 10)
    return jsonify({'random_number': random_number})
#endregion

#region Teste de login
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
#endregion

#region Teste de imagem
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
#endregion

#region Teste de envio de itens, via lista Python
itens = [
    {
        'id': 1,
        'imagem': 'placeholder/salim.png',
        'nome': 'Arroz',
        'quantidade': 5
    },
    {
        'id': 2,
        'imagem': 'placeholder/salim.png',
        'nome': 'Feijão',
        'quantidade': 3
    },
    {
        'id': 3,
        'imagem': 'placeholder/evolucao.png',
        'nome': 'Macarrão',
        'quantidade': 2
    },
    {
        'id': 4,
        'imagem': 'placeholder/salim.png',
        'nome': 'Carne',
        'quantidade': 1
    },
    {
        'id': 5,
        'imagem': 'placeholder/salim.png',
        'nome': 'Batata',
        'quantidade': 3
    },
    {
        'id': 6,
        'imagem': 'placeholder/salim.png',
        'nome': 'Tomate',
        'quantidade': 4
    }
]

@app.route('/itens', methods=['GET'])
def get_itens():
    for item in itens:
        absolute_path = os.path.abspath(item['imagem'])
        if os.path.exists(absolute_path) and absolute_path.endswith('.png'):
            with open(item['imagem'], 'rb') as f:
                item['imagem'] = base64.b64encode(f.read()).decode('utf-8')
        else:
            print("Imagem não encontrada do ", item['nome'])
    return jsonify(itens)

#endregion


if __name__ == '__main__':
    app.run(debug=True)