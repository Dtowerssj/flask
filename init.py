import os
import subprocess

# Instalar los paquetes de requirements.txt
subprocess.call('pip install -r requirements.txt', shell=True)

# Iniciar el servidor Flask en un proceso en segundo plano
flask_process = subprocess.Popen('python main.py', shell=True)

# Iniciar Ngrok en un proceso en segundo plano
# Comando para iniciar ngrok
# command = "./ngrok http 5000"

# Ejecutar el comando
#process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)

# Obtener la URL de ngrok del output
#output = process.stdout.read()
#ngrok_url = output.split()[-1].decode("utf-8")
#print("URL de ngrok:", ngrok_url)

# Esperar a que el proceso de Ngrok termine
#ngrok_process.wait()

# Detener el proceso de Flask
#flask_process.terminate()
