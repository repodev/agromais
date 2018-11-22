from flask import render_template,request,abort,redirect,url_for,session
from app import app
#importação relativa do package, ele faz a pesquisa dentro do pacote atual, e não no pacote global
from .class_teste import *
from app.models.tables import inserir_perfil,verifica_cadastro,inserir_perfil_produtor
import hashlib

@app.route("/")
def index():
    logado=None
    cod=[1,2,3,4,5,6,7,8]

    if('username' in session):
        logado = session['username']


    return render_template('index.html',cods=cod,logado=logado, footer=True)

@app.route("/registro/")
def registro():
    return render_template('registrar.html', footer=True)



@app.route("/login/",methods=['GET','POST'])
def login():
    erro = None
    if(request.method == 'POST'):
        perfil = Perfil()
        perfil.setEmail(request.form['email'])
        perfil.setSenha(request.form['senha'])

        logi=verifica_cadastro(perfil.getEmail(),perfil.getSenha())
        if(logi):
            session['username'] = request.form['email'] #session global
            return redirect(url_for('index'))
        else:
            erro='Email ou senha incorretos, tente novamente!!'         
    
    return render_template('login.html', error=erro)

@app.route("/logout")
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

@app.route("/recuperar")
def recuperar_conta():
    return render_template('recuperarsenha.html')

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

        check=request.form.get('check_loja',False)

        if(not check):
            perfil = Perfil(request.form['nome'],request.form['sobrenome'],request.form['contato'],request.form['cidades'],request.form['bairro'],request.form['endereco'],request.form['cpf'],request.form['email'],request.form['senha'])
            
            resposta=inserir_perfil(perfil.getNome(),perfil.getSobrenome(),perfil.getContato(),perfil.getCidades(),perfil.getBairro(),perfil.getEndereco(),perfil.getCpf(),perfil.getEmail(),perfil.getSenha())
            if (resposta1):
               return 'Perfil inserido'
            else:
               return'Perfil não inserido'
        else:
            perfil_produtor = Perfil_produtor(request.form['nome'],request.form['sobrenome'],request.form['contato'],request.form['cidades'],request.form['bairro'],request.form['endereco'],request.form['cpf'],request.form['email'],request.form['senha'],request.form['nome_loja'],request.form['contato_loja'],request.form['endereco_loja'])
            resposta1=inserir_perfil_produtor(perfil_produtor.getNome_loja(),perfil_produtor.getContato_comercial(),perfil_produtor.getEndereco_comercial(),'lucas@lucas.com')
            if (resposta1):
                return 'Perfil produtor inserido'
            else:
                return'Perfil produtor não inserido'



@app.errorhandler(404)
def page_not_found(error):
    return "<h1 style=text-align:center;>Estamos esperando a chuva!</h1>", 404