
from classes.singleton.singlegon_meta import SingletonMeta;

class Configuracao(metaclass=SingletonMeta):
    def set_sessao(self, value):
        self.sessao = value;
    
    def get_sessao(self):
        return self.sessao;


