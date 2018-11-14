from flask import render_template,request
from app import app

@app.route("/registro/")
def index():
	return render_template('registrar.html')

@app.route("/verifica_registro",methods=['GET','POST'])
def verifica():
	if(request.method == 'POST'):
		nome = request.form['nome']
		sobrenome = request.form['sobrenome']

