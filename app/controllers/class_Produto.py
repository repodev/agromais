class Produto():
	def __init__(self,nome_produto,categoria,subcategoria,preco,estoque,foto_produto,descricao_produto,id_produtor):
		self.__nome_produto = nome_produto
		self.__categoria = categoria
		self.__subcategoria = subcategoria
		self.__preco = preco
		self.__estoque = estoque
		self.__foto_produto = foto_produto
		self.__descricao_produto = descricao_produto
		self.__id_produtor = id_produtor

	def getNome_produto(self):
		return self.__nome_produto

	def getCategoria(self):
		return self.__categoria

	def getSubcategoria(self):
		return self.__subcategoria

	def getPreco(self):
		return self.__preco

	def getEstoque(self):
		return self.__estoque
	
	def getFoto_produto(self):
		return self.__foto_produto

	def getDescricao_produto(self):
		return self.__descricao_produto

	def getId_produtor(self):
		return self.__id_produtor