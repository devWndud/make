from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/test', methods=['POST', 'GET'])
def Test():
    return jsonify({'test': True}), 200

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    note = data.get('note', '')
    return jsonify({'summary': note}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0')  