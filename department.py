import re
from firebase_admin import credentials
from firebase_admin import firestore
import concurrent.futures

# cred = credentials.Certificate('empoyee-payroll-system-firebase-adminsdk-5h89d-1602329ca8.json')
#
# db = firestore.client()


class Department:
    def __init__(self, db):
        self.db = db

    def _process_department(self, companyname, data):

        doc_ref = self.db.collection(companyname).document(u'department')

        is_available = False

        for key, value in doc_ref.get().to_dict().items():
            if key == data['deptname'] and value != {}:
                is_available = True
                break

        if is_available == True and len(data) == 3:
            doc_ref.update({f'{data["deptname"]}.{data["pos0"]}': data['sal0']})
        elif is_available == True and len(data) > 3:
            pos = []
            sal = []
            deptnm = ''
            for key, value in data.items():
                if key == 'deptname':
                    deptnm = value
                elif re.findall("^pos", key):
                    pos.append(value)
                elif re.findall("^sal", key):
                    sal.append(value)
            data_2 = {p: s for p, s in zip(pos, sal)}

            for i,j in data_2.items():
                doc_ref.update({f'{deptnm}.{i}': j})
        else:
            pos = []
            sal = []
            deptnm = ''
            for key, value in data.items():
                if key == 'deptname':
                    deptnm = value
                elif re.findall("^pos", key):
                    pos.append(value)
                elif re.findall("^sal", key):
                    sal.append(value)
            data = {p: s for p, s in zip(pos, sal)}

            doc_ref.update({deptnm: data})

    def add_department(self,companyname, result):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self._process_department,companyname, result)
    def delete_department(self,companyname, dept, pos):
        doc_ref = self.db.collection(companyname).document(u'department')
        position = dept + '.' + pos
        doc_ref.update({position: firestore.DELETE_FIELD})
        if doc_ref.get().to_dict()[dept] == {}:
            doc_ref.update({dept: firestore.DELETE_FIELD})
