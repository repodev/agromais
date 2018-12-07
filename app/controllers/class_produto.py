class Produto():
	def __init__(self,nome_produto,categoria,subcategoria,preco,estoque,foto_produto,descricao_produto,id_produtor):
		self.nome_produto = nome_produto
		self.categoria = categoria
		self.subcategoria = subcategoria
		self.preco = preco
		self.estoque = estoque
		self.foto_produto = foto_produto
		self.descricao_produto = descricao_produto
		self.id_produtor = id_produtor

	def getNome_produto(self):
		return self.nome_produto

	def getCategoria(self):
		return self.categoria

	def getSubcategoria(self):
		return self.subcategoria

	def getPreco(self):
		return self.preco

	def getEstoque(self):
		return self.estoque
	
	def getFoto_produto(self):
		return self.foto_produto

	def getDescricao_produto(self):
		return self.descricao_produto

	def getId_produtor(self):
		return self.id_produtor