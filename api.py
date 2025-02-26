from flask import Flask, requests, jsonify
from datetime import datetime
import requests
import json
import sqlite3
import os 

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('bot_data.db')
    c = conn.cursor()
    c.execute("
        CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NO NULL,
        message_text TEXT,
        ai_response TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ")
    conn.commit()
    conn.close()

init_db()

def save_to_db():
