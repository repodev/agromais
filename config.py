class Config(object):
   pass
class ConfigProducao(Config):
    pass

class ConfigDev(Config):
    DEBUG = True
    SECRET_KEY = 'agr0m4isnUnc4'