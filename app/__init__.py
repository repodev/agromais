from flask import Flask

app = Flask(__name__)
#Chamada da class de configuração

app.config.from_object('config.ConfigDev')

from app.controllers import default
