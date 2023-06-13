from flask import request
from firebase_admin import credentials, storage
import firebase_admin
from PIL import Image
import base64
import datetime
from io import BytesIO


cred = credentials.Certificate('empoyee-payroll-system-firebase-adminsdk-5h89d-1602329ca8.json')
firebase_app = firebase_admin.initialize_app(cred, {
    'storageBucket': 'empoyee-payroll-system.appspot.com'
})


class Create():

    def __init__(self,db,companyname):
        self.db=db
        self.companyname=companyname

    def result(self):

        ''' ADD FORM DETAILS INTO DATABASE '''

        employee_data = (self.db.collection(self.companyname).document('employee').collection('employee').get())

        if employee_data == None:
            last_id = 0
        else:
            last_id = int(employee_data[-1].to_dict()['userID'][3:])

        new_id = ''

        if last_id < 9:
            new_id = "EMP000" + str(last_id + 1)
        elif last_id < 99:
            new_id = "EMP00" + str(last_id + 1)
        elif last_id < 999:
            new_id = "EMP0" + str(last_id + 1)

        if request.method == 'POST':
            # file = request.files['photo']
            # bucket = storage.bucket()
            # blob = bucket.blob(f'{new_id}_{file.filename}')
            # blob.upload_from_file(file)
            # blob = bucket.blob(f'{new_id}_{file.filename}')
            # image_data = blob.download_as_bytes()
            # # Convert image bytes to base64 encoded string
            # image_b64 = base64.b64encode(image_data).decode('utf-8')
            #
            # image = f"data:image/jpeg;base64,{ image_b64 }"
            # 'photo': image,

            personal_data = {
                'employeeName': request.form.get('name'), 'userID': new_id, 'department': request.form.get('department'),
                'email': request.form.get('email'),
                'password':request.form.get('password'),
                'salary': float(request.form.get('salary')), 'jobPosition': request.form.get('jobPosition'),
                'doj': request.form.get('doj'),'designation':request.form.get('designation'),
                'currentExperience': f"{request.form.get('currentExperience')} year", 'dob': request.form.get('dob'),
                'gender': request.form.get('gender'), 'phoneNo': request.form.get('mobileno'),
                'bankName': request.form.get('bankname'), 'accountHolderName': request.form.get('accountholdername'),
                'accountNumber': request.form.get('accountno'), 'ifscCode': request.form.get('ifsccode'),
                'aadharCardNo': request.form.get('aadharno'), 'panCardNo': request.form.get('panno'),
                'passportNo': request.form.get('passportno'),
                'pfAccountNo': 'MABAN00000640000000125', 'uanNo': '100904319456', 'esicNo': '31–00–123456–000–0001'
            }
            self.db.collection(self.companyname).document(u'employee').collection('employee').document(new_id).set(personal_data)

            # ADD LEAVE DATA

            leave_data = {

                'total_leaves': {'CL': 0, 'PL': 0, 'SL': 0, 'LWP': 0}
            }

            self.db.collection(self.companyname).document(u'employee').collection('employee').document(new_id).collection("leaveMST").document("total_leaves").set(leave_data["total_leaves"])

            # ADD SALARY DATA
            # salary_slip_data = {
            #     'employeeName': request.form.get('name'), 'userID': new_id, 'slip_id': '', 'lwp': "", 'basic': "", 'da': "", 'hra': "", 'otherAllowance': "",
            #     'incentive': "", 'outstandingAdjustment': "", 'arrears': "", 'statutoryBonus': '',
            #     'grossSalary': "", 'epfo': "", 'outstandingAdjustments': "", 'pt': "",
            #     'tds': "", 'otherDeduction': "", 'leaveDeduction': "",'totalDeduction': "", 'netSalary': ""
            # }
            # self.db.collection('alian_software').document('employee').collection('employee').document(new_id).collection('salaryslips').document(f"sal00{datetime.datetime.now().month}").set(salary_slip_data)

            # salary_slip_data = {
            #     'employeeName': request.form.get('name'), 'userID': new_id,'slip_id': '', 'lwp': "", 'basic': "", 'da': "", 'hra': "", 'otherAllowance': "",
            #     'incentive': "", 'grsOutstandingAdjustment': "", 'arrears': "", 'statutoryBonus': '',
            #     'grossSalary': "", 'epfo': "", 'dedOutstandingAdjustment': "", 'pt': "",
            #     'tds': "", 'otherDeduction': "", 'leaveDeduction': "",'totalDeduction': "", 'netSalary': "",'month':'','year':''
            # }
            # db.collection(u'alian_software').document('employee').collection('employee').document(new_id).collection('salaryslips').document("slipid").set(salary_slip_data)

            # ADD TDS DATA
            tds_detail = {
                    'hlapplicationno': request.form.get('hlapplicationno'),
                    'hlamount': request.form.get('hlamount'),
                    'hlperiod': request.form.get('hlperiod'),
                    'hlname': request.form.get('hlname'),
                    'hlannual': request.form.get('hlannual'),
                    'pino': request.form.get('pino'),
                    'piname': request.form.get('piname'),
                    'piannual': request.form.get('piannual'),
                    'hipno': request.form.get('hipno'),
                    'hipname': request.form.get('hipname'),
                    'hipannual': request.form.get('hipannual'),
                    'hipperiod': request.form.get('hipperiod'),
                    'hisno': request.form.get('hisno'),
                    'hisname': request.form.get('hisname'),
                    'hisannual': request.form.get('hisannual'),
                    'hisperiod': request.form.get('hisperiod'),
                    'hifno': request.form.get('hifno'),
                    'hifname': request.form.get('hifname'),
                    'hifannual': request.form.get('hifannual'),
                    'hifperiod': request.form.get('hifperiod'),
                    'ihlannual': request.form.get('ihlannual'),
                    'ihlpanlender': request.form.get('ihlpanlender'),
                    'ihlname': request.form.get("ihlname"),
                    'ahrmonth': request.form.get("ahrmonth"),
                    'ahrlandpann': request.form.get("ahrlandpann"),
                    'ahrperiod': request.form.get("ahrperiod"),
                    'ahrlandname': request.form.get("ahrlandname"),
                    'ahrlandaddress': request.form.get("ahrlandaddress"),
                    'elssannual': request.form.get("elssannual"),
                    'elssperiod': request.form.get("elssperiod"),
                    'tfannual': request.form.get("tfannual"),
                    'tfperiod': request.form.get("tfperiod")
            }
            self.db.collection(self.companyname).document(u'employee').collection('employee').document(new_id).collection("tdsmst").document("tds").set(tds_detail)

            return new_id