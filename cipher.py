from cryptography.fernet import Fernet

# key generation
# GEN_KEY = Fernet.generate_key()
# opening the key
# newkry=Fernet.generate_key()
# with open("msgkey.key", "wb") as key_file:
#      key_file.write(newkry)
with open("filekey.key", "rb") as filekey:
    KEY = filekey.read()
with open("msgkey.key", "rb") as filekey:
    MKEY = filekey.read()


class Crypt:
    # def __init__(self) -> None:
    def encrypt(self, path):
        cipher_suite = Fernet(KEY)
        with open(path, "rb") as file:
            file_data = file.read()
            encrypt = cipher_suite.encrypt(file_data)
        with open(path, "wb") as file:
            file.write(encrypt)

    def decrypt(self, path):
        cipher_suite = Fernet(KEY)
        with open(path, "rb") as file:
            file_data = file.read()
            decrypt = cipher_suite.decrypt(file_data)
        with open(path, "wb") as file:
            file.write(decrypt)

    def encrypttext(self, text):
        cipher_suite = Fernet(MKEY)
        encrypt = cipher_suite.encrypt(text.encode())
        return encrypt

    def decrypttext(self, text):
        cipher_suite = Fernet(MKEY)
        decrypt = cipher_suite.decrypt(text)
        return decrypt
