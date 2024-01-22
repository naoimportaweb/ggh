import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

class AesHelper(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return AesHelper._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

if __name__ == "__main__":
    ae = AesHelper(b'1234567890123456');
    criptografado = ae.encrypt('{"comando" : 1, "request" : "index.html"}');
    descriptografado = ae.decrypt(criptografado);
    print("CRIPTOGRAFADO", type(criptografado), criptografado);
    print("desCRIPTOGRAFADO", type(descriptografado), descriptografado);