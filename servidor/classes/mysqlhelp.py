
# importing required libraries
import random, os, sys;

import mysql.connector, json
from mysql.connector import Error
from mysql.connector import errorcode

class MysqlHelp:
    def __init__(self, host=None, user=None, password=None, database=None):
        # Dados padrões para testes, depois tenho que fazer um config sigleton
        self.configuracao = json.loads( os.environ["database"] );
        self.dataBase = mysql.connector.connect(
            host = self.configuracao["server"],
            user = self.configuracao["user"],
            passwd =  self.configuracao["password"] ,
            database = self.configuracao["database"] );
        self.cursorObject = self.dataBase.cursor();
    
    def execute(self, sql, values=None):
        if values == None:
            values = [];

        self.cursorObject.execute(sql, values);
        self.dataBase.commit();
    
    def executes(self, sqls, array_values):
        try:
            self.cursorObject = self.dataBase.cursor();
            for i in range(len(array_values)):
                self.cursorObject.execute(sqls[ i ], array_values[ i ] );
            self.dataBase.commit();
        except mysql.connector.Error as error :
           print("Database Update Failed !: {}".format(error))
           self.dataBase.rollback()   
    
    def datatable(self, sql, values=None):
        if values == None:
            values = [];
        self.cursorObject.execute( sql, values );
        rows = self.cursorObject.fetchall()
        result = []
        for row in rows:
            d = {}
            for i, col in enumerate(self.cursorObject.description):
                d[ col[0] ] = row[ i ];
            result.append( d );
        return result;
    
    def chave_string(self, tabela, field, tamanho ):
        letras = "abcdefghijklmnopqrstuvxzABCDEFGHIJKLMNOPQRSTUVXZ1234567890";
        retorno = "";
        tentatias = 0;
        MAX_TENTATIVAS = 50;
        while True:
            if tentatias > MAX_TENTATIVAS:
                return None;
            retorno = "";
            for i in range( tamanho ):
                posicao = random.randint(0, len( letras ) );
                retorno += letras[ posicao : posicao + 1];
            if len( self.datatable( "SELECT * FROM " + tabela + " where " + field + " = '"+ retorno +"'" ) ) == 0 :
                return retorno;

    def __testar_tabela__(self, nome):
        tables = self.datatable( "show tables " );
        if len(tables) > 0:
            keylist = list(tables[0].keys())
            for tabela in tables:
                if tabela[ keylist[0] ] == nome:
                    return True;
        print("  [*] \033[91mA tabela ", nome, "\033[0m não foi localizada.");
        return False;

    def __testar_field__(self, tabela, field):
        colunas = self.datatable( "SHOW COLUMNS FROM " + tabela );
        for coluna in colunas:
            if coluna["Field"] == field:
                return True;
        print("     [*] \033[91mO campo ", field, " da tabela ", tabela ,"\033[0m não foi localizado.");
        return False;

    def teste(self, estruturas):
        falhas = 0;

        for estrutura in estruturas:
            print("[+] Tabela: \033[94m", estrutura["nome"], "\033[0m");
            if not self.__testar_tabela__(estrutura["nome"]):
                falhas +=1;
                continue;
            for field in estrutura["fields"]:
                if not self.__testar_field__( estrutura["nome"], field):
                    falhas +=1;
        return falhas;