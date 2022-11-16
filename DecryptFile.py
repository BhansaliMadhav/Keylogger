import os
from cryptography.fernet import Fernet
user_name = os.environ["USERPROFILE"]
keys_information_e = f"{user_name}\\PycharmProjects\\keylogger\\project\\showfolder\\e_key_log.txt"
key = "AAvzB4kDg62APorFje7ulESVwmxavpjHoSk5Dsx4RIs="
keys_information_d = "keys_information_d"

with open(keys_information_e, "rb") as f:
    data = f.read()
fernet = Fernet(key)
decrypted = fernet.decrypt(data)

with open(keys_information_d, "wb") as f:
    f.write(decrypted)
