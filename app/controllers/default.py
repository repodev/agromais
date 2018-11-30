from flask import render_template,request,abort,redirect,url_for,session,flash,jsonify
from app import app
#importação relativa do package, ele faz a pesquisa dentro do pacote atual, e não no pacote global
from .class_teste import *
from app.models.tables import inserir_perfil,verifica_cadastro,inserir_perfil_produtor
import hashlib

@app.route("/")
def index():
    logado=None
    cod=[1,2,3,4,5,6,7,8]

    if('tipo_conta' in session):
        logado = session['tipo_conta']
    return render_template('index.html',cods=cod,logado=logado, footer=True)

@app.route("/registro/",methods=['GET','POST'])
def registro():
    erro = None
    return render_template('registrar.html', footer=True,error=erro)



@app.route("/valida_registro",methods=['GET','POST'])
def valida_registro():
    erro = None
    if(request.method == 'POST'):
        check=request.form.get('check_loja',False)

        if(not check):

            perfil = PerfilComprador(request.form['nome'],request.form['sobrenome'],request.form['contato'],request.form['cidade'],request.form['bairro'],request.form['endereco'],request.form['cpf'],request.form['email'],request.form['senha'])
            
            resposta=inserir_perfil(perfil.getNome(),perfil.getSobrenome(),perfil.getContato(),perfil.getCidade(),perfil.getBairro(),perfil.getEndereco(),perfil.getCpf(),perfil.getEmail(),perfil.getSenha())
            
            print(resposta)

            if (resposta=='Duplicado'):
                erro = "Já existe um perfil com essas informações! verifique os campos (email,cpf)"
                return jsonify({'status':'2','erro':erro})

            elif (resposta=='Aceito'):
                flash('Cadastro realizado com sucesso.')
                url = "/"
                return jsonify({'status':'1','url':url})
            else:

                erro = "Erro ao Cadastrar seu perfil, por favor tente novamente."
                return jsonify([{'status':'NO'},{'erro':erro}])
        else:
            perfil_produtor = PerfilProdutor(request.form['nome'],request.form['sobrenome'],request.form['contato'],request.form['cidade'],request.form['bairro'],request.form['endereco'],request.form['cpf'],request.form['email'],request.form['senha'],request.form['nome_loja'],request.form['contato_comercial'],request.form['endereco_loja'],request.form['descricao_loja'])
            
            resposta_perfil=inserir_perfil(perfil_produtor.getNome(),perfil_produtor.getSobrenome(),perfil_produtor.getContato(),perfil_produtor.getCidade(),perfil_produtor.getBairro(),perfil_produtor.getEndereco(),perfil_produtor.getCpf(),perfil_produtor.getEmail(),perfil_produtor.getSenha())
            
            

            if (resposta_perfil == 'Aceito'):
                inserir_perfil_produtor(perfil_produtor.getNome_loja(),perfil_produtor.getContato_comercial(),perfil_produtor.getEndereco_comercial(),perfil_produtor.getDescricao_loja(),perfil_produtor.getEmail())    
                flash('Cadastro realizado com sucesso.')
                url = "/"
                return jsonify({'status':'1','url':url})
            elif(resposta_perfil == 'Duplicado' ):
                erro = "Já existe um perfil com essas informações! verifique os campos (email, cpf, nome loja)"
                return jsonify({'status':'2','erro':erro})
            else:
                erro = "Erro ao inserir o perfil, tente novamente!"
                return jsonify({'status':'2','erro':erro})

@app.route("/login/",methods=['GET','POST'])
def login():
    erro = None
    if(request.method == 'POST'):

        perfil = Login(request.form['email'],request.form['senha'])
        
        resposta = verifica_cadastro(perfil.getEmail(),perfil.getSenha())
        print('------------------',resposta)
        id_produtor = resposta

        #login caso seja comprador
        if(id_produtor == None):
            session['tipo_conta'] = 'comprador' #session global
            flash('Login realizado com sucesso, Vamos as compras?')
            return redirect(url_for('index'))
        
        #login caso seja produtor
        elif(id_produtor != False):
            session['tipo_conta'] = 'produtor' #session global
            flash('Login realizado com sucesso, Vamos vender?')
            return redirect(url_for('index'))

        #Caso aconteça algum erro ou não tenha cadastro  
        else:
            erro='Email ou senha incorretos, tente novamente!!'         
    
    return render_template('login.html', error=erro)



@app.route("/logout")
def logout():
    session.pop('tipo_conta',None)
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


@app.errorhandler(404)
def page_not_found(error):
    return "<h1 style=text-align:center;>Estamos esperando a chuva!</h1>", 404