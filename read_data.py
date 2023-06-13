
import openpyxl
import datetime
import re
from concurrent.futures import ThreadPoolExecutor

class ExcelData():
    def __init__(self, db):
        self.db = db

    def process_employee_data(self, companyname, details):
        id = str(details['Employee ID'])
        if id == 'None':
            return
        else:
            month = datetime.datetime.now().month
            year = datetime.datetime.now().year
            doj = details['Date of Joining'].date()
            dob = details['Date of Birth'].date()

            personal_data = {
                'photo': 'photo',
                'employeeName': details['Employee Full Name'], 'userID': details['Employee ID'],
                'password': details['Password'], 'department': details['Department'],
                'email': details['Email'], 'salary': details['Salary'], 'jobPosition': details['Job Position'],
                'manager': details['Manager'], 'doj': f'{doj}',
                'currentExperience': details['Current Experience'], 'dob': f'{dob}',
                'gender': details['Gender'], 'phoneNo': details['Phone No'],
                'bankName': details['Bank Name'], 'accountHolderName': details['Account Holder Name'],
                'accountNumber': details['Account Number'], 'ifscCode': details['IFSC Code'],
                'aadharCardNo': details['Aadhar Card Number'], 'panCardNo': details['PAN Card No'],
                'passportNo': details['Passport No'],
                'pfAccountNo': details['PF Account No'], 'uanNo': details['UAN No'], 'esicNo': details['ESIC No']
            }
            self.db.collection(companyname).document(u'employee').collection('employee').document(id).set(personal_data)

            total_leaves = {'CL': details['CL'], 'PL': details['PL'], 'SL': details['SL'], 'LWP': details['LWP']}

            self.db.collection(companyname).document(u'employee').collection('employee').document(id).collection(
                "leaveMST").document("total_leaves").set(total_leaves)
            salary_slip_data = {
                'employeeName': details['Employee Full Name'], 'userID': details['Employee ID'],
                'slip_id': f'sal00{month}', 'lwp': details['LWP'], 'basic': details['Basic'], 'da': details['DA'],
                'hra': details['HRA'], 'otherAllowance': details['Other Allowance'],
                'incentive': details['Incentive'],
                'grsOutstandingAdjustment': details['Grs Outstanding Adjustment'],
                'arrears': details['Arrears'], 'statutoryBonus': details['Statutory Bonus'],
                'grossSalary': details['Gross Salary'], 'epfo': details['EPFO'],
                'dedOutstandingAdjustment': details['Ded Outstanding Adjustment'], 'pt': details['PT'],
                'tds': details['TDS'], 'otherDeduction': details['Other Deduction'],
                'leaveDeduction': details['Leave Deduction'], 'netSalary': details['Net Salary'], 'month': month,
                'year': year,
            }
            # self.db.collection(companyname).document('employee').collection('employee').document(id).collection(
            #     'salaryslips').document("sal00" + str({month})).set(salary_slip_data)
            tds_detail = {
                'hlapplicationno': details['Home Loan Application No'],
                'hlamount': details['Home Loan Amount'],
                'hlperiod': details['Period of Home Loan'],
                'hlname': details['Home Loan Person Name'],
                'hlannual': details['Home Loan Interest'],
                'pino': details['Premium Insurance Number'],
                'piname': details['Premium Person Name'],
                'piannual': details['Premium Annual Amount'],
                'hipno': details['Health Insurance (Self) No'],
                'hipname': details['Health Insurance (Self) Person Name'],
                'hipannual': details['Health Insurance (Self) Annual Amount'],
                'hipperiod': details['Health Insurance (Self) Period'],
                'hisno': details['Health Insurance (Spouse) No'],
                'hisname': details['Health Insurance (Spouse) Person Name'],
                'hisannual': details['Health Insurance (Spouse) Annual Amount'],
                'hisperiod': details['Health Insurance (Spouse) Period'],
                'hifno': details['Health Insurance (Father) No'],
                'hifname': details['Health Insurance (Father) person Name'],
                'hifannual': details['Health Insurance (Father) Annual Amount'],
                'hifperiod': details['Health Insurance (Father) Period'],
                'ihlannual': details['Interest on Home Loan Payable'],
                'ihlpanlender': details['interest of Home Loan PAN of Lender'],
                'ihlname': details['Interest of Home loan Person Name'],
                'ahrmonth': details['Annual House Rent of Current Month'],
                'ahrlandpann': details['Rent House Landloard PAN'],
                'ahrperiod': details['Rent House Period'],
                'ahrlandname': details['Rent House Landloard Name'],
                'ahrlandaddress': details['Rent House Landloard Address'],
                'elssannual': details['ELSS Annual Amount'],
                'elssperiod': details['ELSS Period'],
                'tfannual': details['Tution Fees Annual Amount'],
                'tfperiod': details['Tution Fees Period']
            }

            self.db.collection(companyname).document(u'employee').collection('employee').document(id).collection(
                "tdsmst").document("tds").set(tds_detail)

    def store_excel_data(self, companyname, path):
        # Load the Excel file
        wb = openpyxl.load_workbook(path)
        # Get the first sheet of the workbook
        sheet = wb.active
        # Convert the sheet list
        data = []
        for row in sheet.iter_rows(values_only=True):
            data.append(row)
        title_row = data[0]
        employee_data = []
        for n in range(1, len(data)):
            employee_details = list(data[n])
            employee_data.append(employee_details)
        all_employee_data = []
        for num in range(0, len(employee_data)):
            perticular_employee_data = {}
            for x in range(0, len(title_row)):
                key = title_row[x]
                value = employee_data[num][x]
                perticular_employee_data.update({key: value})
            all_employee_data.append(perticular_employee_data)

        # Process employee data using a thread pool
        with ThreadPoolExecutor() as executor:
            for details in all_employee_data:

                executor.submit(self.process_employee_data, companyname, details)
