from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from flask import current_app

class AESEncryption:
    def __init__(self):
        self.key = current_app.config['AES_KEY'].encode('utf-8')
        self.iv = current_app.config['AES_IV'].encode('utf-8')
    
    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        encrypted = cipher.encrypt(pad(data, AES.block_size))
        return base64.b64encode(encrypted).decode('utf-8')
    
    def decrypt(self, encrypted_data):
        encrypted_data = base64.b64decode(encrypted_data)
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        return decrypted.decode('utf-8')