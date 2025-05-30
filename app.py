from flask import Flask, jsonify
from flask_cors import CORS
import traceback
import os

app = Flask(__name__)
CORS(app)


@app.route('/test', methods=['POST', 'GET'])
def Test():
    return 1

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)  