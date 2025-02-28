# Sistema de Gerenciamento de Estoque e Vendas

## Descrição
Este é um sistema desenvolvido utilizando **Godot Engine** para a interface e **Flask** para a API backend. Ele permite gerenciar estoque, cadastrar funcionários, processar vendas e gerar notificações quando os produtos estão em falta.

## Funcionalidades
- **Autenticação de Usuário:** Login com e-mail e senha.
- **Cadastro de Funcionários:** Armazena nome, e-mail, CPF, celular, função e imagem.
- **Gerenciamento de Itens:** Adicionar, editar e remover produtos do estoque.
- **Processamento de Vendas:** Registrar vendas e atualizar o estoque.
- **Geração de Notificações:** Avisar quando um produto está sem estoque.
- **Relatório de Vendas:** Exibir vendas realizadas por funcionário.

## Tecnologias Utilizadas
### Frontend:
- **Godot Engine** (GDScript)

### Backend:
- **Flask** (Python)
- **Flask-CORS** (Habilita requisições entre domínios)
- **Flask-SQLAlchemy** (ORM para banco de dados SQLite)
- **Werkzeug** (Segurança de senhas)

### Banco de Dados:
- **SQLite**

## Estrutura do Projeto
```
/
|-- app.py               # Servidor principal do backend
|-- servidorteste.py     # Servidor de testes
|-- setup_db.py          # Script de configuração do banco de dados
|-- project.godot        # Arquivo do projeto Godot
|-- Scenes/              # Telas da interface do sistema
|-- PackedScenes/        # Componentes reutilizáveis
```

## Configuração e Execução
### Backend (Flask API)
1. Instale as dependências:
   ```bash
   pip install flask flask-cors flask-sqlalchemy werkzeug
   ```
2. Configure o banco de dados:
   ```bash
   python setup_db.py
   ```
3. Inicie o servidor:
   ```bash
   python app.py
   ```

### Frontend (Godot)
1. Abra o **Godot Engine** e carregue o arquivo `project.godot`.
2. Execute a cena principal para testar a aplicação.

## Endpoints da API
### Autenticação
- `POST /login` - Login de usuário

### Gerenciamento de Funcionários
- `GET /funcionarios` - Lista os funcionários cadastrados
- `POST /funcionarios` - Cadastra um novo funcionário
- `PUT /funcionarios` - Atualiza informações de um funcionário
- `DELETE /funcionarios` - Remove um funcionário

### Gerenciamento de Itens
- `GET /item` - Lista os itens do estoque
- `POST /item` - Adiciona um novo item ao estoque
- `PUT /item` - Edita um item existente
- `DELETE /item` - Remove um item do estoque

### Processamento de Vendas
- `POST /venda` - Registra uma nova venda
- `GET /vendas/<funcionario_id>` - Retorna vendas feitas por um funcionário
- `GET /relatorio_vendas` - Retorna os funcionários com mais vendas

### Notificações
- `GET /notificacao` - Lista notificações ativas
- `DELETE /notificacao` - Remove uma notificação
