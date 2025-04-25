import requests
import tkinter as tk
from tkinter import messagebox, filedialog

def obter_taxas_de_cambio(api_key):
    url = f'https://open.er-api.com/v6/latest/USD'  # Você pode mudar a moeda base se desejar
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()['rates']
    else:
        messagebox.showerror("Erro", f'Erro ao acessar a API: {response.status_code}')
        return None

def converter_moeda(valor, taxa):
    return valor * taxa

def converter():
    api_key = 'SUA_CHAVE_DE_API'  # Substitua pela sua chave de API
    taxas = obter_taxas_de_cambio(api_key)
    
    if taxas:
        moeda_origem = moeda_origem_entry.get().upper()
        valor = valor_entry.get()
        moedas_destino = moedas_destino_entry.get().upper().split(',')
        
        try:
            valor = float(valor)
            if moeda_origem in taxas:
                taxa_origem = taxas[moeda_origem]
                resultados = []
                for moeda_destino in moedas_destino:
                    moeda_destino = moeda_destino.strip()  # Remove espaços em branco
                    if moeda_destino in taxas:
                        taxa_destino = taxas[moeda_destino]
                        valor_convertido = converter_moeda(valor / taxa_origem, taxa_destino)
                        resultados.append(f'{valor} {moeda_origem} é igual a {valor_convertido:.2f} {moeda_destino}')
                    else:
                        resultados.append(f"A moeda {moeda_destino} não é válida.")
                
                # Exibir resultados em uma caixa de mensagem
                messagebox.showinfo("Resultados", "\n".join(resultados))
                
                # Salvar resultados em um arquivo
                salvar_resultados(resultados)
            else:
                messagebox.showerror("Erro", "A moeda de origem não é válida.")
        except ValueError:
            messagebox.showerror("Erro", "Por favor, insira um valor numérico válido para a conversão.")

def salvar_resultados(resultados):
    # Abrir um diálogo para escolher o local e nome do arquivo
    arquivo = filedialog.asksaveasfilename(defaultextension=".txt", 
                                             filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if arquivo:
        with open(arquivo, 'w') as f:
            for resultado in resultados:
                f.write(resultado + '\n')
        messagebox.showinfo("Sucesso", "Resultados salvos com sucesso!")

# Criar a janela principal
root = tk.Tk()
root.title("Conversor de Moedas")
root.geometry("400x300")  # Define o tamanho da janela
root.configure(bg="#f0f0f0")  # Cor de fundo

# Adicionar o menu
menu_bar = tk.Menu(root)

# Criar um menu "Arquivo"
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Salvar Resultados", command=lambda: salvar_resultados([]))  # Placeholder
file_menu.add_command(label="Sair", command=root.quit)
menu_bar.add_cascade(label="Arquivo", menu=file_menu)

# Configurar a barra de menu
root.config(menu=menu_bar)

# Criar os widgets
moeda_origem_label = tk.Label(root, text="Moeda de Origem (ex: USD):", bg="#f0f0f0")
moeda_origem_label.pack(pady=5)
moeda_origem_entry = tk.Entry(root)
moeda_origem_entry.pack(pady=5)

valor_label = tk.Label(root, text="Valor a ser convertido:", bg="#f0f0f0")
valor_label.pack(pady=5)
valor_entry = tk.Entry(root)
valor_entry.pack(pady=5)

moedas_destino_label = tk.Label(root, text="Moedas de Destino (ex: EUR, GBP):", bg="#f0f0f0")
moedas_destino_label.pack(pady=5)
moedas_destino_entry = tk.Entry(root)
moedas_destino_entry.pack(pady=5)

converter_button = tk.Button(root, text="Converter", command=converter, bg="#4CAF50", fg="white")
converter_button.pack(pady=20)

# Iniciar o loop da interface gráfica
root.mainloop()