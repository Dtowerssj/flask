import subprocess
import tkinter as tk
import ctypes
import os
import signal
import MetaTrader5 as mt5
import orders
import requests
import json

ctypes.windll.shcore.SetProcessDpiAwareness(True)

# Variable para almacenar el PID del proceso Flask
flask_pid = None
p = None

def run_bot():
    global flask_pid, p
    data = get_data()

    # Si ya hay un proceso Flask en ejecución, detenerlo primero
    if p:
        # Detener el proceso de Flask
        stop_bot()
        exit() 

    if data[0] and data[1] and data[2] and data[3]:
        # connect_mt5(data[0], data[1], data[2], data[3])
        # Ejecutar init.py con los argumentos correspondientes
        command = "python init.py"
        p = subprocess.run(command, shell=True)
       # print(p)
        #flask_pid = p.pid
        run_button.config(text="Detener Bot")
        
        # URL del endpoint en localhost para conectar a MT5
        url = 'http://localhost:5000/connect_mt5'

        # Datos en formato JSON que queremos enviar
        data = {
            "account": data[0], 
            "server": data[1], 
            "pw": data[2], 
            "risk": data[3]
        }

        # Realizar la solicitud POST con los datos en formato JSON
        response = requests.post(url, json=data)
        print(response)

        # Verificar el código de respuesta
        if response.status_code == 200:
            print('Solicitud enviada correctamente')
        else:
            print('Error en la solicitud')

        # Imprimir la respuesta del servidor
        print(response.json())
    else:
        show_err("Por favor llenar todos los campos")

def connect_mt5(account, server, pw, risk):
    print("risk in gui: ", risk)
    #orders.risk = risk
    #print("lot in orders: ", orders.lot)
    #get_trading_lot(float(lot))
    
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
            for prop in account_info_dict:
                print("  {}={}".format(prop, account_info_dict[prop]))
            print()
    
            # convert the dictionary into DataFrame and print
            """ df=pd.DataFrame(list(account_info_dict.items()),columns=['property','value'])
            print("account_info() as dataframe:")
            print(df) """
        else:
            print("failed to connect to trade account, error code =",mt5.last_error())
        #show_err("connected to account")
    else:
        print("failed to connect at account #{}, error code: {}".format(account, mt5.last_error()))

def check_balance():
    account_info=mt5.account_info()
    if account_info!=None:
        # display trading account data 'as is'
        print(account_info)
        # display trading account data in the form of a dictionary
        print("Show account_info()._asdict():")
        account_info_dict = mt5.account_info()._asdict()
        for prop in account_info_dict:
            print("  {}={}".format(prop, account_info_dict[prop]))
            print()
    else:
        print("failed to connect to trade account, error code =",mt5.last_error())   

def stop_bot():
    global flask_pid # hacemos la variable global para poder accederla desde esta función

    if flask_pid:
        print('logica stop')

def on_closing():
    stop_bot()
    window.destroy()

def show_err(text):
    error_label.config(text=text)

def show_green_output(text):
    green_label.config(text=text)

def get_data():
    account_number = account_number_entry.get()
    server = server_entry.get()
    password = password_entry.get()
    risk_size = risk_size_entry.get()
    return account_number, server, password, risk_size

# Configurar la ventana
window = tk.Tk()
window.title("TV-MT5 Rio-Server")
window.geometry("500x360")

# Agregar los elementos de la interfaz
tk.Label(window, text="Número de cuenta:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
account_number_entry = tk.Entry(window, font=("Arial", 14), justify="center")
account_number_entry.grid(row=0, column=1, padx=10, pady=10)
account_number_entry.insert(0, "5013741150")

tk.Label(window, text="Servidor:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
server_entry = tk.Entry(window, font=("Arial", 14), justify="center")
server_entry.grid(row=1, column=1, padx=10, pady=10)
server_entry.insert(0, "MetaQuotes-Demo")

tk.Label(window, text="Contraseña:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
password_entry = tk.Entry(window, font=("Arial", 14), justify="center", show="*")
password_entry.grid(row=2, column=1, padx=10, pady=10)
password_entry.insert(0, "eoosj3nu")

tk.Label(window, text="Riesgo (%):", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10)
risk_size_entry = tk.Entry(window, font=("Arial", 14), justify="center")
risk_size_entry.grid(row=3, column=1, padx=10, pady=10)
risk_size_entry.insert(0, "5")

run_button = tk.Button(window, text="Correr Bot", font=("Calibri", 14), command=run_bot)
run_button.grid(row=4, column=1, padx=10, pady=30)

error_label = tk.Label(window, fg="red", font=("Arial", 11))
error_label.grid(row=5, column=0, columnspan=2, padx=10, pady=0)

green_label = tk.Label(window, text='', fg="green", font=("Arial", 11))
green_label.grid(row=5, column=0, columnspan=2, padx=10, pady=0)

# Configurar el evento de cierre de la ventana
#window.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar la ventana
window.mainloop()