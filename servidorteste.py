from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import random
import os
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
CORS(app)
db = SQLAlchemy(app)

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
        'quantidade': 5,
        'extensao': '.png'
    },
    {
        'id': 2,
        'imagem': 'placeholder/salim.png',
        'nome': 'Feijão',
        'quantidade': 3,
        'extensao': '.png'
    },
    {
        'id': 3,
        'imagem': 'placeholder/evolucao.png',
        'nome': 'Macarrão',
        'quantidade': 2,
        'extensao': '.png'
    },
    {
        'id': 4,
        'imagem': 'placeholder/salim.png',
        'nome': 'Carne',
        'quantidade': 1,
        'extensao': '.png'
    },
    {
        'id': 5,
        'imagem': 'placeholder/salim.png',
        'nome': 'Batata',
        'quantidade': 3,
        'extensao': '.png'
    },
    {
        'id': 6,
        'imagem': 'placeholder/salim.png',
        'nome': 'Tomate',
        'quantidade': 4,
        'extensao': '.png'
    },
    {
        'id': 7,
        'imagem': 'placeholder/salim.png',
        'nome': 'Cebola',
        'quantidade': 6,
        'extensao': '.png'
    },
    {
        'id': 8,
        'imagem': 'placeholder/salim.png',
        'nome': 'Alho',
        'quantidade': 8,
        'extensao': '.png'
    },
    {
        'id': 9,
        'imagem': 'placeholder/evolucao.png',
        'nome': 'Pão',
        'quantidade': 10,
        'extensao': '.png'
    },
    {
        'id': 10,
        'imagem': 'placeholder/salim.png',
        'nome': 'Leite',
        'quantidade': 7,
        'extensao': '.png'
    },
    {
        'id': 11,
        'imagem': 'placeholder/salim.png',
        'nome': 'Ovos',
        'quantidade': 12,
        'extensao': '.png'
    },
    {
        'id': 12,
        'imagem': 'placeholder/salim.png',
        'nome': 'Queijo',
        'quantidade': 2,
        'extensao': '.png'
    },
    {
        'id': 13,
        'imagem': 'placeholder/salim.png',
        'nome': 'Presunto',
        'quantidade': 3,
        'extensao': '.png'
    },
    {
        'id': 14,
        'imagem': 'placeholder/salim.png',
        'nome': 'Manteiga',
        'quantidade': 1,
        'extensao': '.png'
    },
    {
        'id': 15,
        'imagem': 'placeholder/salim.png',
        'nome': 'Café',
        'quantidade': 5,
        'extensao': '.png'
    }
]
@app.route('/itens', methods=['GET'])
def get_itens():
    itensCopy = itens.copy()
    for item in itensCopy:
        absolute_path = os.path.abspath(item['imagem'])
        if os.path.exists(absolute_path) and absolute_path.endswith('.png'):
            with open(item['imagem'], 'rb') as f:
                item['imagem'] = base64.b64encode(f.read()).decode('utf-8')
        else:
            print("Imagem não encontrada do", item['nome'])
    return jsonify(itens)

@app.route('/add_item', methods=['POST'])
def add_item():
    data = request.get_json()
    
    image_data = base64.b64decode(data['imagem'])
    image_path = f"placeholder/{data['nome']}" + data['extensao']
    with open(image_path, 'wb') as f:
        f.write(image_data)
    data['imagem'] = image_path

    new_item = {
        'id': itens[-1]['id'] + 1,
        'imagem': data['imagem'],
        'nome': data['nome'],
        'quantidade': data['quantidade'],
        'extensao': data['extensao']
    }
    itens.append(new_item)
    print("Item adicionado com sucesso!")
    return jsonify({'message': 'Item adicionado com sucesso!'}), 201

#endregion

#region Teste de envio de itens, via SQL
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(200), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer)

#endregion

if __name__ == '__main__':
    app.run(debug=True)