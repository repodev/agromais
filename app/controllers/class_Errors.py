class Errors(object):

    def reg_duplicado(self):
        return "Nenhum erro detectado"
    
    def reg_desconhecido(self):
        return "Nenhum erro detectado"

class ErrorCadPerfil(Errors):
    
    def reg_duplicado(self):
        return "Já existe um perfil com essas informações! verifique os campos (email,cpf)"
    
    def reg_desconhecido(self):
        return "Erro ao cadastrar seu perfil, por favor tente novamente."

class ErrorCadPerfilProdutor(Errors):
    
    def reg_duplicado(self):
        return "Já existe um perfil produtor com essas informações! verifique os campos (email, cpf)"
    
    def reg_desconhecido(self):
        return "Erro ao cadastrar seu perfil produtor, por favor tente novamente."

class ErrorCadProduto(Errors):

    def reg_duplicado(self):
        return "Já existe um produto com essas informações!"
    
    def reg_desconhecido(self):
        return "Erro ao cadastrar seu produto, por favor tente novamente."

class ErrorAtualizaProduto(Errors):

    def reg_duplicado(self):
        return "Já existe um produto com essas informações!"
    
    def reg_desconhecido(self):
        return "Erro ao atualizar seu produto, por favor tente novamente."

class ErroCadLogin(Errors):
    
    def reg_desconhecido(self):
        return "Email ou senha incorretos, tente novamente!!"