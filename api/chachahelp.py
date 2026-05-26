
import json, os, hashlib;
from base64 import b64encode, b64decode;
from Crypto.Cipher import ChaCha20;
from Crypto.Random import get_random_bytes;

class ChaChaHelper():
    def __init__(self, key):
        self.key = hashlib.md5( key.encode() ).hexdigest()[:32].encode();

    def encrypt(self, message):
        cipher = ChaCha20.new(key=self.key);
        ciphertext = cipher.encrypt(message.encode('utf-8'));
        nonce = b64encode(cipher.nonce).decode('utf-8')
        ct = b64encode(ciphertext).decode('utf-8')
        result = nonce + "." + ct;
        return result.encode("utf-8");
    
    def decrypt(self, message):
        nonce = message[: message.find( "." ) ];
        ciphertext = b64decode(message[message.find( "." ) : ]); #+ "========"
        cipher = ChaCha20.new(key=self.key, nonce=b64decode(nonce));
        plaintext = cipher.decrypt(ciphertext);
        return plaintext.decode("utf-8");
    
    def encrypt_binario(self, message):
        nonce = os.urandom(12);#"123456789012".encode();# cipher.nonce;
        cipher = ChaCha20.new(key=self.key, nonce=nonce);
        ciphertext = cipher.encrypt(message);
        return nonce + ciphertext;
    
    def decrypt_binario(self, message):
        #nonce = "123456789012".encode();# message[: 12];
        nonce = message[: 12]; message = message[12:];
        ciphertext = message;# message[12 - 4:];
        cipher = ChaCha20.new( key=self.key, nonce=nonce);
        plaintext = cipher.decrypt(ciphertext);
        return plaintext;

#helper = ChaChaHelper("1234567890123456");
#with open( "/home/well/Downloads/Untitled.jpeg", "rb" ) as f:
#    criptografado = helper.encrypt_binario( f.read() ) ;
#    with open( "/tmp/criptografado.jpg", "wb") as w:
#        w.write(criptografado);
#with open( "/tmp/criptografado.jpg", "rb" ) as f:
#    descriptogrado = helper.decrypt_binario( f.read() ) ;
#    with open( "/tmp/untiteled.jpg", "wb") as w:
#        w.write(descriptogrado);
