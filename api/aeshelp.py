import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

class AesHelper(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        #raw = self._pad(raw)
        for i in range( AES.block_size - (len(raw)  % AES.block_size) ):
            raw += " ";
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        #ct_bytes = cipher.encrypt(pad(data, AES.block_size))
        #return base64.b64encode(iv + cipher.encrypt(raw.encode()))
        #return base64.b64encode(iv + cipher.encrypt(       pad(raw.encode(), AES.block_size)  ))
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        #mensagem = unpad(cipher.decrypt(enc[AES.block_size:]), AES.block_size).decode('utf-8').strip();
        #print("decriptado: ", mensagem);
        #return mensagem;
        #message = Padding.unpad(cipher.decrypt(ct), AES.block_size)
        #return AesHelper._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8');
        return cipher.decrypt( enc[AES.block_size:] ).decode('utf-8').strip();


    #def _pad(self, s):
    #    return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)
    #@staticmethod
    #def _unpad(s):
    #    return s[:-ord(s[len(s)-1:])]

if __name__ == "__main__":
    ae = AesHelper('1234567890123456');
    criptografado = ae.encrypt('{"comando" : 1, "request" : "index.html"}');
    print("Criptografaod: ", criptografado);
    descriptografado = ae.decrypt(criptografado);
    #print("CRIPTOGRAFADO", type(criptografado), criptografado);
    print("desCRIPTOGRAFADO", type(descriptografado), descriptografado);