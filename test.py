# import datetime
#
#
# st=datetime.datetime.now()
# squared_numbers = []
#
#
# for num in range(0,1000):
#     squared_numbers.append(num**2)
#
# endt=datetime.datetime.now()
#
#
#
# st=datetime.datetime.now()
# squared_numbers = [num**2 for num in range(0,1000)]
#
# endt=datetime.datetime.now()
#
#
#
#
# data=["increment_01","increment_02","increment_03","increment_04","increment_05","increment_06"]
import json
import requests
FIREBASE_WEB_API_KEY = "AIzaSyDe2qwkIds8JwMdLBbY3Uw7JQkFRNXtFqo"
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True):
    payload = json.dumps({
        "email": email,
        "password": password,
        "returnSecureToken": return_secure_token
    })

    r = requests.post(rest_api_url,
                      params={"key": FIREBASE_WEB_API_KEY},
                      data=payload)

    return r.json()



print(sign_in_with_email_and_password(email="jeel.patel@aliansoftware.com", password="jeel@123"))