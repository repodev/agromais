from flask import render_template,request
from app import app
#importação relativa do package, ele faz a pesquisa dentro do pacote atual, e não no pacote global
from .class_teste import *

@app.route("/registro/")
def index():
	return render_template('registrar.html')

@app.route("/verifica_registro",methods=['GET','POST'])
def verifica():
	if(request.method == 'POST'):
		perfil = Perfil()
		perfil.setNome = request.form['nome']
		perfil.setSobrenome = request.form['sobrenome']
		return 'teste'