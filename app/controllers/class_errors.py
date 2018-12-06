class Errors(object):

    def reg_duplicado(self):
        return "Nenhum erro detectado"
    
    def reg_desconhecido(self):
        return "Nenhum erro detectado"
    
    def status(self):
        return "10"

class ErrorCadPerfil(Errors):
    
    def reg_duplicado(self):
        return "Nenhum erro detectado"
    
    def reg_desconhecido(self):
        return "Nenhum erro detectado"

    def status(self):
        return "1"

class ErrorCadProduto(Errors):

    def reg_duplicado(self):
        return "Nenhum erro detectado"
    
    def reg_desconhecido(self):
        return "Nenhum erro detectado"

    def status(self):
        return "1"

class ErroCadLogin(Errors):
    
    def reg_desconhecido(self):
        return "Nenhum erro detectadosss"


a = ErroCadLogin()

print(a.reg_desconhecido())