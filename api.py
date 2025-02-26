from flask import Flask, request, jsonify
from datetime import datetime
import requests
import json
import sqlite3
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        message_text TEXT,
        ai_response TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

def save_to_db(user_id, message_text, ai_response):
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("""
        INSERT INTO messages (user_id, message_text, ai_response)
        VALUES (?, ?, ?)
    """, (user_id, message_text, ai_response))
    conn.commit()
    conn.close()

def get_ai_response(message_text):
    ai_service_url = "https://your-ai-service.com/api/response"

    payload = {
        'message_text': message_text
    }
    try:
        response = requests.post(ai_service_url, json=payload)
        if response.status_code == 200:
            ai_response = response.json().get('ai_response')
            return ai_response
        else:
            return "Error: Unable to get response from AI service."
    except requests.exceptions.RequestException as e:
        return f"Exception: {str(e)}"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    user_id = data.get('user_id')
    message_text = data.get('message_text')

    if not user_id or not message_text:
        return jsonify({'error': 'Invalid data'}), 400

    ai_response = get_ai_response(message_text)
    save_to_db(user_id, message_text, ai_response)

    return jsonify({'ai_response': ai_response})

if __name__ == '__main__':
    app.run(debug=True)