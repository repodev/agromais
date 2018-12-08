from .class_PerfilComprador import *

class PerfilProdutor(PerfilComprador):

	def __init__(self,nome,sobrenome,contato,cidade,bairro,endereco,cpf,email,senha,nome_loja,cnpj,contato_comercial,endereco_comercial,descricao_loja,foto_loja):
		super().__init__(nome,sobrenome,contato,cidade,bairro,endereco,cpf,email,senha)
		self.__nome_loja = nome_loja
		self.__cnpj = cnpj
		self.__contato_comercial = contato_comercial
		self.__endereco_comercial = endereco_comercial
		self.__descricao_loja = descricao_loja
		self.__foto_loja = foto_loja

	def getNome_loja(self):
		return self.__nome_loja

	def getCnpj(self):
		return self.__cnpj

	def getDescricao_loja(self):
		return self.__descricao_loja

	def getContato_comercial(self):
		return self.__contato_comercial

	def getEndereco_comercial(self):
		return self.__endereco_comercial

	def getFoto(self):
		return self.__foto_loja