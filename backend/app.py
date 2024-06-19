from flask import Flask, request, jsonify
import sqlite3
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS

DATABASE = 'zoo.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_db():
    db = get_db()
    db.execute('''
        CREATE TABLE IF NOT EXISTS animals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            age INTEGER NOT NULL,
            name TEXT NOT NULL
        )
    ''')
    db.commit()

# Initialize the database when the app starts
initialize_db()

@app.route("/", methods=['GET'])
def hello_world():
    return "[{'color': 'blue'}]"

# Read - Get all animals
@app.route("/get_all_animals", methods=['GET'])
def get_animals():
    db = get_db()
    cur = db.execute('SELECT * FROM animals')
    animals = cur.fetchall()
    return jsonify([dict(animal) for animal in animals])

# Read - Get a single animal by ID
@app.route("/get_animal/<int:id>", methods=['GET'])
def get_animal(id):
    db = get_db()
    cur = db.execute('SELECT * FROM animals WHERE id = ?', (id,))
    animal = cur.fetchone()
    if animal is None:
        return jsonify({'error': 'Animal not found'}), 404
    return jsonify(dict(animal))

# Create - Add a new animal
@app.route("/new_animal", methods=['POST'])
def create_animal():
    new_animal = request.get_json()
    type = new_animal.get('type')
    age = new_animal.get('age')
    name = new_animal.get('name')
    
    if not type or not age or not name:
        return jsonify({'error': 'Missing fields'}), 400
    
    db = get_db()
    db.execute('INSERT INTO animals (type, age, name) VALUES (?, ?, ?)',
               (type, age, name))
    db.commit()
    return jsonify({'message': 'Animal created'}), 201

# Update - Modify an existing animal
@app.route("/update_animal/<int:id>", methods=['PUT'])
def update_animal(id):
    updated_animal = request.get_json()
    type = updated_animal.get('type')
    age = updated_animal.get('age')
    name = updated_animal.get('name')
    
    if not type or not age or not name:
        return jsonify({'error': 'Missing fields'}), 400

    db = get_db()
    db.execute('UPDATE animals SET type = ?, age = ?, name = ? WHERE id = ?',
               (type, age, name, id))
    db.commit()
    
    return jsonify({'message': 'Animal updated'}), 200

# Delete - Remove an animal by ID
@app.route("/delete_animal/<int:id>", methods=['DELETE'])
def delete_animal(id):
    db = get_db()
    db.execute('DELETE FROM animals WHERE id = ?', (id,))
    db.commit()
    return jsonify({'message': 'Animal deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
