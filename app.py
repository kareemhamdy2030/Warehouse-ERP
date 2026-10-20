from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import json

app = Flask(__name__)
CORS(app)

DATABASE = 'erp_system.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS system_store (
            key TEXT PRIMARY KEY,
            data TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/get-data/<key>', methods=['GET'])
def get_data(key):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT data FROM system_store WHERE key = ?', (key,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify(json.loads(row[0]))
    return jsonify([])

@app.route('/api/save-data/<key>', methods=['POST'])
def save_data(key):
    payload = request.get_json()
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO system_store (key, data)
        VALUES (?, ?)
    ''', (key, json.dumps(payload, ensure_ascii=False)))
    conn.commit()
    conn.close()
    return jsonify({"status": "success"})

import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)