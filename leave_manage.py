import datetime
import concurrent.futures

class Leavemanage():
    def __init__(self, db):
        self.db = db

    def leave_add(self, companyname):
        docs = self.db.collection(companyname).document(u'employee').collection('employee')
        for doc in docs.get():
            leaves_ref = docs.document(doc.id).collection('leaveMST').document('total_leaves')
            leaves = leaves_ref.get().to_dict()
            leaves_ref.set({
                'SL': (float(leaves['SL']) + 0.5),
                'PL': (float(leaves['PL']) + 1),
                'CL': (float(leaves['CL']) + 0.5),
                'LWP':0
            })

    def leave_reset(self, companyname):
        docs = self.db.collection(companyname).document(u'employee').collection('employee')
        for doc in docs.get():
            leaves_ref = docs.document(doc.id).collection('leaveMST').document('total_leaves')
            leaves = leaves_ref.get().to_dict()
            leaves_ref.set({
                'SL': 0.5,
                'PL': 1,
                'CL': 0.5,
                'LWP':0

            })

    def take_leave(self, ref_obj, data=None):
        if data == None:
            print('Error')
        else:
            data_dict = {}
            leaves = ref_obj.document('total_leaves').get().to_dict()
            for key, value in data.items():
                data_dict.update({key: value})

            if int(leaves[data_dict['type']]) - int(data_dict['days']) >= 0:
                ref_obj.document('total_leaves').update({
                    data_dict['type']: (leaves[data_dict['type']] - int(data_dict['days']))
                })
            else:

                ref_obj.document('total_leaves').update({
                    'LWP': (leaves['LWP'] + int(data_dict['days'])-int(leaves[data_dict['type']])),
                                                data_dict['type']:0
                })
            
            leave_id = len(ref_obj.get())
            print(data_dict)
            if leave_id < 9:
                doc_name = f'leave00{leave_id}'
            else:
                doc_name = f'leave0{leave_id}'
            data = ref_obj.document(doc_name).set(data_dict)

    def take_leave_edit(self, ref_obj, data=None):
        if data == None:
            print('Error')
        else:
            data_dict = data
            leaves = ref_obj.document('total_leaves').get().to_dict()
            if int(leaves[data_dict['type']]) - int(data_dict['days']) > 0:
                ref_obj.document('total_leaves').update({
                    data_dict['type']: (leaves[data_dict['type']] - int(data_dict['days']))
                })
            else:
                ref_obj.document('total_leaves').update({
                    'LWP': (leaves['LWP'] + int(data_dict['days']))
                })

            leave_id = len(ref_obj.get())
            print(data_dict)
            doc_name = (f'leave00{leave_id}')
            data = ref_obj.document(doc_name).set(data_dict)

    def get_total_leave(self, ref_obj):
        data = ref_obj.document('total_leaves').get()
        data= data.to_dict()
        return data

    def leave_list(self, ref_obj):
        docs = ref_obj.stream()
        data_dict = {}
        for doc in docs:
            data_dict.update({doc.id: doc.to_dict()})
        return data_dict

    def process_leave_add(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.leave_add)

    def process_take_leave(self, ref_obj, data=None):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.take_leave, ref_obj, data)

    def process_take_leave_edit(self, ref_obj, data=None):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(self.take_leave_edit, ref_obj, data)

    def process_get_total_leave(self, ref_obj):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.get_total_leave, ref_obj)
            return future.result()

    def process_leave_list(self, ref_obj):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(self.leave_list, ref_obj)
            return future.result()
