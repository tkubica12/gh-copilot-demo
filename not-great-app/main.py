import sqlite3
import subprocess
import pickle
from flask import Flask, request, jsonify

app = Flask(__name__)
DATABASE = 'test.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)')
    conn.commit()
    conn.close()

@app.route('/add_user', methods=['POST'])
def add_user():
    username = request.form['username']
    password = request.form['password']
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # SQL Injection vulnerability
    cursor.execute(f"INSERT INTO users (username, password) VALUES ('{username}', '{password}')")
    conn.commit()
    conn.close()
    return 'User added successfully'

@app.route('/get_user', methods=['GET'])
def get_user():
    user_id = request.args.get('id')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    # SQL Injection vulnerability
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    user = cursor.fetchone()
    conn.close()
    return jsonify(user)

@app.route('/run_command', methods=['POST'])
def run_command():
    command = request.form['command']
    # Command Injection vulnerability
    result = subprocess.check_output(command, shell=True)
    return result

@app.route('/deserialize', methods=['POST'])
def deserialize():
    data = request.form['data']
    # Insecure Deserialization vulnerability
    obj = pickle.loads(data)
    return str(obj)

@app.route('/xss', methods=['GET'])
def xss():
    name = request.args.get('name')
    # Cross-Site Scripting (XSS) vulnerability
    return f"<h1>Hello {name}</h1>"

@app.route('/ssrf', methods=['GET'])
def ssrf():
    url = request.args.get('url')
    # Server-Side Request Forgery (SSRF) vulnerability
    response = requests.get(url)
    return response.content

@app.route('/open_redirect', methods=['GET'])
def open_redirect():
    url = request.args.get('url')
    # Open Redirect vulnerability
    return redirect(url)

@app.route('/path_traversal', methods=['GET'])
def path_traversal():
    filename = request.args.get('filename')
    # Path Traversal vulnerability
    with open(f"/var/www/uploads/{filename}", 'r') as file:
        content = file.read()
    return content

if __name__ == '__main__':
    init_db()
    app.run(debug=True)