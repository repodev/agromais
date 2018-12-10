from flask import render_template,request,abort,redirect,url_for,session,flash,jsonify
from app import app

#importação relativa do package, ele faz a pesquisa dentro do pacote atual, e não no pacote global
from .class_Pedido import *
from .class_Login import *
from .class_PerfilComprador import *
from .class_Errors import *
from .class_Produto import *
from .class_PerfilProdutor import *

from app.models.tables import inserir_perfil,verifica_cadastro,inserir_perfil_produtor,recupera_id,inserir_produto,recupera_produtos,gera_nome_imagem,salva_imagem,lista_categorias,recupera_produtos_categoria,recupera_um_produto,perfil_produtor_publico,perfil_produtor_produtos,registra_pedido,recupera_pedidos,recupera_vendas,atualiza_status_produto,recupera_meu_perfil,pesquisa_produto,recupera_pedidos_pendentes,muda_status_pedido, atualiza_produto,recupera_produto_edicao

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
        
    elif(request.args.get("s")):
        consulta=request.args.get("s")
    
        produtos=pesquisa_produto(consulta.upper())

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

@app.route("/edita_produto/<int:id_produto>/")
def edita_produto(id_produto):
   
    logado=None
    #variavel para ocultar botão (mais) na pagina do cadastro do produto
    b_cadastrar = None
    produto =None
    if(recupera_produto_edicao(id_produto)):
        produto = recupera_produto_edicao(id_produto)
        print(float(produto[4]))
    
    if(lista_categorias()):
        categorias=lista_categorias()
    else:
        categorias = None
  
  

    if('id_produtor' in session):
        if('tipo_conta' in session):
            logado = session['tipo_conta']
        return render_template('editaproduto.html', categorias=categorias,produto=produto, footer=True,logado=logado, ocultar = b_cadastrar)
    else:
        return abort(404)

@app.route("/confirma_edicao_produto", methods=['GET','POST'])
def confirma_edicao_produto():

    erro=None
    print("-----------",session['id_produtor'])
    if(request.method == 'POST'):
        FLAG = "foto_produto"
        logado = session['tipo_conta']
        id_produtor = session['id_produtor']
        imagem_produto = gera_nome_imagem(FLAG)

        produto = Produto(request.form['nome'],request.form['categoria'],request.form['subcategoria'],request.form['preco'],request.form['estoque'],imagem_produto,request.form['descricao_produto'],id_produtor)
        
        resposta = atualiza_produto(produto.getNome_produto(),produto.getCategoria(),produto.getSubcategoria(),produto.getPreco(),produto.getEstoque(),produto.getFoto_produto(),produto.getDescricao_produto(),produto.getId_produtor(),request.form('id_produto'))
        erro = ErrorAtualizaProduto()

        if (resposta=='Aceito'):
            salva_imagem(FLAG,imagem_produto)
            flash('Produto cadastrado com sucesso.')
            url = "/meus_produtos"
            return jsonify({'status':'1','url':url})

        else:
            return jsonify([{'status':'NO'},{'erro':erro.reg_desconhecido()}])
    return abort(404)









@app.route("/produto/<int:id_produto>/")
def produto(id_produto):
    logado=None
    b_cadastrar = None
    info_produto = None
    if(recupera_um_produto(id_produto)):
        info_produto = recupera_um_produto(id_produto)
    if('tipo_conta' in session):
        logado = session['tipo_conta']

    return render_template('produto.html',footer=False,logado=logado,ocultar = b_cadastrar, produto=info_produto)

@app.route("/historico_pedidos")
def historico_pedidos():
    logado=None
    pedidos = None
    if('tipo_conta' in session):
        logado = session['tipo_conta']
        id_perfil = session['id_perfil']        
        if(recupera_pedidos(id_perfil)):
            pedidos = recupera_pedidos(id_perfil)
    return render_template('historico_pedidos.html',footer=False,logado=logado,pedidos=pedidos,ocultar = None)

@app.route("/vendas", methods=['GET', 'POST'])
def vendas():
    logado=None
    vendas = None
    pedidos_pendentes= None
    if('id_produtor' in session):
        logado = session['tipo_conta']
        id_produtor = session['id_produtor']        
        if(recupera_vendas(id_produtor)):
            vendas = recupera_vendas(id_produtor)
        if(recupera_pedidos_pendentes(id_produtor)):
            pedidos_pendentes = recupera_pedidos_pendentes(id_produtor)

    if(request.method == 'POST'):
            id_pedido = request.form['id_pedido']
            
            if('aceitar' in request.form):
                muda_status_pedido('aceitar', id_produtor, id_pedido,False)
                print(id_produtor,id_pedido)
                flash("Pedido aceito com sucesso!!!")
                return redirect(url_for('vendas'))            
            else:
                qtd = request.form['quantidade']
                muda_status_pedido('negado', id_produtor, id_pedido,qtd)
                print(id_produtor,id_pedido)
                flash("Pedido negado com sucesso!!!")
                return redirect(url_for('vendas'))
    return render_template('vendas.html',footer=False,logado=logado,vendas=vendas,pedidos=pedidos_pendentes,ocultar = None)

@app.route("/meus_produtos", methods=['GET','POST'])
def meus_produtos():
    logado=None
    produtos= None
    if('id_produtor' in session):
        logado = session['tipo_conta']
        id_produtor = session['id_produtor']
        if(perfil_produtor_produtos(id_produtor,'todos')):
            produtos = perfil_produtor_produtos(id_produtor,'todos')  
        if(request.method == 'POST'):
            id_produto = request.form['id_produto']
            if('desativar' in request.form): 
                atualiza_status_produto('false', id_produto)              
                flash("Produto desativado com sucesso!!!")
                return redirect(url_for('meus_produtos'))            
            else:
                atualiza = atualiza_status_produto('true', id_produto)
                if(atualiza == 0):
                    flash("Este produto não foi ativado, o estoque é igual a 0 !!!")
                    return redirect(url_for('meus_produtos')) 
                flash("Produto ativado com sucesso!!!")
                return redirect(url_for('meus_produtos')) 
                 
   
    return render_template('meus_produtos.html',footer=False,produtos=produtos,logado=logado,ocultar = None)

@app.route("/valida_pedido/<int:id_produto>", methods=['GET','POST'])
def valida_pedido(id_produto):
    if(request.method == 'POST'):
        session['id_produto']=id_produto
        session['id_produtor_pedido']=request.form['id_produtor']
        unidade_b = float(request.form['unidade_b']) #unidade vinda do banco
        unidade_u = float(request.form['unidade']) #unidade vinda do usuario
        novo_preco = (float(request.form['preco'])*unidade_u) 
        if(unidade_b >= unidade_u):        
            
            return jsonify({'status': '1','novo_preco': novo_preco, 'unidade': unidade_u})       
        else:
            erro = "Pedido invalido, unidade invalida!"
            print(novo_preco)
            return jsonify({'status':'2','erro': erro})
            

        #if(session['id_perfil']):
        #    pass
        #else:
        #    return redirect (url_for('login'))

@app.route("/confirma_pedido", methods=['GET','POST'])
def confirma_pedido():
    if(request.method == 'POST'):
        session['unidade_pedido'] = request.form['unidade_pedido']
        session['unidade_valor'] = request.form['unidade_valor']
        

    if('id_perfil' in session):
            pedido = Pedido(session['id_produto'],session['id_perfil'],session['id_produtor_pedido'],session['unidade_pedido'],session['unidade_valor'])
            
            registra_pedido(pedido.getId_produto(),pedido.getId_comprador(),pedido.getId_produtor(),pedido.getQuantidade(),pedido.getValor() )
            session.pop('id_produto',None)
            session.pop('id_produtor_pedido',None)
            session.pop('unidade_pedido',None)
            session.pop('unidade_valor',None)
            
            return redirect(url_for('historico_pedidos'))
    else:
            return redirect(url_for('login'))
    
@app.route("/valida_produto", methods=['GET','POST'])
def valida_produto():
  
    erro=None
    print("-----------",session['id_produtor'])
    if(request.method == 'POST'):
        FLAG = "foto_produto"
        logado = session['tipo_conta']
        id_produtor = session['id_produtor']
        imagem_produto = gera_nome_imagem(FLAG)

        produto = Produto(request.form['nome'],request.form['categoria'],request.form['subcategoria'],request.form['preco'],request.form['estoque'],imagem_produto,request.form['descricao_produto'],id_produtor)
        
        resposta = inserir_produto(produto.getNome_produto(),produto.getCategoria(),produto.getSubcategoria(),produto.getPreco(),produto.getEstoque(),produto.getFoto_produto(),produto.getDescricao_produto(),produto.getId_produtor())
        erro = ErrorCadProduto()

        if (resposta=='Duplicado'):
            return jsonify({'status':'2','erro':erro.reg_duplicado()})

        elif (resposta=='Aceito'):
            salva_imagem(FLAG,imagem_produto)
            flash('Produto cadastrado com sucesso.')
            url = "/"
            return jsonify({'status':'1','url':url})

        else:
            return jsonify([{'status':'NO'},{'erro':erro.reg_desconhecido()}])
    return abort(404)

@app.route("/valida_registro",methods=['GET','POST'])
def valida_registro():
    erro = None
    if(request.method == 'POST'):
        check=request.form.get('check_loja',False)

        if(not check):

            perfil = PerfilComprador(request.form['nome'],request.form['sobrenome'],request.form['contato'],request.form['cidade'],request.form['bairro'],request.form['endereco'],request.form['cpf'],request.form['email'],request.form['senha'])
            
            resposta=inserir_perfil(perfil.getNome(),perfil.getSobrenome(),perfil.getContato(),perfil.getCidade(),perfil.getBairro(),perfil.getEndereco(),perfil.getCpf(),perfil.getEmail(),perfil.getSenha())
            
            print(resposta)

            erro = ErrorCadPerfil()

            if (resposta=='Duplicado'):
                return jsonify({'status':'2','erro':erro.reg_duplicado()})

            elif (resposta=='Aceito'):
                flash('Cadastro realizado com sucesso.')
                url = "/"
                return jsonify({'status':'1','url':url})
            else:
                return jsonify([{'status':'NO'},{'erro':erro.reg_desconhecido()}])
        else:
            FLAG = "foto_loja"                
            
            #gera nome, na gambiarra
            imagem = gera_nome_imagem(FLAG)            
            
            perfil_produtor = PerfilProdutor(request.form['nome'],request.form['sobrenome'],request.form['contato'],request.form['cidade'],request.form['bairro'],request.form['endereco'],request.form['cpf'],request.form['email'],request.form['senha'],request.form['nome_loja'],request.form['cnpj'],request.form['contato_comercial'],request.form['endereco_loja'],request.form['descricao_loja'],imagem)
            
            resposta_perfil_produtor=inserir_perfil_produtor(perfil_produtor.getNome(),perfil_produtor.getSobrenome(),perfil_produtor.getContato(),perfil_produtor.getCidade(),perfil_produtor.getBairro(),perfil_produtor.getEndereco(),perfil_produtor.getCpf(),perfil_produtor.getEmail(),perfil_produtor.getSenha(),perfil_produtor.getNome_loja(),perfil_produtor.getCnpj(),perfil_produtor.getContato_comercial(),perfil_produtor.getEndereco_comercial(),perfil_produtor.getDescricao_loja(),perfil_produtor.getFoto())
            
            erro = ErrorCadPerfilProdutor()

            if (resposta_perfil_produtor == 'Aceito'):
                #evita que a imagem fique sendo salva, caso o formulario apresente erro no envio, salva apenas se o cadastro for aceito
                salva_imagem(FLAG,imagem)
                flash('Cadastro realizado com sucesso.')
                url = "/"
                return jsonify({'status':'1','url':url})
            elif(resposta_perfil_produtor == 'Duplicado' ):
                return jsonify({'status':'2','erro':erro.reg_duplicado()})
            else:
                return jsonify({'status':'2','erro':erro.reg_desconhecido()})


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
                session['tipo_conta'] = 'comprador' #session global 
                session['id_perfil'] = recupera_id(request.form['email'])
                if('unidade_pedido' in session and 'unidade_valor' in session): #verifica se tem pedido na session
                    return redirect(url_for('confirma_pedido'))
                flash('Login realizado com sucesso, Vamos as compras?')
                
                return redirect(url_for('index'))
            
            #login caso seja produtor
            elif(id_produtor != False):
                session['tipo_conta'] = 'produtor' #session global 
                session['id_perfil'] = recupera_id(request.form['email']) 
                session['id_produtor'] = id_produtor
                if('unidade_pedido' in session and 'unidade_valor' in session):
                    return redirect(url_for('confirma_pedido'))
                flash('Login realizado com sucesso, Vamos vender?')
                
                return redirect(url_for('index'))
            
            #Caso aconteça algum erro ou não tenha cadastro  
            else:
                error = ErroCadLogin()
                erro = error.reg_desconhecido()         
        
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
    perfil = None
    produtos =None
    if('tipo_conta' in session):
        logado = session['tipo_conta']
    if(perfil_produtor_publico(produtor_id)):
        perfil = perfil_produtor_publico(produtor_id)
    if(perfil_produtor_produtos(produtor_id,None)):
        produtos = perfil_produtor_produtos(produtor_id,None)
        return render_template('produtor.html', info=perfil, logado=logado, footer=True, produtos=produtos)
    else:
        return "Este produtor não existe"


@app.route("/meu_perfil")
def meu_perfil():
    logado = None
    perfil = None
    if('id_produtor' in session):
        id_produtor = session['id_produtor']
        id_perfil = session['id_perfil']
        logado = session['tipo_conta']
        perfil = recupera_meu_perfil(id_perfil,id_produtor)
    elif('id_perfil' in session):
        id_perfil = session['id_perfil']
        logado = session['tipo_conta']
        perfil = recupera_meu_perfil(id_perfil,False)
    else:
        return "Este produtor não existe"
    return render_template('meu_perfil.html', info=perfil, logado=logado, footer=True)

@app.route("/sobre/")
def sobre():
    return render_template('start.html')


@app.errorhandler(404)
def page_not_found(error):
    return "<h1 style=text-align:center;>Estamos esperando a chuva!</h1>", 404

