class Perfil(object):
	def __init__(self,nome,sobrenome,email,senha,cpf):
		self.nome = nome
		self.sobrenome = sobrenome
		self.email = email
		self.senha = senha
		self.cpf = cpf
	
	def getNome(self):
		return self.nome

	def getSobrenome(self):
		return self.sobrenome

	def getEmail(self):
		return self.email

	def getSenha(self):
		return self.senha

	def getCpf(self):
		return self.cpf

class PerfilComprador(Perfil):
	def __init__(self,nome,sobrenome,contato,cidades,bairro,endereco,cpf,email,senha):
		super().__init__(nome,sobrenome,email,senha,cpf)
		self.contato = contato
		self.cidades = cidades
		self.bairro = bairro
		self.endereco = endereco		

	#GETS
	
	def getContato(self):
		return self.contato

	def getCidades(self):
		return self.cidades

	def getBairro(self):
		return self.bairro

	def getEndereco(self):
		return self.endereco


class PerfilProdutor(PerfilComprador):

	def __init__(self,nome,sobrenome,contato,cidades,bairro,endereco,cpf,email,senha,nome_loja,contato_comercial,endereco_comercial):
		super().__init__(nome,sobrenome,contato,cidades,bairro,endereco,cpf,email,senha)
		self.nome_loja = nome_loja
		#self.descricao_produtor = descricao_produtor
		self.contato_comercial = contato_comercial
		self.endereco_comercial = endereco_comercial

	def getNome_loja(self):
		return self.nome_loja

	#def getDescricao_produtor(self):
		#return self.descricao_produtor

	def getContato_comercial(self):
		return self.contato_comercial

	def getEndereco_comercial(self):
		return self.endereco_comercial


class Login():
	def __init__(self,email,senha):#tipoConta
		self.email = email
		self.senha = senha
		#self.tipoConta = tipoConta

	def getEmail(self):
		return self.email

	def getSenha(self):
		return self.senha

	#def getTipoConta(self):
		#return self.tipoConta