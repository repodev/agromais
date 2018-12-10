class Login():
	def __init__(self,email,senha):
		self.__email = email
		self.__senha = senha

	def getEmail(self):
		return self.__email

	def getSenha(self):
		return self.__senha