import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import pymysql

load_dotenv()

app = Flask(__name__)

DB_CONFIG = {
    'host': os.environ['DB_HOST'],
    'user': os.environ.get('DB_USER', 'admin'),
    'password': os.environ['DB_PASSWORD'],
    'db': os.environ.get('DB_NAME', 'feedbackdb'),
    'cursorclass': pymysql.cursors.DictCursor
}

@app.route('/')
def health():
    return jsonify({'status': 'Flask is running'})

@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()

    if not data or not all(k in data for k in ('name', 'email', 'feedback')):
        return jsonify({'error': 'name, email and feedback are required'}), 400

    conn = pymysql.connect(**DB_CONFIG)
    try:
        with conn.cursor() as cur:
            cur.execute(
                'INSERT INTO feedback (name, email, feedback) VALUES (%s, %s, %s)',
                (data['name'], data['email'], data['feedback'])
            )
        conn.commit()
    finally:
        conn.close()

    return jsonify({'message': 'Feedback submitted successfully!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
