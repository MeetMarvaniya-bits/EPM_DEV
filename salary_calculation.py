import calendar
import datetime
from tds_data import TDSData


class SalaryCalculation():

    def __init__(self,db,companyname):
        self.db = db
        self.companyname=companyname

    def generate_salary(self, workingday):

        working_days = workingday

        current_month =datetime.datetime.today().month

        if current_month == 1:
            month = 13 - current_month
        else:
            month = current_month - 1

        year = datetime.datetime.now().year

        if current_month == 1:
            year = year - 1
        else:
            year = year

        salary_percentage = (self.db.collection(self.companyname).document('salary_calc').get()).to_dict()

        employee_list = {}

        docs = self.db.collection(self.companyname).document(u'employee').collection('employee').stream()
        for doc in docs:

            if 'user_status' not in doc.to_dict():
                self.db.collection(self.companyname).document('employee').collection('employee').document(doc.id).collection(
                    'salaryslips').document(f'sal00{current_month-1}').delete()
                employee_list.update({doc.id: doc.to_dict()})
            elif doc.to_dict()['user_status'] != 'disable':
                self.db.collection(self.companyname).document('employee').collection('employee').document(doc.id).collection(
                    'salaryslips').document(f'sal00{current_month-1}').delete()
                employee_list.update({doc.id: doc.to_dict()})
            else:
                self.db.collection(self.companyname).document('employee').collection('employee').document(doc.id).collection(
                    'salaryslips').document(f'sal00{current_month-1}').delete()

        for employee in employee_list:
            print(employee)

        for key, value in employee_list.items():

            empid = key

            emp_data = value

            emp_name = emp_data['employeeName']

            emp_salary = emp_data['salary'] / 12

            total_leaves = (self.db.collection(self.companyname).document('employee').collection('employee').document(
                empid).collection('leaveMST').document('total_leaves').get()).to_dict()

            lwp = total_leaves['LWP']

            emp_basic_salary = round(float(emp_salary * 0.5), 2)

            if emp_salary >= 15000:

                emp_hra = 7500

                emp_da = 0

                other_allowance = emp_salary - emp_basic_salary - emp_hra - emp_da

            else:

                emp_hra = emp_salary - emp_basic_salary

                emp_da = 0

                other_allowance = emp_salary - emp_basic_salary - emp_hra - emp_da

            incentive = 0

            arrears = 0

            grs_outstanding_adjustment = 0

            statutory_bns = 0

            gross_salary = round((emp_basic_salary + emp_hra + emp_da + other_allowance + incentive + arrears + grs_outstanding_adjustment + statutory_bns), 2)

            if emp_salary <= 22000:
                epfo = round(((emp_salary - emp_hra) * 0.24), 2)

                if epfo <= 3600:
                    epfo=epfo
                else:
                    epfo=3600

            else:

                epfo = 3600

            ded_outstanding_adjustment = 0

            pt = 200

            tds = TDSData(db=self.db).deduction(id=empid,epfo=epfo,companyname=self.companyname)

            other_deduction = 0

            if lwp > 0:
                leave_deduction = lwp * (round((float(emp_salary)/working_days * float(salary_percentage['deductionpercentage'])), 2))
            else:
                leave_deduction = 0

            total_deduction = round((epfo + ded_outstanding_adjustment + pt + tds + other_deduction + leave_deduction), 2)

            net_salary = round((gross_salary - total_deduction), 2)

            salary_slip_data = {
                'employeeName': emp_name, 'userID': empid,'slip_id': f'sal00{current_month-1}', 'lwp': lwp,
                'basic': emp_basic_salary, 'da': emp_da, 'hra': emp_hra, 'otherAllowance': other_allowance,
                'incentive': incentive, 'grsOutstandingAdjustment': grs_outstanding_adjustment, 'arrears': arrears,
                'statutoryBonus': statutory_bns, 'grossSalary': gross_salary, 'epfo': epfo,
                'dedOutstandingAdjustment': ded_outstanding_adjustment, 'pt': pt, 'tds': tds,
                'otherDeduction': other_deduction, 'leaveDeduction': leave_deduction, 'totalDeduction': total_deduction,
                'netSalary': net_salary, 'month': month, 'year': year, 'cosecID': emp_data['cosecID'], 'WO': 0,
                'UL': 0, 'Auth_OT': "00:00", 'WrkHrs': "00:00", 'CL': 0, 'PL': 0, 'SL': 0
            }

            users_ref = self.db.collection(self.companyname).document('employee').collection('employee').document(empid)

            if current_month == 1:
                users_ref.collection('salaryslips').document(f'sal00{month}').set(salary_slip_data)
            else:
                users_ref.collection('salaryslips').document(f'sal00{month}').set(salary_slip_data)

            mont_in_num = int(month)
            month_name = calendar.month_name[mont_in_num]

            salary_status = {month_name: 'None'}

            self.db.collection(self.companyname).document('salary_status').update(salary_status)













