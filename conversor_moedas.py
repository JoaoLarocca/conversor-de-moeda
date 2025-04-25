import requests

def get_cotacao(moeda_destino):
    """Obtém a cotação da moeda em relação ao BRL."""
    try:
        url = f"https://api.exchangerate.host/latest?base=BRL&symbols={moeda_destino.upper()}"
        response = requests.get(url)
        response.raise_for_status()
        dados = response.json()
        return dados["rates"][moeda_destino.upper()]
    except Exception as e:
        print("Erro ao buscar cotação:", e)
        return None

def converter(valor, taxa):
    """Converte o valor com base na taxa."""
    return valor * taxa

def main():
    print("=== Conversor de Moedas ===")
    try:
        valor = float(input("Digite o valor em reais (BRL): "))
        moeda = input("Digite a moeda de destino (ex: USD, EUR): ").strip().upper()

        taxa = get_cotacao(moeda)
        if taxa:
            resultado = converter(valor, taxa)
            print(f"\n💱 R$ {valor:.2f} = {resultado:.2f} {moeda}")
        else:
            print("Não foi possível realizar a conversão.")

    except ValueError:
        print("Valor inválido. Por favor, digite um número.")

if __name__ == "__main__":
    main()
