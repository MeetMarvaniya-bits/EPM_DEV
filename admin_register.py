from mail import Mail
import json
import requests
from firebase_admin import credentials,  auth, exceptions, firestore
from flask import request

class Admin_Register():
    def __init__(self, db):
        self.db = db
        self.mail = Mail()

    def admin_register(self, data=None, companyname=None):
        data_dict = {}
        for key, value in data.items():
            data_dict.update({key: value})

        user = auth.create_user(email=request.form.get('workEmail'), password=request.form.get('password'))
        set_data = {
            **data_dict,
            "role":"Admin",
            "name":"Admin",
            "userID":user.uid
        }
        self.db.collection(companyname).document("employee").collection('employee').document(user.uid).set(set_data)
        print(user.uid)
        return True

        # docs = self.db.collection(data_dict['CompanyName']).get()
        # if len(docs) > 0:
        #
        #     return 'Already Company Registered'
        # else:
        #     self.db.collection(data_dict['CompanyName']).document('admin').set(data_dict)
        #     self.db.collection(data_dict['CompanyName']).document('department').set({})
        #     self.db.collection(data_dict['CompanyName']).document('employee').set({})
        #     self.db.collection(data_dict['CompanyName']).document('month_data').set({})
        #     data={'dapercentage':30,'deductionpercentage':1,'hrapercentage':50}
        #     self.db.collection(data_dict['CompanyName']).document('salary_calc').set(data)
        #     self.db.collection(data_dict['CompanyName']).document('holidays').set({})
        #     self.db.collection(data_dict['CompanyName']).document('salary_status').set({})
        #     holidays = self.db.collection(data_dict['CompanyName']).document('holidays').get().to_dict()
        #     self.db.collection(data_dict['CompanyName']).document('month_data').set(moath_data)
        #     '''SEND ID PASS WORD MAIL'''
        #     self.mail.register_responce_mail(companyname=data_dict['CompanyName'], email=data_dict['AdminID'])
        #     return True
