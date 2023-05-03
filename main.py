from flask import Flask, jsonify, request
import os
import json
import MetaTrader5 as mt5
import orders

app = Flask(__name__)

# establish connection to the MetaTrader 5 terminal
if not mt5.initialize("C:/Program Files/MetaTrader 5/terminal64.exe"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()

# display data on MetaTrader 5 version
print(mt5.version())
# connect to the trade account without specifying a password and a server
account=5012885841
server="MetaQuotes-Demo"
pw="aafm2bqu"
authorized=mt5.login(account, pw, server)  # the terminal database password is applied if connection data is set to be remembered
if authorized:
    print("connected to account #{}".format(account))
else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

@app.route('/')
def index():
    return jsonify({"TradingView & MT5 server"})

def extract_trade_info(text):
    lines = text.split('\n')
    symbol = ''
    buy_sell = ''
    tp = 0
    sl = 0
    
    for line in lines:
        if 'OMERTA' in line:
            symbol = line.split(' ')[-1]
        if 'Opportunity' in line:
            buy_sell = line.split(' ')[-2]
        if 'TP' in line:
            tp = float(line.split(':')[-1])
        if 'SL' in line:
            sl = float(line.split(':')[-1])
            
    return symbol, buy_sell, tp, sl

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    if 'text/plain' in request.headers['Content-Type']:
        # Obtener el cuerpo de la solicitud en formato de texto plano
        request_text = request.data.decode('utf-8')
        print(request_text)

        # Procesar la solicitud
        trade_info = extract_trade_info(request_text)
        print(trade_info)

        if trade_info[1] == 'BUY':
            orders.open_buy(trade_info)
        
        if trade_info[1] == 'SELL':
            orders.open_sell(trade_info)

        return 'OK'
    else:
        return 'Unsupported Media Type', 415
    

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
