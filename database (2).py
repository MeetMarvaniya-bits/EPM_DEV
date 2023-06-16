import datetime

from firebase_admin import firestore
import firebase_admin

from firebase_admin import credentials
cred = credentials.Certificate('empoyee-payroll-system-firebase-adminsdk-5h89d-1602329ca8.json')

firebase_app = firebase_admin.initialize_app(cred)

db = firestore.client()

# company_name = 'New_Company_11111'

#
# # db.collection('alian_software').document('admin').update({'auth_password': 'wlcuavwqcnwjfajj'})
#
# data = db.collection('alian_software').document('admin').get().to_dict()
#
# print(data)
#
# db.collection(company_name).document('admin').set('')
# db.collection(company_name).document('department').set('')
# db.collection(company_name).document('employee').collection('employee').document('EMP0001').set('')
# db.collection(company_name).document('employee').collection('employee').document('EMP0001').collection('tdsmst').document('tds').set('')
# db.collection(company_name).document('holidays').set('')
# db.collection(company_name).document('month_data').set('')
# db.collection(company_name).document('salary_calc').set('')
# db.collection(company_name).document('salary_status').set('')
#
# db.collection(company_name).document('salaryslips').collection('salaryslips').document('EMP0001_sal001').set('')
#
# db.collection(company_name).document('leaveMST').collection('leaveMST').document('EMP0001_total_leave').set('')
# db.collection(company_name).document('leaveMST').collection('leaveMST').document('EMP0001_leave001').set('')
# db.collection(company_name).document('tdsMST').collection('tdsMST').document('EMP0001_tds').set('')





# db.collection(company_name).document(company_name).collection('admin').document().set('')
# db.collection(company_name).document(company_name).collection('department').document('departmentnamegoeshere').set('')
# db.collection(company_name).document(company_name).collection('employee').document('EMP0001').set('')
# db.collection(company_name).document(company_name).collection('holidays').document('holidays').set('')
# db.collection(company_name).document(company_name).collection('month_data').document('month_data').set('')
# db.collection(company_name).document(company_name).collection('salary_calc').document('salary_calc').set('')
# db.collection(company_name).document(company_name).collection('salary_status').document('salary_status').set('')
#
# db.collection(company_name).document(company_name).collection('salaryslips').document('EMP0001_sal001').set('')
#
# db.collection(company_name).document(company_name).collection('leaveMST').document('EMP0001_total_leave').set('')
# db.collection(company_name).document(company_name).collection('leaveMST').document('EMP0001_leave001').set('')
# db.collection(company_name).document(company_name).collection('tdsMST').document('EMP0001_tds').set('')



# empid = 'EMP0002'
# companyname = 'alian_software'
#
# # # # For Increment
# increment_01 = {'increment_02': {
#     'grossSalary': 53000.00,
#     'jobPosition': 'SR.UI/UX Designer',
#     'effectiveDate': 'May 28, 2023',
#     'increment': 16000.00,
#     'total': 63600.00,
#     'note': 'This is an first increment'
# }
# }
# db.collection(companyname).document(u'employee').collection('employee').document(empid).update(increment_01)
#
# # # # For Contract
# contract_01 = {'contract_01': {
#     'contractDate': 'May 28, 2023',
#     'contractPeriod': '1 Year',
#     'nextContractDate': 'May 28, 2024'
# }
# }
# db.collection(companyname).document(u'employee').collection('employee').document(empid).update(contract_01)
#
# company_name  = 'meetSoftware'
# db.collection(company_name).document(company_name).collection('salaryslips').document('EMP001_sal001').set({'salary': 55555})
# db.collection(company_name).document(company_name).collection('salaryslips').document('EMP001_sal002').set({'salary': 55555})
# db.collection(company_name).document(company_name).collection('salaryslips').document('EMP001_sal003').set({'salary': 55555})
# db.collection(company_name).document(company_name).collection('salaryslips').document('EMP002_sal001').set({'salary': 55555})
# db.collection(company_name).document(company_name).collection('salaryslips').document('EMP002_sal002').set({'salary': 55555})
# db.collection(company_name).document(company_name).collection('salaryslips').document('EMP002_sal003').set({'salary': 55555})
# db.collection(company_name).document(company_name).collection('salaryslips').document('EMP003_sal001').set({'salary': 55555})
# db.collection(company_name).document(company_name).collection('salaryslips').document('EMP003_sal002').set({'salary': 55555})
# db.collection(company_name).document(company_name).collection('salaryslips').document('EMP003_sal003').set({'salary': 55555})

#
# data = db.collection(company_name).document(company_name).collection('salaryslips').stream()
#
# for doc in data:
#     if doc.id.startswith('EMP001'):
#         print(doc.id)
#         print(doc.to_dict())




# # # # # # # #  CREATE NEW EMPLOYEE CODE # # # # # # # # # # #
#
#
# from flask import request
# from firebase_admin import credentials, storage
# import firebase_admin
# from PIL import Image
# import base64
# import datetime
# from io import BytesIO
#
# cred = credentials.Certificate('empoyee-payroll-system-firebase-adminsdk-5h89d-1602329ca8.json')
# firebase_app = firebase_admin.initialize_app(cred, {
#     'storageBucket': 'empoyee-payroll-system.appspot.com'
# })
#
#
# class Create():
#
#     def __init__(self, db, companyname):
#         self.db = db
#         self.companyname = companyname
#
#     def result(self):
#
#         ''' ADD FORM DETAILS INTO DATABASE '''
#
#         employee_data = (self.db.collection(self.companyname).document('employee').collection('employee').get())
#
#         if employee_data == None:
#             last_id = 0
#         else:
#             last_id = int(employee_data[-1].to_dict()['userID'][3:])
#
#         new_id = ''
#
#         if last_id < 9:
#             new_id = "EMP000" + str(last_id + 1)
#         elif last_id < 99:
#             new_id = "EMP00" + str(last_id + 1)
#         elif last_id < 999:
#             new_id = "EMP0" + str(last_id + 1)
#
#         if request.method == 'POST':
#             # file = request.files['photo']
#             # bucket = storage.bucket()
#             # blob = bucket.blob(f'{new_id}_{file.filename}')
#             # blob.upload_from_file(file)
#             # blob = bucket.blob(f'{new_id}_{file.filename}')
#             # image_data = blob.download_as_bytes()
#             # # Convert image bytes to base64 encoded string
#             # image_b64 = base64.b64encode(image_data).decode('utf-8')
#             #
#             # image = f"data:image/jpeg;base64,{ image_b64 }"
#             # 'photo': image,
#
#             personal_data = {
#                 'employeeName': request.form.get('name'), 'userID': new_id,
#                 'department': request.form.get('department'),
#                 'email': request.form.get('email'),
#                 'password': request.form.get('password'),
#                 'salary': float(request.form.get('salary')), 'jobPosition': request.form.get('jobPosition'),
#                 'doj': request.form.get('doj'), 'designation': request.form.get('designation'),
#                 'currentExperience': f"{request.form.get('currentExperience')} year", 'dob': request.form.get('dob'),
#                 'gender': request.form.get('gender'), 'phoneNo': request.form.get('mobileno'),
#                 'bankName': request.form.get('bankname'), 'accountHolderName': request.form.get('accountholdername'),
#                 'accountNumber': request.form.get('accountno'), 'ifscCode': request.form.get('ifsccode'),
#                 'aadharCardNo': request.form.get('aadharno'), 'panCardNo': request.form.get('panno'),
#                 'passportNo': request.form.get('passportno'),
#                 'pfAccountNo': 'MABAN00000640000000125', 'uanNo': '100904319456', 'esicNo': '31–00–123456–000–0001'
#             }
#             self.db.collection(self.companyname).document(u'employee').collection('employee').document(new_id).set(
#                 personal_data)
#
#             tds_add = {
#                 'salary': personal_data['salary'],
#             }
#             self.db.collection(self.companyname).document(u'tdsmst').collection("tdsmst").document(f"{new_id}_tds").set(
#                 tds_add)
#
#             # ADD LEAVE DATA
#
#             leave_data = {
#
#                 'total_leaves': {'CL': 0, 'PL': 0, 'SL': 0, 'LWP': 0}
#             }
#
#             self.db.collection(self.companyname).document('leaveMST').collection('leaveMST').document(
#                 f'{new_id}_total_leave').set(leave_data["total_leaves"])
#
#             # ADD TDS DATA
#             tds_detail = {
#                 'hlapplicationno': request.form.get('hlapplicationno'),
#                 'hlamount': request.form.get('hlamount'),
#                 'hlperiod': request.form.get('hlperiod'),
#                 'hlname': request.form.get('hlname'),
#                 'hlannual': request.form.get('hlannual'),
#                 'pino': request.form.get('pino'),
#                 'piname': request.form.get('piname'),
#                 'piannual': request.form.get('piannual'),
#                 'hipno': request.form.get('hipno'),
#                 'hipname': request.form.get('hipname'),
#                 'hipannual': request.form.get('hipannual'),
#                 'hipperiod': request.form.get('hipperiod'),
#                 'hisno': request.form.get('hisno'),
#                 'hisname': request.form.get('hisname'),
#                 'hisannual': request.form.get('hisannual'),
#                 'hisperiod': request.form.get('hisperiod'),
#                 'hifno': request.form.get('hifno'),
#                 'hifname': request.form.get('hifname'),
#                 'hifannual': request.form.get('hifannual'),
#                 'hifperiod': request.form.get('hifperiod'),
#                 'ihlannual': request.form.get('ihlannual'),
#                 'ihlpanlender': request.form.get('ihlpanlender'),
#                 'ihlname': request.form.get("ihlname"),
#                 'ahrmonth': request.form.get("ahrmonth"),
#                 'ahrlandpann': request.form.get("ahrlandpann"),
#                 'ahrperiod': request.form.get("ahrperiod"),
#                 'ahrlandname': request.form.get("ahrlandname"),
#                 'ahrlandaddress': request.form.get("ahrlandaddress"),
#                 'elssannual': request.form.get("elssannual"),
#                 'elssperiod': request.form.get("elssperiod"),
#                 'tfannual': request.form.get("tfannual"),
#                 'tfperiod': request.form.get("tfperiod")
#             }
#             self.db.collection(self.companyname).document(u'tdsmst').collection("tdsmst").document(f"{new_id}_tds").update(tds_detail)
#


employee_list_with_increments = (db.collection('alian_software').document('increments').get()).to_dict()

current_month = datetime.datetime.now().month
result = []

for increment in employee_list_with_increments['increments']:
    effective_date = increment.get('effectiveDate')
    if effective_date:
        increment_month = int(effective_date.split('-')[1])
        if increment_month == current_month:
            result.append(increment)
print(result)



data = []
empid = 'EMP0032'
data = [d for d in result if d.get('empid') == 'EMP0031']

print(data)
print(data[0]['total'])