from flask import Flask, jsonify, request, send_file
from matplotlib.pylab import f
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import base64

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
CORS(app)
db = SQLAlchemy(app)

"""
    Metodos GET não necessitam de JSON no corpo da requisição.
    Metodos POST, PUT e DELETE necessitam de JSON no corpo da requisição.
"""



# Criando diretórios para armazenar imagens
IMAGE_DIRS = ["fotos_gerentes", "fotos_funcionarios", "placeholder"]
for dir_path in IMAGE_DIRS:
    os.makedirs(dir_path, exist_ok=True)


# Modelos
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(200), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer)
    preco = db.Column(db.Float, nullable=False)

class Funcionario(db.Model):
    __tablename__ = 'funcionario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    cpf = db.Column(db.String(14), unique=True, nullable=False)  # Adicionado CPF
    celular = db.Column(db.String(20), nullable=False)  # Adicionado Celular
    funcao = db.Column(db.String(50), nullable=False)
    imagem = db.Column(db.String(200), nullable=False)
    _senha = db.Column("senha", db.String(255), nullable=False)
    vendas = db.relationship('Venda', back_populates='funcionario')
    tipo = db.Column(db.String(20), nullable=False)  # Agora obrigatório

    @property
    def senha(self):
        raise AttributeError("A senha não pode ser acessada diretamente.")

    @senha.setter
    def senha(self, senha_plain):
        self._senha = generate_password_hash(senha_plain)

    def verificar_senha(self, senha_plain):
        return check_password_hash(self._senha, senha_plain)


class Venda(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    funcionario_id = db.Column(db.Integer, db.ForeignKey('funcionario.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)

    funcionario = db.relationship('Funcionario', back_populates='vendas')
    item = db.relationship('Item', backref='vendas')


class Notificacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    mensagem = db.Column(db.String(200))


# Gerenciamento de Itens com filtro por prefixo, GET, POST, PUT e DELETE
@app.route('/item', methods=['GET', 'POST', 'PUT', 'DELETE'])
def item_handler():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)  # Obtém o número da página
        per_page = 10  # Define o número de itens por página
        prefix = request.args.get('prefix')

        # Aplica filtro por prefixo, se fornecido
        query = Item.query
        if prefix:
            query = query.filter(Item.nome.startswith(prefix))

        # Aplica paginação
        itens_paginated = query.paginate(page=page, per_page=per_page, error_out=False)
        itens = itens_paginated.items

        itens_encoded = []
        for i in itens:
            print(i.nome)
            print(i.imagem[-4:])
            imagem_base64 = get_image(i.imagem, 'fotos_itens', i)  # Corrigindo variável errada
            itens_encoded.append({
                'id': i.id,
                'imagem': imagem_base64,
                'nome': i.nome,
                'quantidade': i.quantidade,
                'extensao': i.imagem[-4:],
                'preco': i.preco
            })

        return jsonify(itens_encoded)

    data = request.get_json()
    if request.method == 'POST':
        data['imagem'] = set_image(data['imagem'], 'fotos_itens', data['nome'])
        print(data['imagem'])

        # Validação do campo 'preco'
        if 'preco' not in data or data['preco'] is None:
            return jsonify({'erro': 'O campo "preco" é obrigatório'}), 400

        new_item = Item(
            imagem=data['imagem'],
            nome=data['nome'],
            quantidade=data['quantidade'],
            preco=data['preco']
        )

        db.session.add(new_item)

    elif request.method == 'PUT':
        """
        Exemplo de JSON para testar no Postman:
        {
            "id": 1,
            "nome": "Notebook Dell XPS",
            "quantidade": 8
        }
        """
        item = Item.query.get(data['id'])
        if item:
            item.nome = data.get('nome', item.nome)
            item.quantidade = data.get('quantidade', item.quantidade)
            image_path = set_image(data['imagem'], 'fotos_itens', data['nome'])
            item.imagem = image_path
            item.preco = data.get('preco', item.preco)
    elif request.method == 'DELETE':
        """
        Exemplo de JSON para testar no Postman:
        {
            "id": 1
        }
        """
        item = Item.query.get(data['id'])
        if item:
            db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Operação realizada com sucesso!'})

# Gerenciamento de Funcionários (Gerentes e Caixas diferenciados pelo tipo)
@app.route('/funcionarios', methods=['GET', 'POST', 'PUT', 'DELETE'])
def funcionarios_handler():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = 10
        funcionarios_paginated = Funcionario.query.paginate(page=page, per_page=per_page, error_out=False)
        funcionarios = funcionarios_paginated.items

        funcionarios_encoded = []
        for f in funcionarios:
            imagem_base64 = get_image(f.imagem, 'fotos_funcionarios', f)

            funcionarios_encoded.append({
                'id': f.id,
                'nome': f.nome,
                'email': f.email,
                'cpf': f.cpf,  
                'celular': f.celular,  
                'funcao': f.funcao,  
                'tipo': f.tipo,  
                'imagem': imagem_base64,  
                'vendas': [{'id': v.id, 'item_id': v.item_id, 'quantidade': v.quantidade} for v in f.vendas],
                'extensao': f.imagem[-4:]
            })

        return jsonify(funcionarios_encoded)

    data = request.get_json()

    if request.method == 'POST':
        """
        Exemplo de JSON para cadastrar um funcionário no Postman:
        {
            "nome": "Carlos Silva",
            "email": "carlos@email.com",
            "cpf": "123.456.789-00",
            "celular": "(32) 91234-5678",
            "funcao": "Caixa",  // ou "Gerente"
            "senha": "senha123",
            "imagem": "",
            "extensao": ".png"
        }
        """
        if Funcionario.query.filter_by(email=data['email']).first():
            return jsonify({'erro': 'E-mail já cadastrado!'}), 400
        if Funcionario.query.filter_by(cpf=data['cpf']).first():
            return jsonify({'erro': 'CPF já cadastrado!'}), 400

        data['imagem'] = set_image(data['imagem'], 'fotos_funcionarios', data['cpf'])

        # Define o tipo com base na função
        tipo_funcionario = "gerente" if data['funcao'].lower() == "gerente" else "caixa"

        novo_funcionario = Funcionario(
            nome=data['nome'],
            email=data['email'],
            cpf=data['cpf'],
            celular=data['celular'],
            funcao=data['funcao'],
            senha=data['senha'],
            tipo=tipo_funcionario,
            imagem=data['imagem']
        )

        try:
            db.session.add(novo_funcionario)
            db.session.commit()
            return jsonify({'mensagem': 'Funcionário cadastrado com sucesso!'}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'erro': 'Erro ao inserir funcionário. Verifique os dados.'}), 400

    elif request.method == 'PUT':
        """
        Exemplo de JSON para atualizar um funcionário no Postman:
        {
            "id": 1,
            "nome": "Carlos S. Oliveira",
            "cpf": "123.456.789-00",
            "celular": "(32) 91111-2222",
            "funcao": "Caixa" // ou "Gerente"
        }
        """
        funcionario = Funcionario.query.get(data.get('id'))
        if not funcionario:
            return jsonify({'erro': 'Funcionário não encontrado!'}), 404

        funcionario.nome = data.get('nome', funcionario.nome)
        funcionario.email = data.get('email', funcionario.email)
        funcionario.cpf = data.get('cpf', funcionario.cpf)
        funcionario.celular = data.get('celular', funcionario.celular)
        funcionario.funcao = data.get('funcao', funcionario.funcao)

        # Atualiza o tipo com base na função
        funcionario.tipo = "gerente" if data.get('funcao', funcionario.funcao).lower() == "gerente" else "caixa"

        if 'senha' in data and data['senha']:
            funcionario.senha = data['senha']

        try:
            db.session.commit()
            return jsonify({'mensagem': 'Funcionário atualizado com sucesso!'}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({'erro': 'Erro ao atualizar funcionário.'}), 400

    elif request.method == 'DELETE':
        """
        Exemplo de JSON para deletar um funcionário no Postman:
        {
            "id": 1
        }
        """
        funcionario = Funcionario.query.get(data.get('id'))
        if not funcionario:
            return jsonify({'erro': 'Funcionário não encontrado!'}), 404

        try:
            db.session.delete(funcionario)
            db.session.commit()
            return jsonify({'mensagem': 'Funcionário removido com sucesso!'}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({'erro': 'Erro ao remover funcionário.'}), 400

    return jsonify({'erro': 'Método não permitido!'}), 405


# Endpoint para retornar as vendas de um funcionário específico
@app.route('/vendas/<int:funcionario_id>', methods=['GET'])
def vendas_funcionario(funcionario_id):
    vendas = Venda.query.filter_by(funcionario_id=funcionario_id).all()
    vendas_list = []
    for v in vendas:
        vendas_list.append({
            'id': v.id,
            'funcionario_id': v.funcionario_id,
            'item_id': v.item_id,
            'quantidade': v.quantidade
        })
    return jsonify(vendas_list)

# Criar e Registrar Vendas
@app.route('/venda', methods=['POST'])
def realizar_venda():
    """
        Exemplo de JSON para testar no Postman:
        {
            "funcionario_id": 1,
            "item_id": 2,
            "quantidade": 3
        }
            # Tanto o funcionário quanto o item devem existir no banco de dados!!!!
    """
    data = request.get_json()
    print(data)
    for item in data['items']:
        item_id = item['id']
        quantidade_venda = item['quantidade']
        item = Item.query.get(item_id)
        if item and item.quantidade >= quantidade_venda:
            item.quantidade -= quantidade_venda
            if item.quantidade == 0:
                mensagem_notificacao = item.nome
                nova_notificacao = Notificacao(item_id=item.id, mensagem=mensagem_notificacao)
                db.session.add(nova_notificacao)
                print(f"🔔 Notificação criada: {mensagem_notificacao}")
            db.session.commit()
        else:
            return jsonify({'message': 'Erro ao processar venda'}), 400
    return jsonify({'message': 'Venda realizada com sucesso!'})

    '''
    data = request.get_json()
    print("Dados recebidos:", data)
    
    item = Item.query.get(data.get('item_id'))
    funcionario = Funcionario.query.get(data.get('funcionario_id'))
    quantidade_venda = int(data.get('quantidade', 0))

    if item and funcionario and item.quantidade >= quantidade_venda:
        item.quantidade -= quantidade_venda
        venda = Venda(funcionario_id=funcionario.id, item_id=item.id, quantidade=quantidade_venda)
        db.session.add(venda)
        
        # Se o estoque do item chegou a zero, cria uma notificação automaticamente
        if item.quantidade == 0:
            mensagem_notificacao = f"Estoque do item {item.nome} esgotado!"
            nova_notificacao = Notificacao(item_id=item.id, mensagem=mensagem_notificacao)
            db.session.add(nova_notificacao)
            print(f"🔔 Notificação criada: {mensagem_notificacao}")

        db.session.commit()
        return jsonify({'message': 'Venda realizada com sucesso!'})

    return jsonify({'message': 'Erro ao processar venda'}), 400
    '''


# Login simples
@app.route('/login', methods=['POST'])
def login():
    """
        Exemplo de JSON para testar no Postman:
        {
            "email": "carlos@email.com",
            "senha": "senha123"
        }

    """
    data = request.get_json()

    if data['email'] == "admin" and data['senha'] == "admin":
        return jsonify({'message': True, 'funcao': 'Admin'}), 200
    
    funcionario = Funcionario.query.filter_by(email=data['email']).first()


    if not funcionario or not funcionario.verificar_senha(data['senha']):
        return jsonify({'erro': 'Credenciais inválidas!'}), 401

    return jsonify({'message': f'Login bem-sucedido! Bem-vindo, {funcionario.nome}!', 'funcao': funcionario.funcao}), 200

# Relatórios de vendas
@app.route('/relatorio_vendas', methods=['GET'])
def relatorio_vendas():
    funcionarios = (
        db.session.query(Funcionario, func.count(Venda.id).label("total_vendas"))
        .outerjoin(Venda, Funcionario.id == Venda.funcionario_id)
        .group_by(Funcionario.id)
        .order_by(func.count(Venda.id).desc())
        .limit(5)
        .all()
    )

    return jsonify([
        {
            'id': f.id,
            'nome': f.nome,
            'total_vendas': total_vendas
        } for f, total_vendas in funcionarios
    ])

# Gerenciamento de Notificações
@app.route('/notificacao', methods=['GET', 'POST', 'DELETE'])
def notificacao_handler():
    print("Veio ate aq")
    if request.method == 'GET':
        itens_encoded = []
        notificacoes = Notificacao.query.all()
        print(notificacoes)
        for i in notificacoes:
            itens_encoded.append({
                'id': i.id,
                'item_id': i.item_id,
                'mensagem': i.mensagem
            })

        return jsonify(itens_encoded)
    elif request.method == 'DELETE':
        data = request.get_json()
        """
            Exemplo de JSON para testar no Postman:
            {
                "id": 1
            }
        """
        notificacao = Notificacao.query.get(data['id'])
        if notificacao:
            db.session.delete(notificacao)
            db.session.commit()
            return jsonify({'message': 'Notificação removida!'})

    return jsonify({'message': 'Operação realizada com sucesso!'}), 200

def set_image(image_code, folder, name):
    image_data = base64.b64decode(image_code)
    image_path = f"{folder}/{name}.png"
    with open(image_path, 'wb') as f:
        f.write(image_data)
    return image_path

def get_image(image_path, folder, f):
    imagem_base64 = ""
    absolute_path = os.path.abspath(f.imagem)
    if os.path.exists(absolute_path) and (absolute_path.endswith('.png') or absolute_path.endswith('.jpg')):
        with open(f.imagem, 'rb') as file:
            imagem_base64 = base64.b64encode(file.read()).decode('utf-8')
    else:
        print("Imagem não encontrada do", f.nome)
    return imagem_base64

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)