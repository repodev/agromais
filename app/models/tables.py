import psycopg2
import os,time,hashlib
from werkzeug.utils import secure_filename
from app import app
from flask import request
#removido para github public
HOST = ''
USER = ''
PASSWORD = ''
DATABASE = ''


con = psycopg2.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)


def tb_perfil():
    cur = con.cursor()
    try:
        cur.execute('''CREATE TABLE perfil(
            id SERIAL NOT NULL,
            nome VARCHAR NOT NULL,
            sobrenome VARCHAR NOT NULL,
            contato VARCHAR NOT NULL,
            cidade VARCHAR NOT NULL,
            bairro VARCHAR NOT NULL,
            endereco VARCHAR NOT NULL,
            cpf VARCHAR NOT NULL,
            email VARCHAR NOT NULL,
            senha VARCHAR NOT NULL,
            id_produtor INT DEFAULT NULL ,
            PRIMARY KEY(id),
            UNIQUE (email),
            UNIQUE (cpf),
            UNIQUE (id_produtor),
            FOREIGN KEY(id_produtor) REFERENCES perfil_produtor(id_produtor) ON DELETE SET NULL
            )''')
        con.commit()
        con.close()
    except psycopg2.Error as e:
            con.rollback()
            print (e.pgcode,e.diag.message_primary)
    print('TB Perfil criada com sucesso')


def tb_perfil_produtor(): #Criar antes de Perfil
    cur = con.cursor()
    try:
        cur.execute('''CREATE TABLE perfil_produtor(
                id_produtor SERIAL NOT NULL,
                nome_loja VARCHAR NOT NULL,
                cnpj VARCHAR DEFAULT NULL,
                descricao_loja TEXT,
                contato_comercial VARCHAR NOT NULL,
                endereco_comercial VARCHAR,
                foto_loja VARCHAR(400) DEFAULT NULL,
                PRIMARY KEY(id_produtor)
                )''')
        con.commit()
        con.close()
    except psycopg2.Error as e:
            con.rollback()
            print (e.pgcode,e.diag.message_primary)
    print('TB Perfil Produtor criada com sucesso')


def tb_produto():
    cur = con.cursor()
    try:
        cur.execute('''CREATE TABLE produto(
                id_produto SERIAL NOT NULL,
                nome_produto VARCHAR NOT NULL,
                id_categoria INT NOT NULL,
                subcategoria VARCHAR,
                preco NUMERIC NOT NULL,
                estoque NUMERIC NOT NULL,
                foto_produto VARCHAR(300) NOT NULL,
                descricao_produto TEXT NOT NULL,
                id_produtor INT NOT NULL,
                ativo BOOLEAN default True,
                criado_em TIMESTAMPZ NOT NULL,
                atualizado_em TIMESTAMPZ NOT NULL,
                PRIMARY KEY(id_produto),
                FOREIGN KEY(id_produtor) REFERENCES perfil_produtor(id_produtor),
                FOREIGN KEY(id_categoria) REFERENCES categoria(id_categoria)
                )''')
        con.commit()
        con.close()
    except psycopg2.Error as e:
            con.rollback()
            print (e.pgcode,e.diag.message_primary)
    print('TB Produto criada com sucesso')


def tb_pedido():
    cur = con.cursor()
    try:
        cur.execute('''CREATE TABLE pedido(
                id_pedido SERIAL NOT NULL,
                id_produto INT NOT NULL,
                id_comprador INT NOT NULL,
                id_produtor INT NOT NULL,
                quantidade NUMERIC NOT NULL,
                valor NUMERIC NOT NULL,
                pendente BOOLEAN NOT NULL DEFAUL True,
                criado_em TIMESTAMPZ NOT NULL,
                atualizado_em TIMESTAMPZ NOT NULL,
                PRIMARY KEY(id_pedido),
                FOREIGN KEY(id_produto) REFERENCES produto(id_produto),
                FOREIGN KEY(id_comprador) REFERENCES perfil(id),
                FOREIGN KEY(id_produtor) REFERENCES perfil_produtor(id_produtor)
                )''')
        con.commit()
        con.close()
    except psycopg2.Error as e:
            con.rollback()
            print (e.pgcode,e.diag.message_primary)
    print('TB Pedido criada com sucesso')


def tb_categoria(): #Criar essa tabela antes de produto
    cur = con.cursor()
    try:
        cur.execute('''CREATE TABLE categoria(
                id_categoria SERIAL NOT NULL,
                nome_categoria VARCHAR NOT NULL,
                PRIMARY KEY(id_categoria)
                )''')
        con.commit()
        con.close()
    except psycopg2.Error as e:
            con.rollback()
            print (e.pgcode,e.diag.message_primary)
    print('TB Categoria criada com sucesso')


def inserir_perfil(nome,sobrenome,contato,cidade,bairro,endereco,cpf,email,senha):    
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO perfil (nome,sobrenome,contato,cidade,bairro,endereco,cpf,email,senha) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(nome,sobrenome,contato,cidade,bairro,endereco,cpf,email,senha))
        con.commit()
        cur.close()
        
    except psycopg2.Error as e:
           if (str(e.pgcode) == '23505'):
                con.rollback()
                print ("Aquis",e.pgcode,e.diag.message_primary)                         
                return 'Duplicado'
           return False
    else:
            cur.close()
            return 'Aceito'


def inserir_perfil_produtor(nome,sobrenome,contato,cidade,bairro,endereco,cpf,email,senha,nome_loja,cnpj,contato_comercial,endereco_comercial,descricao_loja,foto_loja):
   
    
    try:
        cur = con.cursor()
        cur.execute("INSERT INTO perfil (nome,sobrenome,contato,cidade,bairro,endereco,cpf,email,senha) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(nome,sobrenome,contato,cidade,bairro,endereco,cpf,email,senha))
        cur.execute("INSERT INTO perfil_produtor (nome_loja,cnpj,contato_comercial,endereco_comercial,descricao_loja,foto_loja) VALUES(%s,%s,%s,%s,%s,%s)",(nome_loja,cnpj,contato_comercial,endereco_comercial,descricao_loja,foto_loja))
        cur.execute("UPDATE perfil set id_produtor=(SELECT id_produtor from perfil_produtor WHERE nome_loja=%s) WHERE email=%s and id_produtor IS NULL",(nome_loja,email))

    except psycopg2.Error as e:
        if (str(e.pgcode) == '23505'):
                con.rollback()
                print ("Aqui",e.pgcode,e.diag.message_primary)
                return 'Duplicado'
        print ("Aqui",e.pgcode,e.diag.message_primary)
        return False
    else:        
        con.commit()
        cur.close()

        return 'Aceito'
  

def inserir_produto(nome_produto,categoria,subcategoria,preco,estoque,foto_produto,descricao_produto,id_produtor):  
  

    try:
        cur = con.cursor()
        print("comando")
        cur.execute("INSERT INTO produto (nome_produto,id_categoria,subcategoria,preco,estoque,foto_produto,descricao_produto,id_produtor) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",(nome_produto,categoria,subcategoria,preco,estoque,foto_produto,descricao_produto,id_produtor))
        
    except psycopg2.Error as e:
        if (str(e.pgcode) == '23505'):
                con.rollback()
                print ("Aqui",e.pgcode,e.diag.message_primary)
                return 'Duplicado'
        print ("Aqui",e.pgcode,e.diag.message_primary)
        print("erro desconhecido")
        con.rollback()
        return False        
    else:        
        con.commit()
        cur.close()
        print("Aceito")
        return 'Aceito'      

    
    return True


def verifica_cadastro(email,senha):
    cur = con.cursor()
    cur.execute('SELECT id_produtor FROM perfil WHERE email=%s and senha=%s',(email,senha))
    flag=cur.fetchone()
    print("-------------------FLAG:",flag)
    if(not flag):
        return False
    else:
        cur.close()
        print("--------",flag[0])
        return flag[0]


def recupera_id(email):
    cur = con.cursor()
    cur.execute('SELECT id FROM perfil WHERE email=%s',(email,))
    id_perfil=cur.fetchone()
    cur.close()
    return (id_perfil[0])

#função recupera produtos para index
def recupera_produtos():
     lista_produtos = []
     try:
        cur = con.cursor()   

        cur.execute("SET TIME ZONE 'America/Fortaleza';") 
        cur.execute('SELECT a.id_produto,a.nome_produto,a.foto_produto,a.preco,b.id_produtor,b.nome_loja,c.id_categoria,c.nome_categoria FROM produto a JOIN perfil_produtor b on a.id_produtor = b.id_produtor JOIN categoria c on c.id_categoria = a.id_categoria where a.ativo=True ORDER BY a.id_produto DESC')
        produto = cur.fetchall()
        if(cur.rowcount):
            for produtos in produto:
                lista_produtos.append(produtos)
     except psycopg2.Error as e:
        con.rollback()
        print(e) 
     finally:
        cur.close()
     
     return lista_produtos


def recupera_um_produto(id_produto):
     try:
        cur = con.cursor()   
        cur.execute("SET TIME ZONE 'America/Fortaleza';")
        
        cur.execute('SELECT a.id_produto,a.nome_produto,a.foto_produto,a.preco,a.estoque,a.descricao_produto,b.id_produtor,b.nome_loja,c.id_categoria,c.nome_categoria FROM produto a JOIN perfil_produtor b on a.id_produtor = b.id_produtor JOIN categoria c on c.id_categoria = a.id_categoria where a.ativo=True AND id_produto=%s',(id_produto,))
        produto = cur.fetchone()
     except psycopg2.Error as e:
        con.rollback()
        print(e) 
     finally:
        cur.close()
     
     return produto

def recupera_produto_edicao(id_produto):
     try:
        cur = con.cursor()   
        cur.execute("SET TIME ZONE 'America/Fortaleza';")        
        cur.execute('SELECT * FROM produto where id_produto=%s',(id_produto,))
        produto = cur.fetchone()
     except psycopg2.Error as e:
        con.rollback()
        print(e) 
     finally:
        cur.close()
     
     return produto

def lista_categorias():
     lista_categorias = []
     try:
        cur = con.cursor() 
        cur.execute('select * from categoria')
        categoria = cur.fetchall()
        if(cur.rowcount):
            for categorias in categoria:
                lista_categorias.append(categorias)
     except psycopg2.Error as e:
        con.rollback()
        print(e) 
     finally:
        cur.close()
     
     return lista_categorias


def extensoes(filename):
    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def gera_nome_imagem(FLAG):
    nome_unico = hashlib.sha256(str(time.time()).encode()).hexdigest()
    if(FLAG == 'foto_loja'):
        file = None
        if('foto_loja' in request.files):
            file = request.files['foto_loja']
        if file and extensoes(file.filename):
            #pega o filename e deixa somente a extensão
            filename = secure_filename(file.filename).split(".")[1]            
            #cria novo nome cortado o sha256 e concatena com extensão
            novo_nome = nome_unico[0:20]+"."+filename            
        else:
            novo_nome = 'usuario.png'
        return novo_nome
    else:
        file = None
        if('foto_produto' in request.files):
            file = request.files['foto_produto']
        if file and extensoes(file.filename):
            #pega o filename e deixa somente a extensão
            filename = secure_filename(file.filename).split(".")[1]
            #cria novo nome cortado o sha256 e concatena com extensão
            novo_nome = nome_unico[0:20]+"."+filename
        else:
            novo_nome = None
        return novo_nome


def salva_imagem(FLAG,novo_nome):
    if('foto_loja' in request.files):
        file = request.files['foto_loja']
    if(FLAG == 'foto_loja' and novo_nome != 'usuario.png'):
        file.save(os.path.join(app.config['PASTA_PRODUTORES'], novo_nome))
    if('foto_produto' in request.files):
        file = request.files['foto_produto']
    if(FLAG == 'foto_produto' and novo_nome != None):
        file.save(os.path.join(app.config['PASTA_PRODUTOS'], novo_nome))


def recupera_produtos_categoria(id_categoria):
    lista_produtos = []
    try:
        cur = con.cursor()   

        cur.execute("SET TIME ZONE 'America/Fortaleza';") 
        cur.execute('SELECT a.id_produto,a.nome_produto,a.foto_produto,a.preco,b.id_produtor,b.nome_loja,c.id_categoria,c.nome_categoria FROM produto a JOIN perfil_produtor b on a.id_produtor = b.id_produtor JOIN categoria c on c.id_categoria = a.id_categoria where a.ativo=True and a.id_categoria=%s ORDER BY a.id_produto DESC',(id_categoria,))
        produto = cur.fetchall()
        if(cur.rowcount):
            for produtos in produto:
                lista_produtos.append(produtos)
    except psycopg2.Error as e:
        con.rollback()
        print(e) 
    finally:
        cur.close()
    
    return lista_produtos


def perfil_produtor_publico(id_produtor):

    try:
       cur = con.cursor()
       cur.execute('select * from perfil_produtor WHERE id_produtor=%s',(id_produtor,))
       produtor = cur.fetchone()
    except psycopg2.Error as e:
       con.rollback()
       print(e) 
    finally:
       cur.close()
    
    return produtor

def recupera_meu_perfil(id_perfil,id_produtor):
    try:
       cur = con.cursor()
       if(id_perfil and id_produtor):
            cur.execute('select a.nome,a.sobrenome,a.contato,a.cidade,a.bairro,a.endereco,a.cpf, a.email,b.nome_loja,b.cnpj,b.descricao_loja,b.contato_comercial,b.endereco_comercial,b.foto_loja  from perfil a join perfil_produtor b on a.id_produtor = b.id_produtor WHERE a.id=%s and b.id_produtor=%s',(id_perfil,id_produtor))
            perfil = cur.fetchone()
       else:
            cur.execute('select a.nome,a.sobrenome,a.contato,a.cidade,a.bairro,a.endereco,a.cpf, a.email from perfil a WHERE a.id=%s',(id_perfil,))
            perfil = cur.fetchone()
    except psycopg2.Error as e:
       con.rollback()
       print(e) 
    finally:
       cur.close()
    
    return perfil


def perfil_produtor_produtos(id_produtor,ativo):

    lista_produtos = []
    try:
        cur = con.cursor()   

        cur.execute("SET TIME ZONE 'America/Fortaleza';") 
        if(ativo == 'todos'):
            cur.execute('SELECT a.id_produto,a.nome_produto,a.foto_produto,a.preco,b.id_produtor,b.nome_loja,c.id_categoria,c.nome_categoria,a.ativo FROM produto a JOIN perfil_produtor b on a.id_produtor = b.id_produtor JOIN categoria c on c.id_categoria = a.id_categoria where b.id_produtor=%s ORDER BY a.id_produto DESC',(id_produtor,))
        else:
            cur.execute('SELECT a.id_produto,a.nome_produto,a.foto_produto,a.preco,b.id_produtor,b.nome_loja,c.id_categoria,c.nome_categoria FROM produto a JOIN perfil_produtor b on a.id_produtor = b.id_produtor JOIN categoria c on c.id_categoria = a.id_categoria where a.ativo=True and b.id_produtor=%s ORDER BY a.id_produto DESC',(id_produtor,))
        produto = cur.fetchall()
        if(cur.rowcount):
            for produtos in produto:
                lista_produtos.append(produtos)
    except psycopg2.Error as e:
        con.rollback()
        print(e) 
    finally:
        cur.close()
    
    return lista_produtos


def menu_categorias():
    lista_categorias = []
    try:
       cur = con.cursor()   

       cur.execute('SELECT b.id_categoria,a.nome_categoria FROM produto b JOIN categoria a on b.id_categoria = a.id_categoria;')
       categorias = cur.fetchall()
       if(cur.rowcount):
           for categoria in categorias:
               lista_categorias.append(categoria)
    except psycopg2.Error as e:
       con.rollback()
       print(e) 
    finally:
       cur.close()
    
    return lista_categorias

def registra_pedido(id_produto,id_comprador,id_produtor,quantidade,valor):
    try:
       cur = con.cursor() 
       cur.execute("SET TIME ZONE 'America/Fortaleza';") 
       cur.execute('INSERT INTO pedido(id_produto,id_comprador,id_produtor,quantidade,valor) VALUES(%s,%s,%s,%s,%s)',(id_produto,id_comprador,id_produtor,quantidade,valor))
       cur.execute('UPDATE produto SET estoque=estoque-%s WHERE id_produto=%s',(quantidade,id_produto))
       cur.execute('UPDATE produto SET ativo=false WHERE estoque=0')
     
    except psycopg2.Error as e:
       con.rollback()
       print(e) 
       return "Erro"
    finally:
       con.commit()
       cur.close()
       return "Aceito"


def recupera_pedidos(id_comprador):
    lista_pedidos = []
    try:
       cur = con.cursor()
       cur.execute("SET TIME ZONE 'America/Fortaleza';")  
       cur.execute('select c.nome_produto, a.quantidade, a.valor, a.criado_em, b.nome_loja, b.contato_comercial ,b.endereco_comercial, a.status from pedido a join perfil_produtor b on a.id_produtor = b.id_produtor  join produto c on a.id_produto = c.id_produto WHERE id_comprador=%s ORDER BY a.id_pedido DESC',(id_comprador,))
     
       pedido = cur.fetchall()
       if(cur.rowcount):
            for pedidos in pedido:
                lista_pedidos.append(pedidos)
    except psycopg2.Error as e:
       con.rollback()
       print(e) 
    finally:
       cur.close()
    
    return lista_pedidos

def recupera_vendas(id_produtor):
    lista_vendas = []
    try:
       cur = con.cursor()
       cur.execute("SET TIME ZONE 'America/Fortaleza';")  
       cur.execute('select c.nome_produto, a.quantidade, a.valor, a.criado_em,a.atualizado_em, b.nome, b.contato ,b.endereco, b.email, a.status from pedido a join perfil b on a.id_comprador = b.id join produto c on a.id_produto = c.id_produto where a.id_produtor=%s ORDER BY a.id_pedido DESC',(id_produtor,))
       venda = cur.fetchall()
       if(cur.rowcount):
            for vendas in venda:
                lista_vendas.append(vendas)
    except psycopg2.Error as e:
       con.rollback()
       print(e) 
    finally:
       cur.close()
    
    return lista_vendas

def atualiza_status_produto(ativo,id_produto):
    try:
       cur = con.cursor() 
       cur.execute('UPDATE produto SET ativo=%s WHERE id_produto=%s and estoque>0',(ativo,id_produto))
       row = cur.rowcount
    except psycopg2.Error as e:
       con.rollback()
       print(e) 
       return "Erro"
    finally:
       con.commit()
       cur.close()
       return row

def pesquisa_produto(consulta):
    produtos_localizados = []
    try:
       cur = con.cursor()
       cur.execute("SET TIME ZONE 'America/Fortaleza';")  
       cur.execute("SELECT a.id_produto,a.nome_produto,a.foto_produto,a.preco,b.id_produtor,b.nome_loja,c.id_categoria,c.nome_categoria FROM produto a JOIN perfil_produtor b on a.id_produtor = b.id_produtor JOIN categoria c on c.id_categoria = a.id_categoria where  upper(a.nome_produto) like %s and a.ativo=true",(consulta+"%",))
       produto = cur.fetchall()
       if(cur.rowcount):
            for produtos in produto:
                produtos_localizados.append(produtos)
    except psycopg2.Error as e:
       con.rollback()
       print(e) 
    finally:
       cur.close()
    
    return produtos_localizados

def recupera_pedidos_pendentes(id_produtor):
    pedidos_pendentes = []
    try:
       cur = con.cursor()
       cur.execute("SET TIME ZONE 'America/Fortaleza';")  
       cur.execute("select a.id_pedido, a.quantidade, a.valor ,a.status , a.criado_em , b.nome_produto from pedido a join produto b on a.id_produto = b.id_produto where a.id_produtor = %s and a.status='P' ORDER BY a.id_pedido DESC",(id_produtor,))
       pedido = cur.fetchall()
       if(cur.rowcount):
            for pedidos in pedido:
                pedidos_pendentes.append(pedidos)
    except psycopg2.Error as e:
       con.rollback()
       print(e) 
    finally:
       cur.close()
    
    return pedidos_pendentes

def muda_status_pedido(status,id_produtor,id_pedido,qtd):

    try:
        cur = con.cursor()   
        cur.execute("SET TIME ZONE 'America/Fortaleza';") 
        if(status == 'aceitar'):
            print(status)
            cur.execute("UPDATE pedido SET status='A' WHERE id_produtor=%s and id_pedido=%s",(id_produtor,id_pedido))
            
        else:
            cur.execute("UPDATE pedido SET status='N'  WHERE id_produtor=%s and id_pedido=%s",(id_produtor,id_pedido))
            cur.execute("UPDATE produto set estoque=estoque+%s WHERE id_produto=(SELECT id_produto from pedido WHERE id_pedido=%s)",(qtd,id_pedido))
            cur.execute('UPDATE produto SET ativo=true WHERE estoque!=0 and id_produto=(SELECT id_produto from pedido WHERE id_pedido=%s)',(id_pedido,))
            
    except psycopg2.Error as e:
        con.rollback()
        print(e) 
    finally:
        con.commit()
        cur.close()
    
    return 'Aceito'

def atualiza_produto(nome_produto,categoria,subcategoria,preco,estoque,descricao_produto,id_produtor, id_produto): 

    try:
        cur = con.cursor()
        print("comando")
        cur.execute("SET TIME ZONE 'America/Fortaleza';")    
        cur.execute("UPDATE produto SET nome_produto = %s ,id_categoria = %s ,subcategoria = %s ,preco = %s , estoque = %s ,  descricao_produto = %s WHERE id_produtor = %s and id_produto = %s",(nome_produto,categoria,subcategoria,preco,estoque,descricao_produto,id_produtor,id_produto))
        
    except psycopg2.Error as e:
        print ("Aqui",e.pgcode,e.diag.message_primary)
        con.rollback()
        return 'Error'        
    else:        
        con.commit()
        cur.close()
        print("Aceito")
        return 'Aceito'      

    
    return True