import os
import requests
from datetime import datetime, timedelta

def obter_noticias_bahia():
    api_key = os.environ.get("NEWSAPI_KEY")
    if not api_key:
        raise ValueError("A chave de API NEWSAPI_KEY não está configurada no ambiente.")

    data_inicio = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
    
    url = "https://newsapi.org/v2/everything"
    
    parametros = {
        "q": "Bahia AND (chuvas OR desastre OR alagamento OR enchente OR deslizamento)",
        "language": "pt",
        "from": data_inicio,
        "sortBy": "publishedAt",
        "apiKey": api_key,
        "pageSize": 100
    }

    resposta = requests.get(url, params=parametros)
    
    if resposta.status_code != 200:
        raise Exception(f"Erro na NewsAPI: {resposta.text}")

    dados = resposta.json()
    artigos_processados = []

    for artigo in dados.get("articles", []):
        titulo = artigo.get('title', '')
        descricao = artigo.get('description', '') or ''
        texto_completo = f"{titulo} - {descricao}"
        
        artigos_processados.append({
            "texto": texto_completo,
            "url": artigo.get("url"),
            "data_publicacao": artigo.get("publishedAt"),
            "texto_para_classificacao": texto_completo
        })

    return artigos_processados

if __name__ == "__main__":
    from dotenv import load_dotenv
    
    load_dotenv()
    
    try:
        resultados = obter_noticias_bahia()
        
        if resultados:
            print("\nA mostrar os detalhes das 3 primeiras notícias:")
            for i, noticia in enumerate(resultados[:3], 1):
                print(f"\n--- Notícia {i} ---")
                print(f"Título: {noticia['titulo']}")
                print(f"Data: {noticia['data_publicacao']}")
                texto_ia = noticia['texto_para_classificacao']
                print(f"Texto para a IA: {texto_ia[:100]}..." if len(texto_ia) > 100 else f"Texto para a IA: {texto_ia}")
                print(f"URL: {noticia['url']}")
                
    except Exception as e:
        print(f"\n[ERRO DURANTE O TESTE]: {e}")
        print("Verifique se a sua chave 'NEWSAPI_KEY' está correta no ficheiro .env.")