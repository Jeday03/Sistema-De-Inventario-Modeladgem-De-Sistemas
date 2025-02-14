from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

@app.route('/random', methods=['GET'])
def get_random_number():
    random_number = random.randint(1, 10)
    return jsonify({'random_number': random_number})

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    if username == 'admin' and password == 'admin':
        return jsonify({'message': 'Login efetuado'}), 200
    else:
        return jsonify({'message': 'Informações inválidas'}), 200

if __name__ == '__main__':
    app.run(debug=True)