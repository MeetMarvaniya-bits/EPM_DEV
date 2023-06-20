from firebase_admin import firestore
import firebase_admin

from firebase_admin import credentials
cred = credentials.Certificate('empoyee-payroll-system-firebase-adminsdk-5h89d-1602329ca8.json')
firebase_app = firebase_admin.initialize_app(cred)

db = firestore.client()


def result():

    ''' ADD FORM DETAILS INTO DATABASE '''

    name_list = ["Jay", "Mayank", "Parth", "Jenil", "Gautam", "Het", "Harsh", "Hemang", "Sanit", "Mayur", "Smith", "Yash", "Vishal", "Sagar", "Rohan", "Sanit", "Abhay"]
    for num in range(0, len(name_list) + 1):

        name = name_list[num]

        id = num + 4

        if id < 10:
            new_id = "EMP000" + str(id)
        else:
            new_id = "EMP00" + str(id)


        # ADD PERSONAL DATA

        personal_data = {
            'employeeName': name, 'userID': new_id, 'department': 'Design',
            'email': f'{name}123@gmail.com', 'cosecID': 100 + num,
            'salary': 300000, 'jobPosition': 'Junior', 'passwor': f'{name}@1234',
            'designation': 'Employee', 'doj': '2023-04-03',
            'currentExperience': '3 year', 'dob': '1999-02-04', 'gender': 'male',
            'phoneNo': 35464531456,
            'bankName': 'BOB', 'accountHolderName': name,
            'accountNumber': '3561654653416541341',
            'ifscCode': 'BANKIFSC12',
            'aadharCardNo': 6546541654464, 'panCardNo': 'BNDJC4544D',
            'passportNo': 57847857878,
            'pfAccountNo': 'MABAN00000640000000125', 'uanNo': 100904319456, 'esicNo': 31001234560000001
        }
        db.collection(u'alian_software').document(u'employee').collection('employee').document(new_id).set(personal_data)

        # ADD LEAVE DATA

        total_leaves = {'CL': 0, 'PL': 0, 'SL': 0, 'LWP': 0}

        db.collection(u'alian_software').document(u'employee').collection('employee').document(new_id).collection(
            "leaveMST").document("total_leaves").set(total_leaves)

        # ADD TDS DATA

        tds_detail = {
            'hlapplicationno': 6548656,
            'hlamount': 20000,
            'hlperiod': '2 year',
            'hlname': name,
            'hlannual': '5%',
            'pino': 5454464,
            'piname': name,
            'piannual': 3545,
            'hipno': 466545,
            'hipname': name,
            'hipannual': 4545,
            'hipperiod': '2023 to 2024',
            'hisno': 6563,
            'hisname': 'XYZ',
            'hisannual': 2126,
            'hisperiod': '2023 to 2024',
            'hifno': 446556,
            'hifname': 'Father',
            'hifannual': 5464,
            'hifperiod': '2023 to 2024',
            'ihlannual': 2000,
            'ihlpanlender': 'JHHD56556',
            'ihlname': name,
            'ahrmonth': 2000,
            'ahrlandpann': 'NJHVJ6556S',
            'ahrperiod': '2023 to 2024',
            'ahrlandname': 'Ankit',
            'ahrlandaddress': 'Nadiad',
            'elssannual': 500,
            'elssperiod': '2023 to 2024',
            'tfannual': 1000,
            'tfperiod': '2023 to 2024'
        }


        db.collection(u'alian_software').document(u'employee').collection('employee').document(new_id).collection("tdsmst").document("tds").set(tds_detail)

# result()