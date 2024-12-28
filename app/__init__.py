from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy()

# Configurações do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user123:user123@localhost:5433/auth_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar a extensão
db.init_app(app)

# Importar rotas (faça isso após a inicialização do app e db)
from app import routes