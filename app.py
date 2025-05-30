
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/test', methods=['POST', 'GET'])
def Test():
    return jsonify({'test': True}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')  