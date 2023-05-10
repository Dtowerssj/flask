import tkinter as tk
import subprocess
    

class TradingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("TV-MT5 Rio-Server")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Crear campos de entrada        
        self.account_entry = tk.Entry(self, font=("Arial", 14), justify="center")
        self.account_entry.insert(0, "123456")
        
        self.password_entry = tk.Entry(self, font=("Arial", 14), justify="center", show="*")
        self.password_entry.insert(0, "********")
        
        self.server_entry = tk.Entry(self, font=("Arial", 14), justify="center")
        self.server_entry.insert(0, "demo.mt5.com:443")
        
        self.lot_entry = tk.Entry(self, font=("Arial", 14), justify="center")
        self.lot_entry.insert(0, "0.01")
        
        # Crear etiquetas para los campos de entrada
        tk.Label(self, text="Lotaje", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self, text="Número de cuenta", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self, text="Contraseña", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10)
        tk.Label(self, text="Servidor", font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=10)
        
        # Posicionar los campos de entrada
        self.lot_entry.grid(row=0, column=1, padx=10, pady=10)
        self.account_entry.grid(row=1, column=1, padx=10, pady=10)
        self.password_entry.grid(row=2, column=1, padx=10, pady=10)
        self.server_entry.grid(row=3, column=1, padx=10, pady=10)
        
        # Crear botón para correr o detener init.py
        self.run_button = tk.Button(self, text="Correr", font=("Arial", 14), command=self.run_init)
        self.run_button.grid(row=4, column=1, padx=10, pady=30)
        
    def run_init(self):
        # Código para correr init.py
        cmd = "python init.py"
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        if error:
            print(f"Error: {error}")
        else:
            print(f"Output: {output}")
        
if __name__ == "__main__":
    app = TradingApp()
    app.mainloop()
