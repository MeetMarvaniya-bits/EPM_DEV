from reportlab.pdfgen import canvas
from reportlab.lib import colors
from details import Profile
from salary_manage import Salarymanage
import os
import calendar
import threading
from moth_days import MonthCount
import io
from flask import Response

month_count = MonthCount()


def draw_my_rular(pdf):
    """ FOR GRID LAYOUT """
    pdf.drawString(100, 810, "x100")
    pdf.drawString(200, 810, "x200")
    pdf.drawString(300, 810, "x300")
    pdf.drawString(400, 810, "x400")
    pdf.drawString(500, 810, "x500")

    pdf.drawString(10, 100, "y100")
    pdf.drawString(10, 200, "y200")
    pdf.drawString(10, 300, "y300")
    pdf.drawString(10, 400, "y400")
    pdf.drawString(10, 500, "y500")
    pdf.drawString(10, 600, "y600")
    pdf.drawString(10, 700, "y700")
    pdf.drawString(10, 800, "y800")


# draw_my_rular(pdf)

class SalarySlip():

    def __init__(self, db):
        self.db = db

    def salary_slip_personal(self, companyname, id, salid, path):
        """ CREATE SALARYSLIP PDF FROM PROFILE VIEW """

        empid = id

        personal_data = Profile(self.db, empid, companyname).personal_data()

        salary_data = Profile(self.db, empid, companyname).salary_data()[salid]

        leave_data = Profile(self.db, empid, companyname).leave_data()[0]

        # GET MONTH WORKING DAYS
        holidays = self.db.collection(companyname).document('holidays').get().to_dict()
        month_data = month_count.count_previous_month(holidays, salid)

        # GET MONTH NAME
        mont_in_num = int(salid[5:])
        month = calendar.month_name[mont_in_num]

        # PDF STORAGE LOCATION
        pdf_location = f"{path}/EPMS/Salaryslips/{empid}/{month}_{salary_data['year']}/"
        if not os.path.exists(pdf_location):
            os.makedirs(pdf_location)

        # PDF FILE NAME
        filename = f'{empid}_{salid}.pdf'
        pdf_file = io.BytesIO()
        documentTitle = "SalarySlip!"
        title = "ALIAN SOFTWARE"
        address_line1 = "Shreeji Arcade, 2nd Floor, Opp Shasvat Hospital,"
        address_line2 = "Indira Circle, Anand, Gujarat 388001"
        subtitle = f"Pay Slip for the Month of {month} {salary_data['year']}"
        subtitle_one = "Employee Pay Summary"

        textLines = {"Employee Name": personal_data["employeeName"],
                     "Employee ID": personal_data["userID"],
                     "Date of Joining": personal_data["doj"],
                     "Branch": "Anand",
                     "Designation": personal_data["designation"],
                     "Department": personal_data["department"],
                     "Date of Effectiveness": personal_data["doj"],
                     "Week Offs": month_data['weekoff'],
                     "Working Days": month_data['workingDays'],
                     "LWP": salary_data["lwp"]
                     }

        textLines_two = {"PAN No.": personal_data["panCardNo"],
                         "UAN No.": personal_data["uanNo"],
                         "PF No.": personal_data["pfAccountNo"],
                         "ESIC No.": personal_data["esicNo"],
                         "Bank Name": personal_data["bankName"],
                         "Bank A/c No.": personal_data["accountNumber"],
                         }

        textLines_three = {"Basic Salary": salary_data["basic"],
                           "HRA": salary_data["hra"],
                           "DA": salary_data["da"],
                           "Other Allowance": salary_data["otherAllowance"],
                           "Incentive": salary_data["incentive"],
                           "Arrears": salary_data["arrears"],
                           "Outstanding Adjustment": salary_data["grsOutstandingAdjustment"],
                           "Statutory Bonus": salary_data["statutoryBonus"]
                           }

        textLines_four = {"EPFO": salary_data["epfo"],
                          "TDS": salary_data["tds"],
                          "PT": salary_data["pt"],
                          "Leave Deduction": salary_data["leaveDeduction"],
                          "Other Deduction": salary_data["otherDeduction"],
                          "Outstanding Adjustment": salary_data["dedOutstandingAdjustment"],
                          }

        pdf = canvas.Canvas(pdf_file)

        pdf.setTitle(documentTitle)

        # # # # # Company Name and Address # # # # #

        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(50, 800, title)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, 780, address_line1)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, 765, address_line2)

        pdf.line(30, 750, 550, 750)

        # # # # # Add Company Logo # # # # #

        pdf.drawImage('static/assets/alian_logo_2.png', 380, 770, width=150, height=40)

        # # # # # Employee Pay Summary # # # # #

        pdf.setFont("Helvetica", 10)
        pdf.drawCentredString(290, 735, subtitle)

        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawCentredString(290, 710, subtitle_one)

        # # # # # PERSONAL INFO # # # # #

        text = pdf.beginText(50, 680)
        pdf.setFont("Helvetica-Bold", 10)
        text.setFillColor(colors.black)
        for key, value in textLines.items():
            text.textLines(key)
            text.textLines('')
        pdf.drawText(text)

        text = pdf.beginText(190, 680)
        pdf.setFont("Helvetica", 10)
        text.setFillColor(colors.black)
        for key, value in textLines.items():
            text.textLines(str(value))
            text.textLines('')
        pdf.drawText(text)

        # # # # # ACCOUNT INFO # # # # #

        text = pdf.beginText(320, 680)
        pdf.setFont("Helvetica-Bold", 10)
        text.setFillColor(colors.black)
        for key, value in textLines_two.items():
            text.textLines(key)
            text.textLines('')
        pdf.drawText(text)

        text = pdf.beginText(410, 680)
        pdf.setFont("Helvetica", 10)
        text.setFillColor(colors.black)
        for key, value in textLines_two.items():
            text.textLines(str(value))
            text.textLines('')
        pdf.drawText(text)

        # Table Horizontal lines
        pdf.line(320, 520, 530, 520)
        pdf.line(320, 500, 530, 500)
        pdf.line(320, 480, 530, 480)
        pdf.line(320, 460, 530, 460)

        # Table Vertical lines
        pdf.line(320, 520, 320, 460)
        pdf.line(390, 500, 390, 460)
        pdf.line(460, 500, 460, 460)
        pdf.line(530, 520, 530, 460)

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawCentredString(425, 505, "Leave Balance")
        pdf.drawCentredString(355, 485, "CL")
        pdf.drawCentredString(425, 485, "SL")
        pdf.drawCentredString(495, 485, "PL")
        pdf.setFont("Helvetica", 10)
        pdf.drawCentredString(355, 465, str(leave_data["CL"]))
        pdf.drawCentredString(425, 465, str(leave_data["SL"]))
        pdf.drawCentredString(495, 465, str(leave_data["PL"]))

        pdf.line(30, 430, 550, 430)

        # # # # # Amounts # # # # #

        pdf.setFont("Helvetica-Bold", 13)

        pdf.drawString(50, 410, "Earning")

        pdf.drawString(190, 410, "Amount")

        pdf.drawString(320, 410, "Deduction")

        pdf.drawString(470, 410, "Amount")

        pdf.line(30, 400, 550, 400)

        # # # # # EARNING # # # # #

        text = pdf.beginText(50, 370)
        pdf.setFont("Helvetica-Bold", 10)
        text.setFillColor(colors.black)
        for key, value in textLines_three.items():
            text.textLines(key)
            text.textLines('')
        pdf.drawText(text)

        text = pdf.beginText(190, 370)
        pdf.setFont("Helvetica", 10)
        text.setFillColor(colors.black)
        for key, value in textLines_three.items():
            text.textLines(str(value))
            text.textLines('')
        pdf.drawText(text)

        pdf.line(290, 430, 290, 180)

        # # # # # DEDUCTION # # # # #

        text = pdf.beginText(320, 370)
        pdf.setFont("Helvetica-Bold", 10)
        text.setFillColor(colors.black)
        for key, value in textLines_four.items():
            text.textLines(key)
            text.textLines('')
        pdf.drawText(text)

        text = pdf.beginText(470, 370)
        pdf.setFont("Helvetica", 10)
        text.setFillColor(colors.black)
        for key, value in textLines_four.items():
            text.textLines(str(value))
            text.textLines('')
        pdf.drawText(text)

        pdf.line(30, 180, 550, 180)

        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(50, 160, "Gross Salary(A)")
        pdf.setFont("Helvetica", 13)
        pdf.drawString(190, 160, str(salary_data["grossSalary"]))

        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(320, 160, "Total Deductions(B)")
        pdf.setFont("Helvetica", 13)
        pdf.drawString(470, 160, str(salary_data["totalDeduction"]))

        pdf.line(30, 150, 550, 150)

        # # # # # Footer # # # # #

        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawCentredString(290, 100, f"Total Net Payable = {salary_data['netSalary']} RS")

        pdf.setFont("Helvetica", 10)
        pdf.drawCentredString(290, 10, "Note : This is electronically generated document")

        pdf.showPage()
        pdf.save()

        ''' EXCEL SHEET DATA FORMATE FOR NEW COMPANY '''
        # Create the Excel file

        # Save the file to a BytesIO object
        pdf_file.seek(0)

        # Return the file as a response with appropriate headers
        return Response(
            pdf_file,
            mimetype='application/pdf',
            headers={
                "Content-Disposition": f"attachment;filename={filename}",
                "Content-Type": "application/pdf"
            }
        )

    def generate_slip(self, empid, companyname, salid, path):
        """ CREATE SALARYSLIP PDF FOR ALL EMPLOYEES """
        personal_data = Profile(self.db, empid, companyname).personal_data()
        salary_data = Profile(self.db, empid, companyname).salary_data()[salid]
        leave_data = Profile(self.db, empid, companyname).leave_data()[0]

        # MONTH WORKING DAY
        holidays = self.db.collection(companyname).document('holidays').get().to_dict()
        month_data = month_count.count_previous_month(holidays, salid)

        # GET MONTH NAME
        mont_in_num = int(salid[5:])
        month = calendar.month_name[mont_in_num]
        #
        # # DEFINE PDF LOCATION
        # pdf_location = f"{path}/EPMS/Salaryslips/{month}_{salary_data['year']}/"
        # if not os.path.exists(pdf_location):
        #     os.makedirs(pdf_location)

        # PDF FILE NAME
        filename = f'{empid}_{salid}.pdf'
        pdf_file = io.BytesIO()
        documentTitle = "SalarySlip!"
        title = "ALIAN SOFTWARE"
        address_line1 = "Shreeji Arcade, 2nd Floor, Opp Shasvat Hospital,"
        address_line2 = "Indira Circle, Anand, Gujarat 388001"
        subtitle = f"Pay Slip for the Month of {month} {salary_data['year']}"
        subtitle_one = "Employee Pay Summary"

        textLines = {"Employee Name": personal_data["employeeName"],
                     "Employee ID": personal_data["userID"],
                     "Date of Joining": personal_data["doj"],
                     "Branch": "Anand",
                     "Designation": personal_data["designation"],
                     "Department": personal_data["department"],
                     "Date of effectiveness": personal_data["doj"],
                     "Week Offs": month_data['weekoff'],
                     "Working Days": month_data['workingDays'],
                     "LWP": salary_data['lwp']
                     }

        textLines_two = {"PAN No.": personal_data["panCardNo"],
                         "UAN No.": personal_data["uanNo"],
                         "PF No.": personal_data["pfAccountNo"],
                         "ESIC No.": personal_data["esicNo"],
                         "Bank Name": personal_data["bankName"],
                         "Bank A/c No.": personal_data["accountNumber"],
                         }

        textLines_three = {"Basic Salary": salary_data["basic"],
                           "HRA": salary_data["hra"],
                           "DA": salary_data["da"],
                           "Other Allowance": salary_data["otherAllowance"],
                           "Incentive": salary_data["incentive"],
                           "Arrears": salary_data["arrears"],
                           "Outstanding Adjustment": salary_data["grsOutstandingAdjustment"],
                           "Statutory Bonus": salary_data["statutoryBonus"]
                           }

        textLines_four = {"EPFO": salary_data["epfo"],
                          "TDS": salary_data["tds"],
                          "PT": salary_data["pt"],
                          "Leave Deduction": salary_data["leaveDeduction"],
                          "Other Deduction": salary_data["otherDeduction"],
                          "Outstanding Adjustment": salary_data["dedOutstandingAdjustment"],
                          }

        pdf = canvas.Canvas(pdf_file)

        pdf.setTitle(documentTitle)

        # # # # # Company Name and Address # # # # #

        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawString(50, 800, title)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, 780, address_line1)

        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, 765, address_line2)

        pdf.line(30, 750, 550, 750)

        # # # # # Add Company Logo # # # # #

        pdf.drawImage('static/assets/alian_logo_2.png', 380, 770, width=150, height=40)

        # # # # # Employee Pay Summary # # # # #

        pdf.setFont("Helvetica", 10)
        pdf.drawCentredString(290, 735, subtitle)

        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawCentredString(290, 710, subtitle_one)

        # # # # # PERSONAL INFO # # # # #

        text = pdf.beginText(50, 680)
        pdf.setFont("Helvetica-Bold", 10)
        text.setFillColor(colors.black)
        for key, value in textLines.items():
            text.textLines(key)
            text.textLines('')
        pdf.drawText(text)

        text = pdf.beginText(190, 680)
        pdf.setFont("Helvetica", 10)
        text.setFillColor(colors.black)
        for key, value in textLines.items():
            text.textLines(str(value))
            text.textLines('')
        pdf.drawText(text)

        # # # # # ACCOUNT INFO # # # # #

        text = pdf.beginText(320, 680)
        pdf.setFont("Helvetica-Bold", 10)
        text.setFillColor(colors.black)
        for key, value in textLines_two.items():
            text.textLines(key)
            text.textLines('')
        pdf.drawText(text)

        text = pdf.beginText(410, 680)
        pdf.setFont("Helvetica", 10)
        text.setFillColor(colors.black)
        for key, value in textLines_two.items():
            text.textLines(str(value))
            text.textLines('')
        pdf.drawText(text)

        # Table Horizontal lines
        pdf.line(320, 520, 530, 520)
        pdf.line(320, 500, 530, 500)
        pdf.line(320, 480, 530, 480)
        pdf.line(320, 460, 530, 460)

        # Table Vertical lines
        pdf.line(320, 520, 320, 460)
        pdf.line(390, 500, 390, 460)
        pdf.line(460, 500, 460, 460)
        pdf.line(530, 520, 530, 460)

        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawCentredString(425, 505, "Leave Balance")
        pdf.drawCentredString(355, 485, "CL")
        pdf.drawCentredString(425, 485, "SL")
        pdf.drawCentredString(495, 485, "PL")
        pdf.setFont("Helvetica", 10)
        pdf.drawCentredString(355, 465, str(leave_data["CL"]))
        pdf.drawCentredString(425, 465, str(leave_data["SL"]))
        pdf.drawCentredString(495, 465, str(leave_data["PL"]))

        pdf.line(30, 430, 550, 430)

        # # # # # Amounts # # # # #

        pdf.setFont("Helvetica-Bold", 13)

        pdf.drawString(50, 410, "Earning")

        pdf.drawString(190, 410, "Amount")

        pdf.drawString(320, 410, "Deduction")

        pdf.drawString(470, 410, "Amount")

        pdf.line(30, 400, 550, 400)

        # # # # # EARNING # # # # #

        text = pdf.beginText(50, 370)
        pdf.setFont("Helvetica-Bold", 10)
        text.setFillColor(colors.black)
        for key, value in textLines_three.items():
            text.textLines(key)
            text.textLines('')
        pdf.drawText(text)

        text = pdf.beginText(190, 370)
        pdf.setFont("Helvetica", 10)
        text.setFillColor(colors.black)
        for key, value in textLines_three.items():
            text.textLines(str(value))
            text.textLines('')
        pdf.drawText(text)

        pdf.line(290, 430, 290, 180)

        # # # # # DEDUCTION # # # # #

        text = pdf.beginText(320, 370)
        pdf.setFont("Helvetica-Bold", 10)
        text.setFillColor(colors.black)
        for key, value in textLines_four.items():
            text.textLines(key)
            text.textLines('')
        pdf.drawText(text)

        text = pdf.beginText(470, 370)
        pdf.setFont("Helvetica", 10)
        text.setFillColor(colors.black)
        for key, value in textLines_four.items():
            text.textLines(str(value))
            text.textLines('')
        pdf.drawText(text)

        pdf.line(30, 180, 550, 180)

        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(50, 160, "Gross Salary(A)")
        pdf.setFont("Helvetica", 13)
        pdf.drawString(190, 160, str(salary_data["grossSalary"]))

        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(320, 160, "Total Deductions(B)")
        pdf.setFont("Helvetica", 13)
        pdf.drawString(470, 160, str(salary_data["totalDeduction"]))

        pdf.line(30, 150, 550, 150)

        # # # # # Footer # # # # #

        pdf.setFont("Helvetica-Bold", 15)
        pdf.drawCentredString(290, 100, f"Total Net Payable = {salary_data['netSalary']} RS")

        pdf.setFont("Helvetica", 10)
        pdf.drawCentredString(290, 10, "Note : This is electronically generated document")

        pdf.showPage()
        pdf.save()

        # Save the file to a BytesIO object
        pdf_file.seek(0)

        # Return the file as a response with appropriate headers
        return Response(
            pdf_file,
            mimetype='application/pdf',
            headers={
                "Content-Disposition": f"attachment;filename={filename}",
                "Content-Type": "application/pdf"
            }
        )

    def salary_slip(self, companyname, salid, path):
        """ CREATE SALARYSLIP PDF """
        salary_list = Salarymanage(self.db).get_all_emp_salary_data(salid=salid, companyname=companyname)
        threads = []
        for i in salary_list:
            empid = salary_list[i]["userID"]
            thread = threading.Thread(target=self.generate_slip, args=(empid, companyname, salid, path))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
