from Flask import Flask, jsonify, request
from Flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/random', methods=['GET'])
def get_random_number():
    random_number = random.randint(1, 10)
    return jsonify({'random_number': random_number})

if __name__ == '__main__':
    app.run(debug=True)