class Pedido():
	def __init__(self,id_pedido,id_produto,id_comprador,id_produtor,quantidade,data,valor,pendente):
		self.id_pedido = id_pedido
		self.id_produto = id_produto		
		self.id_comprador = id_comprador
		self.id_produtor = id_produtor
		self.quantidade = quantidade
		self.data = data
		self.valor = valor
		self.pendente = pendente

		def getId_pedido(self):
			return self.id_pedido

		def getId_produto(self):
			return self.id_produto		

		def getId_comprador(self):
			return self.id_comprador

		def getId_produtor(self):
			return self.id_produtor

		def getQuantidade(self):
			return self.quantidade

		def getData(self):
			return self.data

		def getValor(self):
			return self.valor

		def getPendente(self):
			return self.pendente