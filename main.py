from flask import Flask, jsonify, request
import os
import MetaTrader5 as mt5
import orders
#from gui import show_err, show_green_output

app = Flask(__name__)

account= None
server= None
pw= None
lot = None
risk = 3
balance = 0

def get_trading_data(values):
    global account,server,pw,lot
    account= values[0]
    server= values[1]
    pw= values[2]
    lot = values[3]
    print(account, server)


""""
account=211990864
server="OctaFX-Demo"
pw="jy6yTYRE"

 Name     : Diego Torress
Type     : Forex Hedged USD
Server   : MetaQuotes-Demo
Login    : 5013587602
Password : 5ljmmqqr
Investor : chylmpe2 

Name     : Diego Torresss
Type     : Forex Hedged USD
Server   : MetaQuotes-Demo
Login    : 5013741150
Password : eoosj3nu
Investor : 2owynrnf


"""


""" 

# establish connection to the MetaTrader 5 terminal
if not mt5.initialize("C:/Program Files/MetaTrader 5/terminal64.exe"):
    print("initialize() failed, error code =",mt5.last_error())
    quit()

# display data on MetaTrader 5 version
print(mt5.version())
# connect to the trade account without specifying a password and a server

authorized = None
if account and server and lot and pw:
    authorized=mt5.login(account, pw, server)  # the terminal database password is applied if connection data is set to be remembered
if authorized:
    text = "connected to account #{}".format(account)
    print(text)
    #show_err("connected to account")
else:
    print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))
 """
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

@app.route('/connect_mt5', methods=['POST'])
def connect_mt5():
    global risk, balance
    if request.is_json:
        data = request.get_json()

        account = data.get("account")
        pw = data.get("pw")
        server = data.get("server")
        risk = data.get("risk")

        # establish connection to the MetaTrader 5 terminal
        if not mt5.initialize("C:/Program Files/MetaTrader 5/terminal64.exe"):
            print("initialize() failed, error code =",mt5.last_error())
            quit()

        # display data on MetaTrader 5 version
        print(mt5.version())
        # connect to the trade account without specifying a password and a server

        authorized=mt5.login(int(account), pw, server)  # the terminal database password is applied if connection data is set to be remembered
        if authorized:
            text = "connected to account #{}".format(account)
            print(text)
            account_info=mt5.account_info()
            if account_info!=None:
                # display trading account data 'as is'
                #print(account_info)

                # display trading account data in the form of a dictionary
                print("Show account_info()._asdict():")
                account_info_dict = mt5.account_info()._asdict()
                print(account_info_dict['balance'] )
                balance = account_info_dict['balance']

                print(risk, balance)

                """ for prop in account_info_dict:
                    print("  {}={}".format(prop, account_info_dict[prop]))
                print() """
        
            else:
                print("failed to connect to trade account, error code =",mt5.last_error())
        #show_err("connected to account")
        else:
            print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error())) 
        
        return jsonify({'message': 'Solicitud JSON recibida correctamente'})
    else:
        return jsonify({'message': 'La solicitud no es de tipo JSON'})
    

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    global risk, balance
    if 'text/plain' in request.headers['Content-Type']:
        # Obtener el cuerpo de la solicitud en formato de texto plano
        request_text = request.data.decode('utf-8')

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
            orders.open_buy(trade_info, risk, balance)
        
        if trade_info[1] == 'SELL':
            orders.open_sell(trade_info, risk, balance)

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


