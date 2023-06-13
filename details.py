import calendar
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
        salary_status=docs = self.db.collection(self.companyname).document(u'salary_status').get().to_dict()
        docs = self.db.collection(self.companyname).document(u'employee').collection('employee').document(
            str(self.id)).collection('salaryslips').stream()


        data_dict = {}
        for doc in docs:

            month_name = calendar.month_name[int(doc.id[5:])]
            if salary_status[month_name]=='Paid':
                data_dict.update({doc.id: doc.to_dict()})
        return data_dict
