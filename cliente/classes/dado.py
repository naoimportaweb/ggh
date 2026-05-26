

class Dado:
    def campo(self, js, campo_nome):
        if js.get(campo_nome) != None:
            return js[campo_nome];
        return None;