from .class_Perfil import *

class PerfilComprador(Perfil):
	def __init__(self,nome,sobrenome,contato,cidade,bairro,endereco,cpf,email,senha):
		super().__init__(nome,sobrenome,email,senha,cpf)
		self.contato = contato
		self.cidade = cidade
		self.bairro = bairro
		self.endereco = endereco		

	#GETS
	
	def getContato(self):
		return self.contato

	def getCidade(self):
		return self.cidade

	def getBairro(self):
		return self.bairro

	def getEndereco(self):
		return self.endereco