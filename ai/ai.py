import joblib
import os
from bs4 import BeautifulSoup

BAIRROS_SALVADOR = [
    "Comércio", "Pelourinho", "Nazaré", "Barris", "Tororó",
    "Campo Grande", "Dois de Julho", "Cidade Alta", "Cidade Baixa",
    "Barra", "Ondina", "Rio Vermelho", "Amaralina", "Pituba",
    "Costa Azul", "Armação", "Boca do Rio", "Patamares",
    "Piatã", "Stella Maris", "Itapuã", "Ipitanga",
    "Brotas", "Federação", "Graça", "Canela", "Vale do Canela",
    "Engenho Velho", "Cabula", "Tancredo Neves", "Sussuarana",
    "Pau da Lima", "São Marcos", "Castelo Branco", "Cajazeiras",
    "Pernambués", "Imbuí", "Itaigara", "Caminho das Árvores",
    "Subúrbio", "Periperi", "Paripe", "Plataforma", "Lobato",
    "São Caetano", "Mussurunga", "Pero Vaz", "Liberdade",
    "Nordeste de Amaralina", "Santa Cruz", "Cosme de Farias",
    "Bonocô", "Retiro", "Pau Miúdo", "Baixa de Quintas",
    "Fazenda Grande", "Alto do Cabrito", "Valéria"
]

REGIOES_BAHIA = [
    "Recôncavo", "Litoral Norte", "Litoral Sul",
    "Chapada Diamantina", "Sertão", "Feira de Santana",
    "Ilhéus", "Camaçari", "Vitória da Conquista",
    "Lauro de Freitas", "Itabuna", "Porto Seguro",
    "Juazeiro", "Barreiras"
]

class ClassificadorDesastres:
    def __init__(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))

        self.vectorizer = joblib.load(
            os.path.join(base_dir, "vectorizer_desastres.pkl")
        )
        self.modelo = joblib.load(
            os.path.join(base_dir, "modelo_desastres.pkl")
        )

    def _extrair_locais(self, titulo: str) -> list:
        encontrados = []
        titulo_lower = titulo.lower()
        
        for bairro in BAIRROS_SALVADOR:
            if bairro.lower() in titulo_lower:
                encontrados.append(bairro)
                
        for regiao in REGIOES_BAHIA:
            if regiao.lower() in titulo_lower:
                encontrados.append(regiao)
                
        if not encontrados:
            if "salvador" in titulo_lower:
                return ["Salvador (sem bairro)"]
            elif "bahia" in titulo_lower:
                return ["Bahia (geral)"]
            return ["não identificado"]
            
        return encontrados

    def classificar(self, texto: str, threshold: float = 0.50) -> tuple:
        vec = self.vectorizer.transform([texto])
        pred = self.modelo.predict(vec)[0]
        prob = self.modelo.predict_proba(vec)[0]
        confianca = float(max(prob))
        
        locais = self._extrair_locais(texto)  

        label = None

        if (confianca >= threshold) and (pred == 1):
            label = "DESASTRE"
            return label, confianca, locais
        else:
            return

classificador_padrao = ClassificadorDesastres()

if __name__ == '__main__':
    exemplos = [
        "Alagamento destrói casas em Brotas",
        "Deslizamento deixa famílias ilhadas no Subúrbio e Periperi",
        "Chuva forte causa estragos em Pau da Lima e Cajazeiras",
        "Carnaval de Salvador bate recorde de turistas", 
    ]

    for texto in exemplos:
        classificacao, confianca, locais = classificador_padrao.classificar(texto)
        
        if classificacao == "DESASTRE":
            print(f"[{classificacao}] ({confianca:.4f})")
            print(f"  Texto:  {texto}")
            print(f"  Locais: {locais}")
            print()