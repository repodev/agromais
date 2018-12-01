from flask import Flask

app = Flask(__name__)
#Chamada da class de configuração

app.config.from_object('config.ConfigDev')
UPLOAD_FOLDER = 'upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
from app.controllers import default
