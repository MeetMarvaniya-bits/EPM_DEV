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
# FIREBASE_WEB_API_KEY = "AIzaSyDe2qwkIds8JwMdLBbY3Uw7JQkFRNXtFqo"
# rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
# def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True):
#     payload = json.dumps({
#         "email": email,
#         "password": password,
#         "returnSecureToken": return_secure_token
#     })
#
#     r = requests.post(rest_api_url,
#                       params={"key": FIREBASE_WEB_API_KEY},
#                       data=payload)
#
# st=datetime.datetime.now()
# squared_numbers = []
#
#
# for num in range(0,1000):
#     squared_numbers.append(num**2)
#
# endt=datetime.datetime.now()
# st=datetime.datetime.now()
# squared_numbers = [num**2 for num in range(0,1000)]
# endt=datetime.datetime.now()
# data=["increment_01","increment_02","increment_03","increment_04","increment_05","increment_06"]


from firebase_admin import firestore
import firebase_admin

from firebase_admin import credentials
cred = credentials.Certificate('empoyee-payroll-system-firebase-adminsdk-5h89d-1602329ca8.json')
firebase_app = firebase_admin.initialize_app(cred)


db = firestore.client()
collection_ref = db.collection('alian_software_dev').document('employee').collection('employee')

# Get all documents from the collection
documents = collection_ref.stream()

tds_detail = {
    'hlapplicationno': 0,
    'hlamount': 0,
    'hlperiod': '2 year',
    'hlname': 'name',
    'hlannual': '5%',
    'pino': 0,
    'piname': 'name',
    'piannual': 0,
    'hipno': 0,
    'hipname': "name",
    'hipannual': 0,
    'hisno': 0,
    'hisname': 'XYZ',
    'hisannual': 0,
    'hifno': 0,
    'hifname': 'Father',
    'hifannual': 0,
    'ihlannual': 0,
    'ihlpanlender': 'JHHD56556',
    'ihlname': "0",
    'ahrmonth': 0,
    'ahrlandpann': 'NJHVJ6556S',
    'ahrlandname': 'Ankit',
    'ahrlandaddress': 'Nadiad',
    'elssannual': 0,
    'tfannual': 0,

}
# Iterate over the documents and print their IDs
for doc in documents:
    document_ref = collection_ref.document(doc.id)
    print(doc.id)
    # document_ref.update({'userID': doc.id})
    document_ref.collection('tdsmst').document('tds').update(tds_detail)
