from flask import Flask

app = Flask(__name__)
#Chamada da class de configuração

app.config.from_object('config.ConfigDev')
UPLOAD_FOLDER_PRODUCTS = 'app/static/upload/produtos'
UPLOAD_FOLDER_SELLER = 'app/static/upload/produtores'
app.config['PASTA_PRODUTOS'] = UPLOAD_FOLDER_PRODUCTS
app.config['PASTA_PRODUTORES'] = UPLOAD_FOLDER_SELLER
from app.controllers import default
