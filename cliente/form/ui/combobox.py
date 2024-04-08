import inspect;

from PySide6.QtWidgets import QComboBox;

class ItemValor:
    def __init__(self, key, value):
        self.key = key;
        self.value = value;

class ComboBox (QComboBox):
    def __init__(self, form, cache_name, configuracao=None):
        super().__init__();
        self.em_carregamento = False;
        self.cache_name = cache_name;
        self.valores = [];
        self.configuracao = configuracao;
        self.currentIndexChanged.connect(self.__interno_selected)

    def __interno_selected(self):
        if self.configuracao == None or self.em_carregamento or self.currentIndex() < 0:
            return;
        self.configuracao.setValor(self.cache_name, self.currentIndex());
    
    def addArrayObject(self, js, key, value):
        self.valores = [];
        for item in js:
            self.valores.append( ItemValor(getattr(item,  key), getattr(item, value)) );
        self.redesenhar();
    def getSelected(self):
        if self.currentIndex() < 0:
            return None;
        return self.valores[self.currentIndex()];
    def redesenhar(self):
        self.em_carregamento = True;
        self.clear();
        for item in self.valores:
            self.addItem( item.value );
        buffer = self.configuracao.getValor(self.cache_name);
        if buffer == None:
            self.setCurrentIndex(0);
        else:
            self.setCurrentIndex( buffer );
        self.em_carregamento = False;




