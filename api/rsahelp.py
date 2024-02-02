import os, sys, json, base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA

class RsaHelper:
    def __init__(self, chave_publica, chave_privada=None):
        self.chave_publica = chave_publica;
        self.chave_privada = chave_privada;

    def encrypt(self, raw):
        key_pub = RSA.importKey( self.chave_publica );
        encryptor = PKCS1_OAEP.new( key_pub );
        encrypted = base64.b64encode( encryptor.encrypt( raw.encode()  ));
        return encrypted.decode("ascii");

    def decrypt(self, enc):
        if self.chave_privada == None:
            return None;
        decryptor = PKCS1_OAEP.new( self.chave_privada );
        return decryptor.decrypt( base64.b64decode( enc.encode() ) ).decode();
        

