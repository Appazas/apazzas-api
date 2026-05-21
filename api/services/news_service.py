from api.news import obter_noticias_bahia
from ai.ai import classificador_padrao

class NewsService:
    @staticmethod
    def get_catastrofes() -> list:

        noticias = obter_noticias_bahia()
        
        resultados = []

        for noticia in noticias:
            texto_alvo = noticia.get("texto_para_classificacao", "")
            
            if not texto_alvo.strip() or " - [Removed]" in texto_alvo:
                continue
            
            classificacao = classificador_padrao.classificar(texto_alvo)

            if not classificacao:
                continue

            label, confianca, locais = classificacao
            
            resultados.append({
                "noticia": {
                    "texto": noticia.get("texto"),
                    "url": noticia.get("url"),
                    "data_publicacao": noticia.get("data_publicacao")
                },
                "analise_ia": {
                    "classificação": label,
                    "confiança": confianca,
                    "locais": locais
                }
            })
            
        return resultados