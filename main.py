from flask import Flask, jsonify, request
import os
import sys
import json
import MetaTrader5 as mt5
import orders
from pyngrok import conf, ngrok
import subprocess

app = Flask(__name__)



# establish connection to the MetaTrader 5 terminal
if not mt5.initialize("C:/Program Files/MetaTrader 5/terminal64.exe"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()

# display data on MetaTrader 5 version
print(mt5.version())
# connect to the trade account without specifying a password and a server
account=51208256
server="ICMarkets-Demo"
pw="NcXtqQms"
authorized=mt5.login(account, pw, server)  # the terminal database password is applied if connection data is set to be remembered
if authorized:
    print("connected to account #{}".format(account))
else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

@app.route('/')
def index():
    return jsonify({"TradingView & MT5 server"})

def extract_symbol(text):
    lines = text.split('\n')
    symbol = ''

    for line in lines:
        if 'OMERTA' in line:
            symbol = line.split(' ')[-1]

    return symbol

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

def extract_sl(text):
    lines = text.split('\n')
    sl = ''

    for line in lines:
        if 'SL' in line:
            sl = line.split(' ')[-1]

    return sl

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    if 'text/plain' in request.headers['Content-Type']:
        # Obtener el cuerpo de la solicitud en formato de texto plano
        request_text = request.data.decode('utf-8')
        print(request_text)

        # Verificar que haya que cerrar posicion
        if 'Closed' in request_text:
            symbol = extract_symbol(request_text)
            orders.close_position(symbol)
            return

        # Verificar que haya que modificar stop loss
        if 'Stop Loss Modified' in request_text:
            symbol = extract_symbol(request_text)
            sl = extract_sl(request_text)
            orders.modify_sl(symbol, sl)
            exit()

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
""" 
if ngrok.get_ngrok_process():
    print("La conexión con Ngrok ya ha sido establecida.")
    print(ngrok.get_ngrok_process())
    # Detener el túnel y eliminar el proceso de ngrok
    ngrok.disconnect(ngrok.get_ngrok_process())
else:
    print("La conexión con Ngrok aún no ha sido establecida.")
    # Crear un túnel con ngrok
    public_url = ngrok.connect(5000) 
     """

#os.system('cmd /c "ngrok.exe http 5000"')
# command = "./ngrok http 5000"

# Ejecutar el comando
#process = subprocess.Popen(['cmd', '/c', 'ngrok.exe http 5000'])

# Obtener la URL de ngrok del output
#output = process.stdout.read()
#print(output)
#ngrok_url = output.split()[-1].decode("utf-8")
#print("URL de ngrok:", ngrok_url)

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))


