class Pedido():
	def __init__(self,id_produto,id_comprador,id_produtor,quantidade,valor):
		self.id_produto = id_produto		
		self.id_comprador = id_comprador
		self.id_produtor = id_produtor
		self.quantidade = quantidade	
		self.valor = valor
	


	def getId_produto(self):
		return self.id_produto		

	def getId_comprador(self):
		return self.id_comprador

	def getId_produtor(self):
		return self.id_produtor

	def getQuantidade(self):
		return self.quantidade

	def getValor(self):
		return self.valor
