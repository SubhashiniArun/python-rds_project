from cryptography.fernet import Fernet
import os

SECRET_KEY = os.getenv('ENCRYPTION_KEY')
fernet = Fernet(SECRET_KEY)

def encrypt_token(token: str) -> str:
    encrypted_token = fernet.encrypt(token.encode()).decode()
    return encrypted_token

def decrypt_token(encrypted_token: str) -> str:
    decrypted_token = fernet.decrypt(encrypted_token.encode()).decode()
    return decrypted_token