from flask import Flask
from dotenv import load_dotenv

from api.controllers.news_controller import news_controller

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(news_controller)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)