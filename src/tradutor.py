import requests
import uuid
from bs4 import BeautifulSoup

SUBSCRIPTION_KEY = "SUA_CHAVE_AQUI"
ENDPOINT = "https://api.cognitive.microsofttranslator.com"
LOCATION = "eastus"

def traduzir_texto(texto, sub_key, endpoint, location):
    path = '/translate'
    constructed_url = f"{endpoint}{path}"
    
    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': ['pt-br']
    }

    headers = {
        'Ocp-Apim-Subscription-Key': sub_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': texto}]
    
    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    
    if response.status_code == 200:
        return response.json()[0]['translations'][0]['text']
    else:
        return f"[Erro na tradução: {response.status_code}]"

def extrair_e_traduzir_site(url_site):
    print(f"Acessando o artigo em: {url_site}...")
    
    headers_web = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(url_site, headers=headers_web)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        artigo = soup.find('article')
        if not artigo:
            artigo = soup
            
        paragrafos = artigo.find_all(['p', 'h1', 'h2', 'h3'])
        
        print(f"Traduzindo conteúdo técnico com Azure AI...")
        
        resultado_final = []
        
        for p in paragrafos:
            texto_original = p.get_text().strip()
            
            if len(texto_original) > 5:
                traducao = traduzir_texto(texto_original, SUBSCRIPTION_KEY, ENDPOINT, LOCATION)
                resultado_final.append(traducao)
                print(f"Trecho traduzido ({len(texto_original)} caracteres)")

        # Salvando o resultado
        with open("artigo_web_traduzido.txt", "w", encoding="utf-8") as f:
            f.write("\n\n".join(resultado_final))
            
        print("\n" + "="*30)
        print("Arquivo gerado: artigo_web_traduzido.txt")
        print("="*30)

    except Exception as e:
        print(f"❌ Erro ao processar o site: {e}")

if __name__ == "__main__":
    url_do_artigo = "https://dev.to/chronosquant/python-multi-currency-quantitative-strategy-framework-design-concepts-and-implementation-details-53eo"

    extrair_e_traduzir_site(url_do_artigo)
