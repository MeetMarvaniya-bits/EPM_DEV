import concurrent.futures
from concurrent.futures import ThreadPoolExecutor
import datetime


class Salarymanage():
    def __init__(self, db):
        self.db = db

    def salary_update(self, companyname, empid, salid, data=None):

        data_dict = {}
        for key, value in data.items():
            data_dict.update({key: value})
        self.db.collection(companyname).document('employee').collection('employee').document(empid).collection(
            'salaryslips').document(salid).update(data_dict)


    from concurrent.futures import ThreadPoolExecutor

    def process_employee(self, emp, companyname):
        docs = self.db.collection(companyname).document(u'employee').collection('employee')
        salary_list = {}
        salary_data = docs.document(str(emp.id)).collection('salaryslips').stream()
        for doc in salary_data:
            salary_list.update({doc.id: doc.to_dict()})
        return {emp.id: salary_list}

    def calculate_salary_data(self, employee_salary):
        salary_data = {}
        for i in employee_salary:
            for j in employee_salary[i]:
                if j == "salid":
                    continue
                if j not in salary_data.keys():
                    salary_data.update({j: {
                        'netSalary': 0,
                        'grossSalary': 0,
                        'epfo': 0,
                        'pt': 0,
                        'tds': 0,
                    }})
                if j != "salid":
                    salary_data.update({j: {
                        'netSalary': round(salary_data[j]['netSalary'] + float(employee_salary[i][j]["netSalary"]), 2),
                        'grossSalary': round(salary_data[j]['grossSalary'] + float(employee_salary[i][j]["grossSalary"]), 2),
                        'epfo': round(salary_data[j]['epfo'] + float(employee_salary[i][j]["epfo"]), 2),
                        'pt': round(salary_data[j]['pt'] + float(employee_salary[i][j]["pt"]), 2),
                        'tds': round((salary_data[j]['tds'] + float(employee_salary[i][j]["tds"])),2)
                    }})
        return salary_data

    def get_all_month_salary_data(self, companyname):
        docs = self.db.collection(companyname).document(u'employee').collection('employee')
        employee_salary = {}
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.process_employee,emp, companyname) for emp in docs.stream()]
            for future in futures:
                employee_salary.update(future.result())

        salary_data = self.calculate_salary_data(employee_salary)
        return salary_data

    def get_all_emp_salary_data(self, companyname, salid):
        employee_salary = {}
        docs = self.db.collection(companyname).document(u'employee').collection('employee').stream()
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = [executor.submit(self.get_employee_salary_data, companyname, emp.id, salid) for emp in docs]
            for future in concurrent.futures.as_completed(results):
                emp_id, salary_data = future.result()
                if salary_data is not None:
                    employee_salary.update({emp_id: salary_data})
        return employee_salary

    def get_employee_salary_data(self, companyname, emp_id, salid):
        salary_data = self.db.collection(companyname).document(u'employee').collection('employee').document(
            str(emp_id)).collection('salaryslips').document(salid).get().to_dict()
        return emp_id, salary_data

    def get_salary_data(self, companyname, empid, salid):
        doc = self.db.collection(companyname).document('employee').collection('employee').document(empid).collection(
            'salaryslips').document(salid).get()
        data_dict = {}
        data_dict.update({doc.id: doc.to_dict()})
        return data_dict
