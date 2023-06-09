import calendar
import datetime


class Profile:
    # GETTING ID
    def __init__(self,db, id, companyname):
        self.db = db
        self.id = id
        self.companyname = companyname

    # PERSONAL DATA
    def personal_data(self):
        users_ref = self.db.collection(self.companyname).document('employee').collection('employee').document(self.id).get()
        return users_ref.to_dict()

    # TDS DATA
    def tds_data(self):
        user_ref = self.db.collection(self.companyname).document(u'employee').collection('employee').document(str(self.id)).collection('tdsmst').document('tds').get()
        return user_ref.to_dict()

    # LEAVE DATA
    def leave_data(self):
        data = []
        user_ref = self.db.collection(self.companyname).document(u'employee').collection('employee').document(self.id).collection('leaveMST').document('total_leaves').get()
        data.append(user_ref.to_dict())
        user_ref = self.db.collection(self.companyname).document(u'employee').collection('employee').document(str(self.id)).collection('leaveMST').document('date').get()
        data.append(user_ref.to_dict())
        return data

    # DEPARTMENT DATA
    def department_data(self):
        user_ref = self.db.collection(self.companyname).document(u'department').get()
        return user_ref.to_dict()

    # SALARY DATA
    def salary_data(self):
        salary_status = self.db.collection(self.companyname).document(u'salary_status').get().to_dict()

        #print(salary_status)
        docs = self.db.collection(self.companyname).document(u'employee').collection('employee').document(
            str(self.id)).collection('salaryslips').stream()
        data_dict = {}
        for doc in docs:
            print(doc.to_dict())
            month_name = calendar.month_name[int(doc.id.split('_')[0][5:])]
            year=doc.id.split('_')[1]
            print(month_name)
            print(year)
            if salary_status[year][month_name]=='Paid':
                print(444)
                data_dict.update({doc.id: doc.to_dict()})
            else:
                pass
        print(data_dict)
        return data_dict
