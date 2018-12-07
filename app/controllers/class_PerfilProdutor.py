from .class_PerfilComprador import *

class PerfilProdutor(PerfilComprador):

	def __init__(self,nome,sobrenome,contato,cidade,bairro,endereco,cpf,email,senha,nome_loja,cnpj,contato_comercial,endereco_comercial,descricao_loja,foto_loja):
		super().__init__(nome,sobrenome,contato,cidade,bairro,endereco,cpf,email,senha)
		self.nome_loja = nome_loja
		self.cnpj = cnpj
		self.contato_comercial = contato_comercial
		self.endereco_comercial = endereco_comercial
		self.descricao_loja = descricao_loja
		self.foto_loja = foto_loja

	def getNome_loja(self):
		return self.nome_loja

	def getCnpj(self):
		return self.cnpj

	def getDescricao_loja(self):
		return self.descricao_loja

	def getContato_comercial(self):
		return self.contato_comercial

	def getEndereco_comercial(self):
		return self.endereco_comercial

	def getFoto(self):
		return self.foto_loja