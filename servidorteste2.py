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

# Modelos
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(200), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer)

class Gerente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    vendas = db.Column(db.Integer, default=0)

class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    quantidade = db.Column(db.Integer)

class Notificacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    mensagem = db.Column(db.String(200))

# Gerenciamento de Itens
@app.route('/item', methods=['GET', 'POST', 'PUT', 'DELETE'])
def item_handler():
    if request.method == 'GET':
        itens = Item.query.all()
        return jsonify([{'id': i.id, 'imagem': i.imagem, 'nome': i.nome, 'quantidade': i.quantidade} for i in itens])
    data = request.get_json()
    if request.method == 'POST':
        new_item = Item(imagem=data['imagem'], nome=data['nome'], quantidade=data['quantidade'])
        db.session.add(new_item)
    elif request.method == 'PUT':
        item = Item.query.get(data['id'])
        if item:
            item.nome = data.get('nome', item.nome)
            item.quantidade = data.get('quantidade', item.quantidade)
    elif request.method == 'DELETE':
        item = Item.query.get(data['id'])
        if item:
            db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Operação realizada com sucesso!'})

# Gerenciamento de Gerentes
@app.route('/gerente', methods=['POST', 'DELETE'])
def gerente_handler():
    data = request.get_json()
    if request.method == 'POST':
        new_gerente = Gerente(nome=data['nome'], email=data['email'])
        db.session.add(new_gerente)
    elif request.method == 'DELETE':
        gerente = Gerente.query.get(data['id'])
        if gerente:
            db.session.delete(gerente)
    db.session.commit()
    return jsonify({'message': 'Operação realizada com sucesso!'})

# Gerenciamento de Funcionários
@app.route('/funcionarios', methods=['GET', 'POST', 'DELETE'])
def funcionarios_handler():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        funcionarios = Funcionario.query.paginate(page, 10, False).items
        return jsonify([{'id': f.id, 'nome': f.nome, 'vendas': f.vendas} for f in funcionarios])
    data = request.get_json()
    if request.method == 'POST':
        new_funcionario = Funcionario(nome=data['nome'])
        db.session.add(new_funcionario)
    elif request.method == 'DELETE':
        funcionario = Funcionario.query.get(data['id'])
        if funcionario:
            db.session.delete(funcionario)
    db.session.commit()
    return jsonify({'message': 'Operação realizada com sucesso!'})

# Criar e Registrar Vendas
@app.route('/venda', methods=['POST'])
def realizar_venda():
    data = request.get_json()
    print("Dados recebidos:", data)  # Debug: mostra os dados recebidos
    item = Item.query.get(data.get('item_id'))
    funcionario = Funcionario.query.get(data.get('funcionario_id'))
    print("Item:", item)
    print("Funcionário:", funcionario)
    
    # Se necessário, converta a quantidade para int
    quantidade_venda = int(data.get('quantidade', 0))
    print("Quantidade da venda:", quantidade_venda)
    
    if item and funcionario and item.quantidade >= quantidade_venda:
        item.quantidade -= quantidade_venda
        funcionario.vendas += 1
        venda = Venda(funcionario_id=funcionario.id, item_id=item.id, quantidade=quantidade_venda)
        db.session.add(venda)
        db.session.commit()
        return jsonify({'message': 'Venda realizada com sucesso!'})
    return jsonify({'message': 'Erro ao processar venda'}), 400


# Relatórios de vendas
@app.route('/relatorio_vendas', methods=['GET'])
def relatorio_vendas():
    funcionarios = Funcionario.query.order_by(Funcionario.vendas.desc()).limit(5).all()
    return jsonify([{'id': f.id, 'nome': f.nome, 'vendas': f.vendas} for f in funcionarios])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria todas as tabelas definidas pelos modelos
    app.run(debug=True)
