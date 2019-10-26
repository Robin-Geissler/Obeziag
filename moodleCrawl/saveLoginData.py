import sys
import dataFunctions





user = sys.argv[1]
passwort = sys.argv[2]

dataFunctions.write_login_data(user, passwort)

print("written successfully")

sys.stdout.flush()






