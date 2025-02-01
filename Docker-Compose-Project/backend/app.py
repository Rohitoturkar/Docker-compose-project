from flask import Flask, request, jsonify
import mysql.connector
import os

app = Flask(__name__)

# Load database credentials from environment variables
db_config = {
    "host": "db",  # ✅ Matches the service name in docker-compose.yml
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}

# Ensure database connection
def get_db_connection():
    return mysql.connector.connect(**db_config)

# Create a table if it doesn't exist
def create_table():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL
            );
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print("Error creating table:", e)

# Route to add data to the database
@app.route('/add', methods=['POST'])
def add_data():
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"error": "Missing 'name' field"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name) VALUES (%s)", (name,))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Inserted: {name}"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
        conn.close()
        return jsonify({"users": users})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    create_table()  # Ensure table exists before running the app
    app.run(host='0.0.0.0', port=5000)

