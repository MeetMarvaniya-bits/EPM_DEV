class Login():
    def __init__(self, db):
        self.db = db
        pass

    def login(self, data, comapyname):
        data_dict = {}
        for key, value in data.items():
            data_dict.update({key: value})
        docs = self.db.collection(comapyname).get()

        if len(docs) > 0:
            docs = self.db.collection(comapyname).document('admin').get().to_dict()

            if len(docs)>0:

               if (docs['AdminID'] == data_dict['email']) and str((docs['password']) == str(data_dict['password'])):

                   return 'Admin'
        doc = self.db.collection(comapyname).document("employee").collection('employee').where('userID', "==",data_dict['email']).where('password', "==", str(data_dict['password'])).get()
        # docs = self.db.collection("alian_software").document("employee").collection('employee').where('email', "==", data_dict['email'] ).where('password',"==",str(data_dict['password'])).get()

        len(doc)

        if len(doc) > 0:

            if doc[0].to_dict()['department']=='HR':
                return {"name":doc[0].to_dict()['employeeName'],"type":'HR'}
            else:
                return {"name":doc[0].to_dict()['employeeName'],"type":'Employee',"empid":doc[0].to_dict()['userID']}
        return False