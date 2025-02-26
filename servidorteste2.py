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
    tipo = db.Column(db.String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'funcionario',
        'polymorphic_on': tipo
    }

    @property
    def senha(self):
        raise AttributeError("A senha não pode ser acessada diretamente.")

    @senha.setter
    def senha(self, senha_plain):
        self._senha = generate_password_hash(senha_plain)

    def verificar_senha(self, senha_plain):
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


# Função para salvar imagem Base64
def salvar_imagem(base64_str, nome_arquivo, pasta):
    try:
        caminho_completo = os.path.join(pasta, f"{nome_arquivo}.png")
        with open(caminho_completo, 'wb') as f:
            f.write(base64.b64decode(base64_str))
        return caminho_completo
    except Exception as e:
        print(f"Erro ao salvar imagem: {e}")
        return None

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
        gerentes_encoded = []
        
        for g in gerentes:
            absolute_path = os.path.abspath(g.imagem)
            if os.path.exists(absolute_path) and (absolute_path.endswith('.png') or absolute_path.endswith('.jpg')):
                with open(absolute_path, 'rb') as img_file:
                    imagem_base64 = base64.b64encode(img_file.read()).decode('utf-8')
            else:
                print("Imagem não encontrada para o gerente", g.nome)
                imagem_base64 = g.imagem  # Mantém a referência caso a imagem não esteja salva

            gerentes_encoded.append({
                'id': g.id,
                'nome': g.nome,
                'email': g.email,
                'cpf': g.cpf,  # Adicionando CPF
                'celular': g.celular,  # Adicionando Celular
                'nivel_acesso': g.nivel_acesso,
                'imagem': imagem_base64  # Adicionando a imagem convertida
            })

        return jsonify(gerentes_encoded)

    data = request.get_json()

    if request.method == 'POST':
        if Gerente.query.filter_by(email=data['email']).first():
            return jsonify({'erro': 'E-mail já cadastrado!'}), 400
        if Gerente.query.filter_by(cpf=data['cpf']).first():
            return jsonify({'erro': 'CPF já cadastrado!'}), 400

        image_data = base64.b64decode(data['imagem'])
        image_path = f"fotos_gerentes/{data['nome']}" + data['extensao']
        with open(image_path, 'wb') as f:
            f.write(image_data)
        data['imagem'] = image_path

        new_gerente = Gerente(
            nome=data['nome'],
            email=data['email'],
            cpf=data['cpf'],  # Adicionando CPF
            celular=data['celular'],  # Adicionando Celular
            senha=data.get('senha', 'default_senha'),
            funcao='Gerente',
            nivel_acesso=data.get('nivel_acesso', 'Alto'),
            imagem=data['imagem']
        )

        try:
            db.session.add(new_gerente)
            db.session.commit()
            return jsonify({'mensagem': 'Gerente cadastrado com sucesso!'}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'erro': 'Erro ao inserir gerente. Verifique os dados.'}), 400

    elif request.method == 'PUT':
        gerente = Gerente.query.get(data.get('id'))
        if not gerente:
            return jsonify({'erro': 'Gerente não encontrado!'}), 404

        gerente.nome = data.get('nome', gerente.nome)
        gerente.email = data.get('email', gerente.email)
        gerente.cpf = data.get('cpf', gerente.cpf)  # Atualizando CPF
        gerente.celular = data.get('celular', gerente.celular)  # Atualizando Celular
        gerente.nivel_acesso = data.get('nivel_acesso', gerente.nivel_acesso)

        if 'senha' in data:
            gerente.senha = data['senha']

        if 'imagem' in data and data['imagem']:
            image_data = base64.b64decode(data['imagem'])
            image_path = f"fotos_gerentes/{data['nome']}" + data['extensao']
            with open(image_path, 'wb') as f:
                f.write(image_data)
            gerente.imagem = image_path

        try:
            db.session.commit()
            return jsonify({'mensagem': 'Gerente atualizado com sucesso!'}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({'erro': 'Erro ao atualizar gerente.'}), 400

    elif request.method == 'DELETE':
        gerente = Gerente.query.get(data.get('id'))
        if not gerente:
            return jsonify({'erro': 'Gerente não encontrado!'}), 404

        try:
            db.session.delete(gerente)
            db.session.commit()
            return jsonify({'mensagem': 'Gerente removido com sucesso!'}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({'erro': 'Erro ao remover gerente.'}), 400

    return jsonify({'erro': 'Método não permitido!'}), 405


# Gerenciamento de Funcionários
@app.route('/funcionarios', methods=['GET', 'POST', 'PUT', 'DELETE'])
def funcionarios_handler():
    if request.method == 'GET':
        funcionarios = Funcionario.query.all()
        funcionarios_encoded = []
        for f in funcionarios:
            funcionarios_encoded.append({
                'id': f.id,
                'nome': f.nome,
                'email': f.email,
                'cpf': f.cpf,  # Adicionando CPF
                'celular': f.celular,  # Adicionando Celular
                'funcao': f.funcao,
                'tipo': f.tipo
            })

        return jsonify(funcionarios_encoded)

    data = request.get_json()

    if request.method == 'POST':
        if Funcionario.query.filter_by(email=data['email']).first():
            return jsonify({'erro': 'E-mail já cadastrado!'}), 400
        if Funcionario.query.filter_by(cpf=data['cpf']).first():
            return jsonify({'erro': 'CPF já cadastrado!'}), 400

        new_funcionario = Funcionario(
            nome=data['nome'],
            email=data['email'],
            cpf=data['cpf'],  # Adicionando CPF
            celular=data['celular'],  # Adicionando Celular
            funcao=data.get('funcao', 'Funcionário'),
            senha=data.get('senha', 'default_senha'),
            tipo=data.get('tipo', 'funcionario'),
            imagem=""
        )

        try:
            db.session.add(new_funcionario)
            db.session.commit()
            return jsonify({'mensagem': 'Funcionário cadastrado com sucesso!'}), 201
        except IntegrityError:
            db.session.rollback()
            return jsonify({'erro': 'Erro ao inserir funcionário. Verifique os dados.'}), 400

    elif request.method == 'PUT':
        funcionario = Funcionario.query.get(data.get('id'))
        if not funcionario:
            return jsonify({'erro': 'Funcionário não encontrado!'}), 404

        funcionario.nome = data.get('nome', funcionario.nome)
        funcionario.email = data.get('email', funcionario.email)
        funcionario.cpf = data.get('cpf', funcionario.cpf)  # Atualizando CPF
        funcionario.celular = data.get('celular', funcionario.celular)  # Atualizando Celular
        funcionario.funcao = data.get('funcao', funcionario.funcao)

        try:
            db.session.commit()
            return jsonify({'mensagem': 'Funcionário atualizado com sucesso!'}), 200
        except IntegrityError:
            db.session.rollback()
            return jsonify({'erro': 'Erro ao atualizar funcionário.'}), 400

    elif request.method == 'DELETE':
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

# Login simples
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    funcionario = Funcionario.query.filter_by(email=data['email']).first()

    if not funcionario or not funcionario.verificar_senha(data['senha']):
        return jsonify({'erro': 'Credenciais inválidas!'}), 401

    return jsonify({'mensagem': f'Login bem-sucedido! Bem-vindo, {funcionario.nome}!'}), 200


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
    if request.method == 'GET':
        notificacoes = Notificacao.query.all()
        return jsonify([{'id': n.id, 'item_id': n.item_id, 'mensagem': n.mensagem} for n in notificacoes])

    data = request.get_json()
    if request.method == 'POST':
        new_notificacao = Notificacao(item_id=data['item_id'], mensagem=data['mensagem'])
        db.session.add(new_notificacao)
        db.session.commit()

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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)