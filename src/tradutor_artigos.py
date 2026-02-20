import requests
import uuid

SUBSCRIPTION_KEY = "SUA_CHAVE_AQUI"
ENDPOINT = "https://api.cognitive.microsofttranslator.com/"
LOCATION = "eastus"

def traduzir_artigo(texto_ingles):
    path = '/translate'
    constructed_url = f"{ENDPOINT}{path}"

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': ['pt-br']
    }

    headers = {
        'Ocp-Apim-Subscription-Key': SUBSCRIPTION_KEY,
        'Ocp-Apim-Subscription-Region': LOCATION,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': texto_ingles
    }]

    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    
    if response.status_code == 200:
        resultado = response.json()
        return resultado[0]['translations'][0]['text']
    else:
        return f"Erro: {response.status_code} - {response.text}"

if __name__ == "__main__":
    artigo_original = """
    In the strategy initialization phase, we first define global variables SYMBOLS, QUOTO, 
    and INTERVAL. This framework features a Python-based language and supports 
    multi-currency concurrent trading.
    """
    
    print("Iniciando tradução")
    
    traducao = traduzir_artigo(artigo_original)
    
    print("\n--- Resultado da Tradução ---")
    print(traducao)
    
    with open("artigo_traduzido.txt", "w", encoding="utf-8") as f:
        f.write(traducao)

        print("\n Arquivo 'artigo_traduzido.txt' foi gerado")
