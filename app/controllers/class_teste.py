class Perfil:
	#SETS
	def setNome(self,nome):
		self.__nome = nome

	def setSobrenome(self,sobrenome):
		self.__sobrenome = sobrenome

	def setContato(self,contato):
		self.__contato = contato

	def setCidades(self,cidades):
		self.__cidades = cidades

	def setBairro(self,bairro):
		self.__bairro = bairro

	def setEndereco(self,endereco):
		self.__endereco = endereco

	def setCpf(self,cpf):
		self.__cpf = cpf

	def setEmail(self,email):
		self.__email = email

	def setSenha(self,senha):
		self.__senha = senha
	#GETS
	def getNome(self):
		return self.__nome

	def getSobrenome(self):
		return self.__sobrenome

	def getContato(self):
		return self.__contato

	def getCidades(self):
		return self.__cidades

	def getBairro(self):
		return self.__bairro

	def getEndereco(self):
		return self.__endereco

	def getCpf(self):
		return self.__cpf

	def getEmail(self):
		return self.__email

	def getSenha(self):
		return self.__senha