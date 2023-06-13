from mail import Mail
from moth_days import MonthCount

moth_count = MonthCount()
class Register():
    def __init__(self, db):
        self.db = db
        self.mail = Mail()

    def register(self, data=None):
        data_dict = {}
        for key, value in data.items():
            data_dict.update({key: value})

        docs = self.db.collection(data_dict['CompanyName']).get()
        if len(docs) > 0:

            return 'Already Company Registered'
        else:
            self.db.collection(data_dict['CompanyName']).document('admin').set(data_dict)
            self.db.collection(data_dict['CompanyName']).document('department').set({})
            self.db.collection(data_dict['CompanyName']).document('employee').set({})
            self.db.collection(data_dict['CompanyName']).document('month_data').set({})
            data={'dapercentage':30,'deductionpercentage':1,'hrapercentage':50}
            self.db.collection(data_dict['CompanyName']).document('salary_calc').set(data)
            self.db.collection(data_dict['CompanyName']).document('holidays').set({})
            self.db.collection(data_dict['CompanyName']).document('salary_status').set({})
            holidays = self.db.collection(data_dict['CompanyName']).document('holidays').get().to_dict()
            moath_data = moth_count.count(holidays)
            self.db.collection(data_dict['CompanyName']).document('month_data').set(moath_data)
            '''SEND ID PASS WORD MAIL'''
            self.mail.register_responce_mail(companyname=data_dict['CompanyName'], email=data_dict['AdminID'])
            return True
