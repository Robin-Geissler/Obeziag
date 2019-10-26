import json
import cryptography


def write_login_data(username, userpassword):
    data = {"user": username, "password": userpassword}

    with open("../data/loginData.json", "w") as json_file:
        json.dump(data, json_file)


def read_login_data():
    with open("../data/loginData.json") as json_file:
        return json.load(json_file)


