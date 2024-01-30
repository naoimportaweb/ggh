import os, json, sys;

from api.chachahelp import ChaChaHelper;

class FsSeguro:
    def __init__(self, chave):
        self.chave = chave;

    def ler_raw(self, path):
        if not os.path.exists( path ):
            return None;
        try:
            with open( path, "r" ) as f:
                buffer = f.read();
                aes_help = ChaChaHelper( key=self.chave );
                return aes_help.decrypt( buffer );
        except:
            return None;

    def ler_json(self, path):
        buffer = self.ler_raw( path );
        if buffer == None:
            return None;
        return json.loads( buffer );

    def escrever_raw(self, path, data):
        if len(data) > 0:
            aes_help = ChaChaHelper( key=self.chave );
            data = aes_help.encrypt( data ).decode();
        with open( path, "w" ) as f:
            f.write( data );
        return os.path.exists( path );

    def escrever_json(self, path, js):
        return self.escrever_raw(path, json.dumps( js ) );

#f = FsSeguro("1234567890123456");
#f.escrever_raw("/tmp/criptografado.txt", "abcdefghijklmnopqrstuvxzabcdefghijklmnopqrstuvxzabcdefghijklmnopqrstuvxzabcdefghijklmnopqrstuvxz")
#print( f.ler_raw( "/tmp/criptografado.txt" ) )
#f.escrever_json("/tmp/criptografado.json", {"comando" : "teste", "exemplo" : "1"});
#print( f.ler_json( "/tmp/criptografado.json" ));


