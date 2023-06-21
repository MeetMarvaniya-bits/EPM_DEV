from mail import Mail
import json
import requests
from firebase_admin import credentials,  auth, exceptions, firestore
from flask import request

class Admin_Register():
    def __init__(self, db):
        self.db = db
        self.mail = Mail(db)

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
        return True
