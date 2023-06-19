from flask import request
from firebase_admin import credentials,  auth, exceptions, firestore
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

        # if employee_data == None:
        #     last_id = 0
        # else:
        #     last_id = int(employee_data[-1].to_dict()['userID'][3:])
        #
        # new_id = ''
        #
        # if last_id < 9:
        #     new_id = "EMP000" + str(last_id + 1)
        # elif last_id < 99:
        #     new_id = "EMP00" + str(last_id + 1)
        # elif last_id < 999:
        #     new_id = "EMP0" + str(last_id + 1)

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



            user = auth.create_user(email=request.form.get('workEmail'), password=request.form.get('password'))
            print(user.uid)
            personal_data = {
                'employeeName': request.form.get('name'), 'userID': user.uid, 'department': request.form.get('department'),
                'email': request.form.get('email'),
                'role':  request.form.get('role'),
                'password':request.form.get('password'),
                "cosecID":request.form.get('cosecID'),
                'salary': float(request.form.get('salary')), 'jobPosition': request.form.get('jobPosition'),
                'doj': request.form.get('doj'),'designation':request.form.get('designation'),
                'currentExperience': f"{request.form.get('currentExperience')}",'workEmail':request.form.get('workEmail'), 'dob': request.form.get('dob'),
                'gender': request.form.get('gender'), 'phoneNo': request.form.get('mobileno'),
                'emergencyNumber': request.form.get('emergencyNumber'),
                'relationWithPerson': request.form.get('relationWithPerson'),
                'bankName': request.form.get('bankname'), 'accountHolderName': request.form.get('accountholdername'),
                'accountNumber': request.form.get('accountno'), 'ifscCode': request.form.get('ifsccode'),
                'branchName': request.form.get('branchName'),
                'aadharCardNo': request.form.get('aadharno'), 'panCardNo': request.form.get('panno'),
                'passportNo': request.form.get('passportno'), 'epfo_status': request.form.get('epfo'),
                'pfAccountNo': request.form.get('pfAccountNo'), 'uanNo': request.form.get('esicNo'), 'esicNo': request.form.get('passportno'),
                'abry': request.form.get('abry')
            }
            # print(personal_data)
            self.db.collection(self.companyname).document(u'employee').collection('employee').document(user.uid).set(personal_data)

            # ADD LEAVE DATA

            leave_data = {

                'total_leaves': {'CL': 0, 'PL': 0, 'SL': 0, 'LWP': 0}
            }

            self.db.collection(self.companyname).document(u'employee').collection('employee').document(user.uid).collection("leaveMST").document("total_leaves").set(leave_data["total_leaves"])
            doc_ref = self.db.collection(self.companyname).document('increments')
            if request.form.get('doj') !=None and request.form.get('doj')!='':
                doc_ref.update({'increments': firestore.ArrayUnion([{'empid': user.uid,
                                                                     'effectiveDate': request.form.get('doj'),
                                                                     'total': float(request.form.get('salary')/12),
                                                                     'grossSalary':0
                                                                     }])})

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
                    'hlStartDate': request.form.get('hlStartDate'),
                    'hlEndDate': request.form.get('hlEndDate'),
                    'hlname': request.form.get('hlname'),
                    'hlannual': request.form.get('hlannual'),
                    'pino': request.form.get('pino'),
                    'piname': request.form.get('piname'),
                    'piannual': request.form.get('piannual'),
                    'hipno': request.form.get('hipno'),
                    'hipname': request.form.get('hipname'),
                    'hipannual': request.form.get('hipannual'),
                    'hipStartDate': request.form.get('hipStartDate'),
                    'hipEndDate': request.form.get('hipEndDate'),
                    'hisno': request.form.get('hisno'),
                    'hisname': request.form.get('hisname'),
                    'hisannual': request.form.get('hisannual'),
                    'hisStartDate': request.form.get('hisStartDate'),
                    'hisEndDate': request.form.get('hisEndDate'),
                    'hifno': request.form.get('hifno'),
                    'hifname': request.form.get('hifname'),
                    'hifannual': request.form.get('hifannual'),
                    'hifStartDate': request.form.get('hifStartDate'),
                    'hifEndDate': request.form.get('hifEndDate'),
                    'ihlannual': request.form.get('ihlannual'),
                    'ihlpanlender': request.form.get('ihlpanlender'),
                    'ihlname': request.form.get("ihlname"),
                    'ahrmonth': request.form.get("ahrmonth"),
                    'ahrlandpann': request.form.get("ahrlandpann"),
                    'ahrStartDate': request.form.get("ahrStartDate"),
                    'ahrEndDate': request.form.get("ahrEndDate"),
                    'ahrlandname': request.form.get("ahrlandname"),
                    'ahrlandaddress': request.form.get("ahrlandaddress"),
                    'elssannual': request.form.get("elssannual"),
                    'elssStartDate': request.form.get("elssStartDate"),
                    'elssEndDate': request.form.get("elssEndDate"),
                    'tfannual': request.form.get("tfannual"),
                    'tfStartDate': request.form.get("tfStartDate"),
                    'tfEndDate': request.form.get("tfEndDate")

            }
            self.db.collection(self.companyname).document(u'employee').collection('employee').document(user.uid).collection("tdsmst").document("tds").set(tds_detail)

            return True