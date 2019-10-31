import sys
import dataFunctions

# dieses Skript speichert die userdaten in der Datei loginData.json im folder data

user = sys.argv[1]
passwort = sys.argv[2]

dataFunctions.write_login_data(user, passwort)

print("written successfully")

sys.stdout.flush()






