class Errors(object):

    def reg_duplicado(self):
        return "Nenhum erro detectado"
    
    def reg_desconhecido(self):
        return "Nenhum erro detectado"
    
    def status(self):
        return "10"

class ErrorCadPerfil(Errors):
    
    def reg_duplicado(self):
        return "Já existe um perfil com essas informações! verifique os campos (email,cpf)"
    
    def reg_desconhecido(self):
        return "Erro ao Cadastrar seu perfil, por favor tente novamente."

    def status(self):
        return "1"

class ErrorCadPerfilProdutor(Errors):
    
    def reg_duplicado(self):
        return "Já existe um perfil com essas informações! verifique os campos (email, cpf, nome loja)"
    
    def reg_desconhecido(self):
        return "Erro ao Cadastrar seu perfil, por favor tente novamente."

    def status(self):
        return "1"

class ErrorCadProduto(Errors):

    def reg_duplicado(self):
        return "Já existe um produto com essas informações!"
    
    def reg_desconhecido(self):
        return "Erro ao Cadastrar seu produto, por favor tente novamente."

    def status(self):
        return "1"

class ErroCadLogin(Errors):
    
    def reg_desconhecido(self):
        return "Email ou senha incorretos, tente novamente!!"

