# import os
# from dotenv import load_dotenv

# load_dotenv()

# class Config:
#     SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
#     DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost/fingerprint_db')
#     UPLOAD_FOLDER = 'uploads'
#     ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}
#     AES_KEY = os.getenv('AES_KEY', '0123456789abcdef0123456789abcdef')  # 32 bytes for AES-256
#     AES_IV = os.getenv('AES_IV', 'abcdef0123456789')  # 16 bytes for AES
    
# config = Config()
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://fingerprint_user:securepassword123@localhost:5432/fingerprint_db')
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'tiff'}
    AES_KEY = os.getenv('AES_KEY', '0123456789abcdef0123456789abcdef')  # 32 bytes for AES-256
    AES_IV = os.getenv('AES_IV', 'abcdef0123456789')  # 16 bytes for AES
    
config = Config()