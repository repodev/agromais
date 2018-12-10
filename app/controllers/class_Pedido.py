class Pedido():
	def __init__(self,id_produto,id_comprador,id_produtor,quantidade,valor):
		self.__id_produto = id_produto		
		self.__id_comprador = id_comprador
		self.__id_produtor = id_produtor
		self.__quantidade = quantidade	
		self.__valor = valor
	
	def getId_produto(self):
		return self.__id_produto		

	def getId_comprador(self):
		return self.__id_comprador

	def getId_produtor(self):
		return self.__id_produtor

	def getQuantidade(self):
		return self.__quantidade

	def getValor(self):
		return self.__valor
