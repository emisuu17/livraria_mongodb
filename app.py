from flask import Flask

# 1. Cria a aplicação Flask
app = Flask(__name__)

# 2. configura a chave secreta 
app.config['SECRET_KEY'] = 'uma_chave_secreta_aqui'

# 3. importa as rotas DEPOIS de criar o app
from routes import *

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')