
from openpyxl import load_workbook
from datetime import datetime
from firebase_admin import auth

class Uploaddata():

    def __init__(self, db):
        self.db = db

    def read_excel_rows(self, file_path, companyname):
        workbook = load_workbook(filename=file_path)

        sheet = workbook['Sheet1']

        max_row = sheet.max_row

        data = []

        for row in range(1, max_row + 1):
            row_data = []
            for column in range(1, sheet.max_column + 1):
                cell_value = sheet.cell(row=row, column=column).value
                # Check if the cell value is a datetime object

                if isinstance(cell_value, datetime):
                    # Convert the datetime to the desired format
                    cell_value = cell_value.strftime("%d-%m-%Y")

                if cell_value != None:
                    row_data.append(cell_value)

            data.append(row_data)

        header_row_index = None

        for i, row in enumerate(data):
            if row == ['Name', 'Department', 'Job Position', 'Designation', 'COSEC ID', 'Password', 'Confirm Password', 'Date of Joining (DD/MM/YYYY)', 'CTC ₹ per year', 'Email']:
                header_row_index = i

        if header_row_index is None:
            print("Invalid data format. Unable to find header row or attendance data.")
            exit()
        #
        column_headers = data[header_row_index]

        employee_records = []

        for row in data:
            if row != []:
                record = dict(zip(column_headers, row))
                employee_records.append(record)

        all_data = employee_records

        for data in all_data[1:]:
            doj = ''
            if data['Date of Joining (DD/MM/YYYY)'][2] == "/":
                date = (data['Date of Joining (DD/MM/YYYY)']).split('/')
                doj = f"{date[2]}-{date[1]}-{date[0]}"
            elif data['Date of Joining (DD/MM/YYYY)'][2] == "-":
                date = (data['Date of Joining (DD/MM/YYYY)']).split('-')
                doj = f"{date[2]}-{date[1]}-{date[0]}"
            emp_data = {'cosecID': data["COSEC ID"], 'employeeName': data["Name"], 'department': data["Department"],
                        'designation': data["Designation"], "password": data['Password'],
                        'confirmPassword': data["Confirm Password"], 'doj': doj,
                        'salary': data['CTC ₹ per year'], 'workEmail': data['Email']}
            # print(emp_data)

            try:
                user = auth.create_user(email=emp_data['workEmail'], password=emp_data['password'])
                self.db.collection(companyname).document(u'employee').collection('employee').document(user.uid).set(emp_data)
            except:
                pass





