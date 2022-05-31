from cryptography.fernet import Fernet

def dcrypt(encMessage, key):
    storedkey = key
    fernet = Fernet(storedkey)
    decMessage = fernet.decrypt(encMessage).decode()
    return decMessage

