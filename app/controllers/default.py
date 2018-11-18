from flask import render_template,request,abort
from app import app
#importação relativa do package, ele faz a pesquisa dentro do pacote atual, e não no pacote global
from .class_teste import *
from app.models.tables import inserir_perfil

@app.route("/")
def index():
	cod=[1,2,3,4,5,6,7,8]
	return render_template('index.html',cods=cod)

@app.route("/registro/")
def registro():
	return render_template('registrar.html')

@app.route("/login/")
def login():
	return render_template('login.html')


@app.route("/perfil/<int:produtor_id>/")
def perfil(produtor_id):
	if produtor_id in [1,2,3,4,5,6,7,8]:
		return render_template('produtor.html', id=produtor_id)
	else:
		return "Este produtor não existe"


@app.route("/sobre/")
def sobre():
	return render_template('start.html')

@app.route("/verifica_registro",methods=['GET','POST'])
def verifica():
	if(request.method == 'POST'):
		perfil = Perfil()
		perfil.setNome (request.form['nome'])
		perfil.setSobrenome (request.form['sobrenome'])
		perfil.setContato(request.form['contato'])
		perfil.setCidades(request.form['cidades'])
		perfil.setBairro(request.form['bairro'])
		perfil.setEndereco(request.form['endereco'])
		perfil.setCpf(request.form['cpf'])
		perfil.setEmail(request.form['email'])
		perfil.setSenha(request.form['senha'])
		
		resposta=inserir_perfil(perfil.getNome(),perfil.getSobrenome(),perfil.getContato(),perfil.getCidades(),perfil.getBairro(),perfil.getEndereco(),perfil.getCpf(),perfil.getEmail(),perfil.getSenha())
		return resposta







@app.errorhandler(404)
def page_not_found(error):
    return "<h1 style=text-align:center;>Estamos esperando a chuva!</h1>", 404