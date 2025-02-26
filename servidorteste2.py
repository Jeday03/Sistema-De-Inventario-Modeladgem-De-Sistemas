from flask import Flask, jsonify, request, send_file
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

# Modelos
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    imagem = db.Column(db.String(200), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer)



class Funcionario(db.Model):
    __tablename__ = 'funcionario'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    funcao = db.Column(db.String(50), nullable=False)
    _senha = db.Column("senha", db.String(255), nullable=False)  # Armazena o hash da senha
    vendas = db.relationship('Venda', back_populates='funcionario')
    tipo = db.Column(db.String(20))  # Diferencia funcionário de gerente

    __mapper_args__ = {
        'polymorphic_identity': 'funcionario',
        'polymorphic_on': tipo
    }

    # Setter para armazenar a senha como hash
    @property
    def senha(self):
        raise AttributeError("A senha não pode ser acessada diretamente.")

    @senha.setter
    def senha(self, senha_plain):
        """Armazena a senha de forma segura como um hash"""
        self._senha = generate_password_hash(senha_plain)

    # Método para verificar a senha
    def verificar_senha(self, senha_plain):
        """Verifica se a senha fornecida confere com o hash armazenado"""
        return check_password_hash(self._senha, senha_plain)


class Gerente(Funcionario):
    id = db.Column(db.Integer, db.ForeignKey('funcionario.id'), primary_key=True)
    nivel_acesso = db.Column(db.String(20), nullable=False, default="Alto")

    __mapper_args__ = {
        'polymorphic_identity': 'gerente'
    }



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
        prefix = request.args.get('prefix')
        if prefix:
            itens = Item.query.filter(Item.nome.startswith(prefix)).all()
        else:
            itens = Item.query.all()
        itens_encoded = []
        for i in itens:
            absolute_path = os.path.abspath(i.imagem)
            if os.path.exists(absolute_path) and (absolute_path.endswith('.png') or absolute_path.endswith('.jpg')):
                with open(absolute_path, 'rb') as f:
                    imagem_base64 = base64.b64encode(f.read()).decode('utf-8')
            else:
                print("Imagem não encontrada para o item", i.nome)
                imagem_base64 = i.imagem
            itens_encoded.append({
                'id': i.id,
                'imagem': imagem_base64,
                'nome': i.nome,
                'quantidade': i.quantidade
            })
        return jsonify(itens_encoded)

    data = request.get_json()
    if request.method == 'POST':
        image_data = base64.b64decode(data['imagem'])
        image_path = f"placeholder/{data['nome']}" + data['extensao']
        with open(image_path, 'wb') as f:
            f.write(image_data)
        data['imagem'] = image_path
        new_item = Item(imagem=data['imagem'], nome=data['nome'], quantidade=data['quantidade'])
        db.session.add(new_item)
    elif request.method == 'PUT':
        item = Item.query.get(data['id'])
        if item:
            item.nome = data.get('nome', item.nome)
            item.quantidade = data.get('quantidade', item.quantidade)
            item.imagem = data.get('imagem', item.imagem)
    elif request.method == 'DELETE':
        item = Item.query.get(data['id'])
        if item:
            db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Operação realizada com sucesso!'})

# Gerenciamento de Gerentes com GET, POST, PUT e DELETE
@app.route('/gerente', methods=['GET', 'POST', 'PUT', 'DELETE'])
def gerente_handler():
    if request.method == 'GET':
        gerentes = Gerente.query.all()
        return jsonify([{'id': g.id, 'nome': g.nome, 'email': g.email, 'nivel_acesso': g.nivel_acesso} for g in gerentes])
    
    data = request.get_json()
    if request.method == 'POST':
        new_gerente = Gerente(
            nome=data['nome'],
            email=data['email'],
            senha=data.get('senha', 'default_senha'),  # Recomenda-se usar hash
            funcao='Gerente',
            nivel_acesso=data.get('nivel_acesso', 'Alto')
        )
        db.session.add(new_gerente)
    elif request.method == 'PUT':
        gerente = Gerente.query.get(data['id'])
        if gerente:
            gerente.nome = data.get('nome', gerente.nome)
            gerente.email = data.get('email', gerente.email)
            gerente.nivel_acesso = data.get('nivel_acesso', gerente.nivel_acesso)
    elif request.method == 'DELETE':
        gerente = Gerente.query.get(data['id'])
        if gerente:
            db.session.delete(gerente)
    db.session.commit()
    return jsonify({'message': 'Operação realizada com sucesso!'})

# Gerenciamento de Funcionários
@app.route('/funcionarios', methods=['GET', 'POST', 'PUT', 'DELETE'])
def funcionarios_handler():
    if request.method == 'GET':
        page = request.args.get('page', 1, type=int)
        per_page = 10
        funcionarios_paginated = Funcionario.query.paginate(page=page, per_page=per_page, error_out=False)
        funcionarios = funcionarios_paginated.items
        
        return jsonify([{
        'id': f.id,
        'nome': f.nome,
        'email': f.email,
        'funcao': f.funcao,
        'tipo': f.tipo,
        'vendas': [{'id': v.id, 'item_id': v.item_id, 'quantidade': v.quantidade} for v in f.vendas]  # ✅ Convertendo cada venda para dicionário
    } for f in funcionarios])


    data = request.get_json()

    if request.method == 'POST':
        # Verifica se o e-mail já existe
        if Funcionario.query.filter_by(email=data['email']).first():
            return jsonify({'erro': 'E-mail já cadastrado!'}), 400  # Retorna erro HTTP 400

        new_funcionario = Funcionario(
            nome=data['nome'],
            email=data['email'],
            funcao=data.get('funcao', 'Funcionário'),
            senha=data.get('senha', 'default_senha'),  # 🔥 Senha será automaticamente armazenada como hash
            tipo=data.get('tipo', 'funcionario')
        )

        try:
            db.session.add(new_funcionario)
            db.session.commit()
            return jsonify({'mensagem': 'Funcionário cadastrado com sucesso!'}), 201  # Sucesso HTTP 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'erro': 'Erro ao inserir funcionário. Verifique os dados.'}), 400

    elif request.method == 'PUT':
        funcionario = Funcionario.query.get(data.get('id'))
        if not funcionario:
            return jsonify({'erro': 'Funcionário não encontrado!'}), 404  # Retorna erro HTTP 404

        funcionario.nome = data.get('nome', funcionario.nome)
        funcionario.email = data.get('email', funcionario.email)
        funcionario.funcao = data.get('funcao', funcionario.funcao)

        # 🔥 Atualiza a senha, se fornecida, armazenando o hash
        if 'senha' in data:
            funcionario.senha = data['senha']

        funcionario.tipo = data.get('tipo', funcionario.tipo)

        try:
            db.session.commit()
            return jsonify({'mensagem': 'Funcionário atualizado com sucesso!'}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({'erro': 'Erro ao atualizar funcionário.'}), 400

    elif request.method == 'DELETE':
        funcionario = Funcionario.query.get(data.get('id'))
        if not funcionario:
            return jsonify({'erro': 'Funcionário não encontrado!'}), 404  # Retorna erro HTTP 404

        try:
            db.session.delete(funcionario)
            db.session.commit()
            return jsonify({'mensagem': 'Funcionário removido com sucesso!'}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({'erro': 'Erro ao remover funcionário.'}), 400

    return jsonify({'erro': 'Método não permitido!'}), 405  # Retorna erro HTTP 405 para métodos inválidos

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
    data = request.get_json()
    print("Dados recebidos:", data)
    item = Item.query.get(data.get('item_id'))
    funcionario = Funcionario.query.get(data.get('funcionario_id'))
    quantidade_venda = int(data.get('quantidade', 0))
    
    if item and funcionario and item.quantidade >= quantidade_venda:
        item.quantidade -= quantidade_venda
        numero_vendas = Venda.query.filter_by(funcionario_id=funcionario.id).count()
        venda = Venda(funcionario_id=funcionario.id, item_id=item.id, quantidade=quantidade_venda)
        db.session.add(venda)
        db.session.commit()
        return jsonify({'message': 'Venda realizada com sucesso!'})
    return jsonify({'message': 'Erro ao processar venda'}), 400

# Relatórios de vendas: retorna os 5 funcionários que mais venderam
@app.route('/relatorio_vendas', methods=['GET'])
def relatorio_vendas():
    funcionarios = (
        db.session.query(Funcionario, func.count(Venda.id).label("total_vendas"))
        .outerjoin(Venda, Funcionario.id == Venda.funcionario_id)  # Une as tabelas
        .group_by(Funcionario.id)
        .order_by(func.count(Venda.id).desc())  # Ordena pelo número de vendas
        .limit(5)
        .all()
    )

    return jsonify([
        {
            'id': f.id,
            'nome': f.nome,
            'total_vendas': total_vendas  # Agora pegamos o total de vendas corretamente
        } for f, total_vendas in funcionarios
    ])

# Gerenciamento de Notificações de estoque zerado com GET, POST e DELETE
@app.route('/notificacao', methods=['GET', 'POST', 'DELETE'])
def notificacao_handler():
    if request.method == 'GET':
        notificacoes = Notificacao.query.all()
        return jsonify([{'id': n.id, 'item_id': n.item_id, 'mensagem': n.mensagem} for n in notificacoes])
    
    data = request.get_json()
    if request.method == 'POST':
        new_notificacao = Notificacao(item_id=data['item_id'], mensagem=data['mensagem'])
        db.session.add(new_notificacao)
        db.session.commit()
        # Simulação de envio de e-mail para todos os gerentes
        gerentes = Gerente.query.all()
        for g in gerentes:
            print(f"Email enviado para {g.email}: {data['mensagem']}")
        return jsonify({'message': 'Notificação criada e emails enviados!'})
    elif request.method == 'DELETE':
        notificacao = Notificacao.query.get(data['id'])
        if notificacao:
            db.session.delete(notificacao)
            db.session.commit()
            return jsonify({'message': 'Notificação removida!'})
    return jsonify({'message': 'Operação realizada com sucesso!'})

# Login simples
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    funcionario = Funcionario.query.filter_by(email=data['email']).first()

    if not funcionario or not funcionario.verificar_senha(data['senha']):
        return jsonify({'erro': 'Credenciais inválidas!'}), 401  # Retorna erro HTTP 401

    return jsonify({'mensagem': f'Login bem-sucedido! Bem-vindo, {funcionario.nome}!'}), 200




if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas definidas pelos modelos
    app.run(debug=True)
