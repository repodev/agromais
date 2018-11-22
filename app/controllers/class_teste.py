class Perfil:
	def __int__(nome,sobrenome,contato,cidades,bairro,endereco,cpf,email,senha):
		self.nome = nome
		self.sobrenome = sobrenome
		self.cidades = cidades
		self.bairro = bairro
		self.endereco = endereco
		self.cpf = cpf
		self.email = email
		self.senha = senha

	#GETS
	def getNome(self):
		return self.nome

	def getSobrenome(self):
		return self.sobrenome

	def getContato(self):
		return self.contato

	def getCidades(self):
		return self.cidades

	def getBairro(self):
		return self.bairro

	def getEndereco(self):
		return self.endereco

	def getCpf(self):
		return self.cpf

	def getEmail(self):
		return self.email

	def getSenha(self):
		return self.senha

class Perfil_produtor(Perfil):

	def __int__(self,nome,sobrenome,contato,cidades,bairro,endereco,cpf,email,senha,nome_loja,contato_comercial,endereco_comercial):
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