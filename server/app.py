# app.py

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/")
def get_countries():
    return jsonify({
        "status": 200
    })

