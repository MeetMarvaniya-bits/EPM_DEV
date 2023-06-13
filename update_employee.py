import concurrent.futures


class Update_information():
    def __init__(self, db):
        self.db = db

    def update_personal_info(self, companyname, data, id):
        data_dict = {}
        for key, value in data.items():
            if value != '':
                if key=='salary':
                    value=float(value)
                data_dict.update({key: value})
        a = self.db.collection(companyname).document('employee').collection('employee').document(id).update(data_dict)


    def update_tds_info(self, companyname, data, id):
        data_dict = {}
        for key, value in data.items():
            if value != '':
                data_dict.update({key: value})
        self.db.collection(companyname).document('employee').collection('employee').document(id).collection(
            'tdsmst').document('tds').update(data_dict)

    def update_personal_info_concurrent(self,companyname, data_list):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.update_personal_info,companyname, data, id) for data, id in data_list]
            print(futures)
            for future in concurrent.futures.as_completed(futures):
                result = future.result()


    def update_tds_info_concurrent(self, data_list,companyname):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.update_tds_info, data,companyname, id) for data, id in data_list]
            for future in concurrent.futures.as_completed(futures):
                result = future.result()

