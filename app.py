from flask import Flask, render_template, request, redirect, url_for, flash
import requests

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para usar flash messages

def obter_taxas_de_cambio():
    url = 'https://open.er-api.com/v6/latest/USD'  # Você pode mudar a moeda base se desejar
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()['rates']
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        moeda_origem = request.form['moeda_origem'].upper()
        valor = request.form['valor']
        moedas_destino = request.form['moedas_destino'].upper().split(',')
        
        try:
            valor = float(valor)
            taxas = obter_taxas_de_cambio()
            if taxas and moeda_origem in taxas:
                taxa_origem = taxas[moeda_origem]
                resultados = []
                for moeda_destino in moedas_destino:
                    moeda_destino = moeda_destino.strip()
                    if moeda_destino in taxas:
                        taxa_destino = taxas[moeda_destino]
                        valor_convertido = valor / taxa_origem * taxa_destino
                        resultados.append(f'{valor} {moeda_origem} é igual a {valor_convertido:.2f} {moeda_destino}')
                    else:
                        resultados.append(f"A moeda {moeda_destino} não é válida.")
                return render_template('index.html', resultados=resultados)
            else:
                flash("A moeda de origem não é válida.")
        except ValueError:
            flash("Por favor, insira um valor numérico válido para a conversão.")
    
    return render_template('index.html', resultados=None)

if __name__ == '__main__':
    app.run(debug=True)