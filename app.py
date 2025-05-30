from flask import Flask, jsonify, render_template_string, request, Response
import sqlite3
import os

app = Flask(__name__)

DB_PATH = 'toggle_state.db'
TOGGLES = ['기능1', '기능2', '기능3']

def init_db():
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE toggles (name TEXT PRIMARY KEY, state INTEGER)''')
        for name in TOGGLES:
            c.execute('INSERT INTO toggles (name, state) VALUES (?, ?)', (name, 0))
        conn.commit()
        conn.close()

def get_toggles():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT name, state FROM toggles')
    toggles = {name: bool(state) for name, state in c.fetchall()}
    conn.close()
    return toggles

def set_toggle(name, state):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE toggles SET state=? WHERE name=?', (int(state), name))
    conn.commit()
    conn.close()

@app.route('/api/toggles', methods=['GET'])
def api_get_toggles():
    return jsonify(get_toggles())

@app.route('/api/toggle', methods=['POST'])
def api_set_toggle():
    data = request.get_json()
    name = data.get('name')
    state = data.get('state')
    if name not in TOGGLES or state not in [True, False]:
        return jsonify({'error': 'Invalid data'}), 400
    set_toggle(name, state)
    return jsonify({'success': True})

@app.route('/api/toggle/<name>', methods=['GET'])
def api_get_toggle(name):
    if not name.isdigit():
        return Response('error', status=400, mimetype='text/plain')
    idx = int(name)
    if idx < 1 or idx > len(TOGGLES):
        return Response('error', status=404, mimetype='text/plain')
    toggles = get_toggles()
    toggle_name = TOGGLES[idx-1]
    return Response(str(toggles[toggle_name]).lower(), mimetype='text/plain')

@app.route('/dashboard', methods=['GET'])
def dashboard():
    toggles = get_toggles()
    toggle_infos = [
        {"name": "기능1", "desc": "이것은 첫 번째 임시 기능입니다."},
        {"name": "기능2", "desc": "이것은 두 번째 임시 기능입니다."},
        {"name": "기능3", "desc": "이것은 세 번째 임시 기능입니다."},
    ]
    return render_template_string('''
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>다크모드 토글</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body {
            background: #181C20;
            color: #fff;
            font-family: 'Inter', 'Pretendard', 'Apple SD Gothic Neo', Arial, sans-serif;
            min-height: 100vh;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            background: #23272F;
            border-radius: 24px;
            box-shadow: 0 4px 24px rgba(0,0,0,0.2);
            padding: 48px 32px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 32px;
        }
        .toggle-group {
            display: flex;
            gap: 32px;
        }
        .toggle-card {
            background: #23272F;
            border-radius: 18px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.12);
            padding: 32px 28px 24px 28px;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-width: 220px;
            max-width: 260px;
            gap: 18px;
            border: 1.5px solid #353B45;
        }
        .toggle-title {
            font-size: 1.15rem;
            font-weight: 700;
            margin-bottom: 2px;
        }
        .toggle-desc {
            font-size: 0.98rem;
            color: #b0b8c1;
            text-align: center;
            margin-bottom: 8px;
        }
        .toggle {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
        }
        .switch {
            position: relative;
            display: inline-block;
            width: 56px;
            height: 32px;
        }
        .switch input { display: none; }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0; left: 0; right: 0; bottom: 0;
            background: #353B45;
            border-radius: 32px;
            transition: background 0.2s;
            border: 2px solid #444B55;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 24px;
            width: 24px;
            left: 4px;
            bottom: 2px;
            background: #23272F;
            border-radius: 50%;
            transition: transform 0.2s, background 0.2s;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }
        input:checked + .slider {
            background: #444B55;
            border-color: #353B45;
        }
        input:checked + .slider:before {
            transform: translateX(24px);
            background: #b0b8c1;
        }
        .toggle-label {
            font-size: 1.1rem;
            font-weight: 700;
            letter-spacing: -0.5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h2 style="margin-bottom: 16px;">기능 토글</h2>
        <div class="toggle-group">
            {% for info in toggle_infos %}
            <div class="toggle-card">
                <div class="toggle-title">{{ info.name }}</div>
                <div class="toggle-desc">{{ info.desc }}</div>
                <div class="toggle">
                    <label class="switch">
                        <input type="checkbox" id="toggle-{{ loop.index0 }}" {% if toggles[info.name] %}checked{% endif %} onchange="toggleSwitch('{{ info.name }}', this.checked)">
                        <span class="slider"></span>
                    </label>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    <script>
        function toggleSwitch(name, state) {
            fetch('/api/toggle', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: name, state: state })
            }).then(res => res.json()).then(data => {
                if (!data.success) {
                    alert('상태 변경 실패');
                }
            });
        }
    </script>
</body>
</html>
''', toggles=toggles, toggle_infos=toggle_infos)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0')  