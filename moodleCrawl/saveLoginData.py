import sys
import cryptography
import json


def writedata(username, userpassword):
    data = {'user': username, 'password': userpassword}

    with open("../data/loginData.json", 'w') as storefile:
        json.dump(data, storefile)



user = sys.argv[1]
passwort = sys.argv[2]

writedata(user,passwort)
print("the user is: " + user + "\nthe password is: " + passwort)
print(True)

sys.stdout.flush()






