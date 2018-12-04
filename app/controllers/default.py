from flask import render_template,request,abort,redirect,url_for,session,flash,jsonify
from app import app

#importação relativa do package, ele faz a pesquisa dentro do pacote atual, e não no pacote global
from .class_teste import *

from app.models.tables import inserir_perfil,verifica_cadastro,inserir_perfil_produtor,recupera_id,inserir_produto,recupera_produtos,gera_nome_imagem,salva_imagem,lista_categorias,recupera_produtos_categoria,recupera_um_produto

@app.route("/")
def index():

    logado=None
    if(lista_categorias()):
        categorias=lista_categorias()
    else:
        categorias = None
    if(request.args.get("categoria")):
        id_categoria=request.args.get("categoria")
        produtos=recupera_produtos_categoria(int(id_categoria))

    elif(recupera_produtos()):
        produtos=recupera_produtos()
    else:
        produtos = None
    

    if('tipo_conta' in session):
        logado = session['tipo_conta']
    return render_template('index.html',categorias=categorias,produtos=produtos,logado=logado, footer=True)


@app.route("/registro/",methods=['GET','POST'])
def registro():
    erro = None
    if('tipo_conta' in session):
        return abort(404)
    else:
        return render_template('registrar.html', footer=True,error=erro)


@app.route("/registra_produto/")
def registra_produto():
    logado=None
    #variavel para ocultar botão (mais) na pagina do cadastro do produto
    b_cadastrar = None
    if(lista_categorias()):
        categorias=lista_categorias()
    else:
        categorias = None
    if('id_produtor' in session):
        if('tipo_conta' in session):
            logado = session['tipo_conta']
        return render_template('registrarproduto.html', categorias=categorias, footer=True,logado=logado, ocultar = b_cadastrar)
    else:
        return abort(404)


@app.route("/produto/<int:id_produto>/")
def produto(id_produto):
    logado=None
    b_cadastrar = None
    if(recupera_um_produto(id_produto)):
        info_produto = recupera_um_produto(id_produto)
    if('tipo_conta' in session):
        logado = session['tipo_conta']

    return render_template('produto.html',footer=False,logado=logado,ocultar = b_cadastrar, produto=info_produto)


@app.route("/valida_compra")
def valida_compra():
    session['id_produto']=id_produto

    if(session['id_perfil']):
        pass
    else:
        return redirect (url_for('login'))

@app.route("/valida_produto", methods=['GET','POST'])
def valida_produto():
    b_cadastrar = None
    erro=None
    print("-----------",session['id_produtor'])
    if(request.method == 'POST'):
        FLAG = "foto_produto"
        logado = session['tipo_conta']
        id_produtor = session['id_produtor']
        imagem_produto = gera_nome_imagem(FLAG)

        produto = Produto(request.form['nome'],request.form['categoria'],request.form['subcategoria'],request.form['preco'],request.form['estoque'],imagem_produto,request.form['descricao_produto'],id_produtor)
        
        resposta = inserir_produto(produto.getNome_produto(),produto.getCategoria(),produto.getSubcategoria(),produto.getPreco(),produto.getEstoque(),produto.getFotoProduto(),produto.getDescricao_produto(),produto.getIdProdutor())
        if (resposta=='Duplicado'):
            erro = "Já existe um produto com essas informações!"
            return jsonify({'status':'2','erro':erro})

        elif (resposta=='Aceito'):
            salva_imagem(FLAG,imagem_produto)
            flash('Produto cadastrado com sucesso.')
            url = "/"
            return jsonify({'status':'1','url':url})

        else:
            erro = "Erro ao Cadastrar seu produto, por favor tente novamente."
            return jsonify([{'status':'NO'},{'erro':erro}])
    return render_template('registrarproduto.html', footer=True,logado=logado, ocultar = b_cadastrar)


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
            FLAG = "foto_loja"                
            
            #gera nome, na gambiarra
            imagem = gera_nome_imagem(FLAG)            
            
            perfil_produtor = PerfilProdutor(request.form['nome'],request.form['sobrenome'],request.form['contato'],request.form['cidade'],request.form['bairro'],request.form['endereco'],request.form['cpf'],request.form['email'],request.form['senha'],request.form['nome_loja'],request.form['cnpj'],request.form['contato_comercial'],request.form['endereco_loja'],request.form['descricao_loja'],imagem)
            
            resposta_perfil_produtor=inserir_perfil_produtor(perfil_produtor.getNome(),perfil_produtor.getSobrenome(),perfil_produtor.getContato(),perfil_produtor.getCidade(),perfil_produtor.getBairro(),perfil_produtor.getEndereco(),perfil_produtor.getCpf(),perfil_produtor.getEmail(),perfil_produtor.getSenha(),perfil_produtor.getNome_loja(),perfil_produtor.getCnpj(),perfil_produtor.getContato_comercial(),perfil_produtor.getEndereco_comercial(),perfil_produtor.getDescricao_loja(),perfil_produtor.getFoto())
            
            if (resposta_perfil_produtor == 'Aceito'):
                #evita que a imagem fique sendo salva, caso o formulario apresente erro no envio, salva apenas se o cadastro for aceito
                salva_imagem(FLAG,imagem)
                flash('Cadastro realizado com sucesso.')
                url = "/"
                return jsonify({'status':'1','url':url})
            elif(resposta_perfil_produtor == 'Duplicado' ):
                erro = "Já existe um perfil com essas informações! verifique os campos (email, cpf, nome loja)"
                return jsonify({'status':'2','erro':erro})
            else:
                erro = "Erro ao inserir o perfil, tente novamente!"
                return jsonify({'status':'2','erro':erro})


@app.route("/login/",methods=['GET','POST'])
def login():
    erro = None
    if('tipo_conta' in session):
        return abort(404)
    else:    
        if(request.method == 'POST'):

            perfil = Login(request.form['email'],request.form['senha'])
            
            id_produtor = verifica_cadastro(perfil.getEmail(),perfil.getSenha())

            #login caso seja comprador
            if(id_produtor == None):
                session['tipo_conta'] = 'comprador' #session global <<<-- Tirar depois
                session['id_perfil'] = recupera_id(request.form['email'])
                flash('Login realizado com sucesso, Vamos as compras?')
                return redirect(url_for('index'))
            
            #login caso seja produtor
            elif(id_produtor != False):
                session['tipo_conta'] = 'produtor' #session global <<<-- Tirar depois
                session['id_perfil'] = recupera_id(request.form['email']) 
                session['id_produtor'] = id_produtor
                flash('Login realizado com sucesso, Vamos vender?')
                return redirect(url_for('index'))

            #Caso aconteça algum erro ou não tenha cadastro  
            else:
                erro='Email ou senha incorretos, tente novamente!!'         
        
        return render_template('login.html', error=erro)



@app.route("/logout")
def logout():
    session.pop('tipo_conta',None)
    session.pop('id_produtor',None)
    session.pop('id_perfil',None)
    return redirect(url_for('index'))


@app.route("/recuperar")
def recuperar_conta():
    return render_template('recuperarsenha.html')


@app.route("/perfil/<int:produtor_id>/")
def perfil(produtor_id):
    logado = None
    if('tipo_conta' in session):
        logado = session['tipo_conta']
    if produtor_id in [1,2,3,4,5,6,7,8]:
        return render_template('produtor.html', id=produtor_id, logado=logado)
    else:
        return "Este produtor não existe"


@app.route("/sobre/")
def sobre():
    return render_template('start.html')


@app.errorhandler(404)
def page_not_found(error):
    return "<h1 style=text-align:center;>Estamos esperando a chuva!</h1>", 404