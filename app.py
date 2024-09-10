import sqlite3
from flask import Flask, jsonify, request

app = Flask(__name__)


def create_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)''')
    conn.commit()
    conn.close()


def db_conn():
    conn = None
    try:
        conn = sqlite3.connect('users.db')
    except sqlite3.Error as e:
        print("Error while connecting to SQLite database:", e)
    return conn


@app.route('/users', methods=['GET'])
def get_users():
    conn = db_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM users''')
    rows = c.fetchall()
    conn.close()
    return jsonify(rows)


@app.route('/users', methods=['POST'])
def add_user():
    conn = db_conn()
    c = conn.cursor()
    c.execute('''INSERT INTO users (name) VALUES (?) RETURNING *''',
              (request.json['name'],))
    row = c.fetchone()  # Get the inserted user
    conn.commit()
    conn.close()
    return jsonify(row)


@app.route('/users/<int:id>', methods=['GET'])
def get_user():
    conn = db_conn()
    c = conn.cursor()
    c.execute('''SELECT * FROM users WHERE id = ?''', (id,))
    row = c.fetchone()
    conn.close()
    return jsonify(row)


@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    conn = db_conn()
    c = conn.cursor()
    c.execute('''UPDATE users SET name = ? WHERE id = ? RETURNING *''',
              (request.json['name'], id))
    row = c.fetchone()
    conn.commit()
    conn.close()
    return jsonify(row)


@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    conn = db_conn()
    c = conn.cursor()
    c.execute('''DELETE FROM users WHERE id = ?''', (id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'User deleted successfully'})


if __name__ == '__main__':
    create_db()
    app.run(debug=True)
