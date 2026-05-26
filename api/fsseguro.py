import os, json, sys, traceback;

from api.chachahelp import ChaChaHelper;

class FsSeguro:
    def __init__(self, chave):
        self.chave = chave;

    def ler_raw(self, path):
        if not os.path.exists( path ):
            return None;
        try:
            with open( path, "rb" ) as f:
                buffer = f.read();
                aes_help = ChaChaHelper( key=self.chave );
                return aes_help.decrypt( buffer.decode("utf-8") );
        except:
            traceback.print_exc();
            return None;

    def ler_json(self, path):
        buffer = self.ler_raw( path );
        if buffer == None:
            return None;
        return json.loads( buffer );

    def escrever_raw(self, path, data):
        if len(data) > 0:
            aes_help = ChaChaHelper( key=self.chave );
            data = aes_help.encrypt( data );
            with open( path, "wb" ) as f:
                f.write( data );
            return os.path.exists( path );
        return False;
    def escrever_json(self, path, js):
        return self.escrever_raw(path, json.dumps( js ) );
    
    def escrever_binario(self, path, binario):
        cypherhelp = ChaChaHelper( key=self.chave );
        binario = cypherhelp.encrypt_binario( binario );
        with open (path, "bw") as f:
            f.write( binario );
            return True;
        return False;

    def ler_binario(self, path):
        cypherhelp = ChaChaHelper( key=self.chave );
        with open(path, "rb") as k:
            return cypherhelp.decrypt_binario( k.read() );
        return None;





#with open (self.path_private_key, "bw") as prv_file:
#    prv_file.write( self.private_key );
#with open (self.path_public_key, "wb") as pub_file:
#    self.public_key = public_key.exportKey().decode("utf-8");
#    pub_file.write( self.public_key.encode("utf-8") );


