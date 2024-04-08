import os, sys;

from api.fsseguro import FsSeguro;
from classes.singleton.singlegon_meta import SingletonMeta;

class Configuracao(metaclass=SingletonMeta):
    def __init__(self, path_cliente, fs):
        self.path_cliente = path_cliente;
        self.path_arquivo = self.path_cliente + "/config.json";
        self.fs = fs;
        self.valores = None;
        self.carregar();

    def carregar(self):
        if os.path.exists(self.path_arquivo):
            self.valores = self.fs.ler_json( self.path_arquivo );
        else:
            self.valores = {};
    
    def salvar(self):
        self.fs.escrever_json( self.path_arquivo, self.valores );

    def setValor(self, chave, value):
        if self.getValor( chave ) != value:
            self.valores[chave] = value;
            self.salvar();
    
    def getValor(self, chave):
        if self.valores.get( chave ) == None:
            return None;
        return self.valores[chave];


