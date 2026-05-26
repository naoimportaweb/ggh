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
        encrypted = base64.b64encode( encryptor.encrypt( raw.encode('utf-8')  ));
        return encrypted.decode('utf-8');

    def decrypt(self, enc):
        decryptor = PKCS1_OAEP.new( self.chave_privada );
        buffer = base64.b64decode( enc.encode('utf-8') );
        return decryptor.decrypt( buffer ).decode('utf-8');
        
