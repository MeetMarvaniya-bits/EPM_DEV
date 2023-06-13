import concurrent.futures
from datetime import datetime
from multiprocessing.pool import ThreadPool


class Dashboard():
    def __init__(self, db):
        self.db = db

    import concurrent.futures

    def _get_employee_data(self, emp_doc):
        employee_data = {'name': emp_doc.get('employeeName'),
                         'dob': emp_doc.get('dob'),
                         'doj': emp_doc.get('doj'),
                         'leaves': {}}

        if employee_data['dob'] != '' or employee_data['dob'] == None:
            dob = datetime.strptime(employee_data['dob'].strip(), '%Y-%m-%d')
            if dob.month == datetime.today().month:
                employee_data['birthday'] = employee_data['dob']
        if employee_data['doj'] != '':

            doj = datetime.strptime(employee_data['doj'][:10], '%Y-%m-%d')
            # doj = datetime.strptime(employee_data['doj'], '%Y-%m-%d')
            if doj.month == datetime.today().month:
                years = datetime.today().year - doj.year
                if years>0:
                    employee_data['anniversary'] = {
                        'name': employee_data['name'],
                        'date': employee_data['doj'],
                        'years': years}
        leaves = emp_doc.reference.collection('leaveMST')
        total_leaves = 0
        for leave in leaves.stream():
            if leave.id != 'total_leaves':
                dt2 = datetime.today().date()
                apply_date = (leaves.document(leave.id).get()).to_dict()['applydate']
                print(apply_date)
                dt1 = datetime.strptime(apply_date, '%Y-%m-%d')
                print(dt1)
                print(dt2)
                diff = (dt2.year - dt1.year) * 12 + (dt2.month - dt1.month)
                if diff < 1:
                    employee_data['leaves'] = leave.get('fromdate')
            if leave.id != 'total_leaves':
                total_leaves += int(leave.get('days'))
        employee_data['total_leaves'] = total_leaves
        print(total_leaves)
        return employee_data

    def Dashboard_data(self, companyname):
        users_ref = self.db.collection(companyname).document('employee').collection('employee')
        employee_data = []
        with concurrent.futures.ThreadPoolExecutor() as executor:
            for emp_doc in users_ref.stream():
                employee_data.append(executor.submit(self._get_employee_data, emp_doc))
        employee_on_leave, total_leaves, employee_birthday, employee_anniversary = {}, {}, {}, {}
        for future in concurrent.futures.as_completed(employee_data):
            result = future.result()
            if 'birthday' in result:
                employee_birthday[result['name']] = result['birthday']
            if 'anniversary' in result:
                employee_anniversary[result['name']] = result['anniversary']
            if result['leaves']:
                employee_on_leave[result['name']] = result['leaves']
            total_leaves[result['name']] = result['total_leaves']
        return employee_on_leave, total_leaves, employee_birthday, employee_anniversary



    def all_data(self, companyname):
        user_ref = self.db.collection(companyname).document(u'employee').collection('employee')

        def count_employees():
            return int(len(user_ref.get()))

        def count_employees_by_designation(designation):
            return int(len(user_ref.where('designation', '==', designation).get()))

        def count_employees_on_probation():
            return count_employees_by_designation('Probation')

        def count_employees_on_training():
            return count_employees_by_designation('Interns')

        def count_employees_by_experience_range(start, end):
            return sum(
                [int(len(user_ref.where('currentExperience', '==', f'{i} year').get())) for i in range(start, end + 1)])

        def count_employees_by_department(dept):
            return str(int(len(user_ref.where('department', '==', dept).get())))

        def count_employees_by_salary_range(start, end):
            return int(len(user_ref.where('salary', '<=', end).where('salary', '>', start).get()))

        with ThreadPool(processes=6) as pool:
            results = pool.starmap_async(count_employees_by_experience_range, [(0, 1), (2, 3), (4, 5), (6, 10), (11, 20)])
            experience_counts = results.get()

            results = pool.map_async(count_employees_by_department,
                                     self.db.collection(companyname).document(u'department').get().to_dict().keys())

            department_counts = results.get()

            results = pool.starmap_async(count_employees_by_salary_range,
                                         [(0, 20000), (20000, 50000), (50000, 80000), (80000, 100000),
                                          (100000, float('inf'))])
            salary_counts = results.get()

        all_employees = {
            'total_employees': count_employees(),
            'emp_on_probation': count_employees_on_probation(),
            'emp_on_training': count_employees_on_training()
        }
        employee_overview = {
            'Internship': count_employees_by_designation('Interns'),
            'Trainee': count_employees_by_designation('Trainee'),
            'Employee': count_employees_by_designation('Employee'),
            'Probation': count_employees_by_designation('Probation'),
        }
        exprience_list = {
            '0 to 1': experience_counts[0],
            '1 to 3': experience_counts[1],
            '3 to 5': experience_counts[2],
            '5 to 10': experience_counts[3],
            'Above 10': experience_counts[4]
        }

        department_wise_emp = {}
        for dept, count in zip(self.db.collection(companyname).document(u'department').get().to_dict().keys(), department_counts):
            department_wise_emp.update({dept: count})
        salary_wise_emp = {
            '0 to 20 K': salary_counts[0],
            '20 to 50 K': salary_counts[1],
            '50 to 80 K': salary_counts[2],
            '80 to 100 K': salary_counts[3],
            '100 K +': salary_counts[4]
        }
        all_data_dashboard = {
            'all_employees': all_employees,
            'employee_overview': employee_overview,
            'exprience_list': exprience_list,
            'department': self.db.collection(companyname).document(u'department').get().to_dict().keys(),
            'department_wise_emp': department_wise_emp,
            'salary_wise_emp': salary_wise_emp
        }
        return all_data_dashboard
