from flask import Blueprint, jsonify
from api.services.news_service import NewsService
import traceback

news_controller = Blueprint('news_controller', __name__)

@news_controller.route('/classificar', methods=['GET'])
def get_noticias():
    try:
        resultados = NewsService.get_catastrofes()
        
        return jsonify({
            "status": "sucesso",
            "total_processado": len(resultados),
            "resultados": resultados
        }), 200
        
    except ValueError as ve:
        return jsonify({"status": "erro", "mensagem": str(ve)}), 500
        
    except Exception as e:
        print(traceback.format_exc())
        return jsonify({"status": "erro", "mensagem": "Erro interno ao processar as notícias."}), 500