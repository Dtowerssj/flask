from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})
@app.route('/webhook', methods=['POST'])
def webhook():
    data = json.loads(request.data)
    symbol = data['symbol']
    print(symbol)
    return symbol


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
