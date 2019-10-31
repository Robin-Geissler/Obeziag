import json
from cryptography.fernet import Fernet

# Todo: Bei einem allgemeinem Build muss der key geändert werden
# damit er über den source Code nicht einsehbar ist
# zur key Generierung wird die Funktion gen_key bereit gestellt
key = b'VM2Ug42nvv-L0-BMmqblXgTPiTkIviraa7pZAxWb5Yg='


# encryption and decrytion useses fernet, which is based on AES-CBC with 128 bit Keys
# input is a str Object
def encrypt_data(data):
    data = str.encode(data)
    f = Fernet(key)
    encrypted = f.encrypt(data)
    encrypted = encrypted.decode()
    return encrypted


# input is a str Object
def decrypt_data(data):
    data = str.encode(data)
    f = Fernet(key)
    decrypted = f.decrypt(data)
    decrypted = decrypted.decode()
    return decrypted


# writes username and userpassword to loginData.json in folder data
# the data will be encrypted
def write_login_data(username, userpassword):
    username = encrypt_data(username)
    userpassword = encrypt_data(userpassword)

    data = {"user": username, "password": userpassword}

    with open("../data/loginData.json", "w") as json_file:
        json.dump(data, json_file)


# reads username and userpassword from loginData.json in folder data
# output is a Tupel (user,password)
# password and username will be decrypted
def read_login_data():
    with open("../data/loginData.json") as json_file:
        json_data = json.load(json_file)
        user = json_data.get("user")
        password = json_data.get("password")

        user = decrypt_data(user)
        password = decrypt_data(password)

        return user, password


# can be used to generate a new key
def gen_key():
    new_key = Fernet.generate_key()
    print(new_key)




