import datetime


class TDSData():

    def __init__(self, db):
        self.db = db

    def deduction(self, id, companyname, epfo):

        ''' Calculate TDS '''

        users_ref = self.db.collection(companyname).document('employee').collection('employee').document(id)

        tds_data = users_ref.collection('tdsmst').document('tds').get().to_dict()



        if tds_data == None or tds_data['hlamount'] == '' or tds_data['hlamount'] == None :

            tds = 0

            return tds

        else:

            current_month = float(datetime.date.today().month)

            # current_month = 12

            # Annual Salary of Employee

            total_salary = float(users_ref.get().to_dict()["salary"])

            # TDS Data from Database

            principle_home_loan = float(tds_data["hlamount"])

            primium_on_insurance = float(tds_data["piannual"])

            elss = float(tds_data["elssannual"])

            tution_fee = float(tds_data["tfannual"])

            # EPFO Data from previous Salaryslip

            if current_month == 1:
                annual_pf = float(epfo) * 12
            elif current_month == 2:
                annual_pf = float(epfo) * 12
            else:
                annual_pf = float(epfo) * 12

            # 80C (1,50,000 Limit)

            total = principle_home_loan + primium_on_insurance + elss + annual_pf + tution_fee

            if total <= 150000:
                new_total_1 = total

            else:
                new_total_1 = 150000

            # TDS Health Insurance

            health_insurance = float(tds_data["hipannual"]) + \
                               float(tds_data["hisannual"]) + \
                               float(tds_data["hifannual"])

            if health_insurance >= 50000:
                new_total_2 = 50000

            else:
                new_total_2 = health_insurance

            # TDS floaterest on Home loan

            floaterest_on_home_loan = float(tds_data["ihlannual"])

            if floaterest_on_home_loan >= 200000:
                new_total_3 = 200000

            else:
                new_total_3 = floaterest_on_home_loan

            # TDS House rent

            annual_house_rent = float(tds_data["ahrmonth"]) * 12

            if principle_home_loan > 0:
                new_total_4 = 0
            else:
                min_annual_house_rent = min(
                    (annual_house_rent - ((total_salary - new_total_1 - new_total_2 - new_total_3) * 0.1)),
                    (total_salary * 0.25), 60000)
                if min_annual_house_rent < 0:
                    new_total_4 = 0
                else:
                    new_total_4 = min_annual_house_rent

            gross_salary_taxable = total_salary - new_total_1 - new_total_2 - new_total_3 - new_total_4 - 50000

            # prfloat(f"Gross = {gross_salary_taxable}")

            if gross_salary_taxable > 1000000:
                new_total_5 = ((gross_salary_taxable - 1000000) * 0.3 + (500000 * 0.2) + 12500)

            elif gross_salary_taxable > 500000:
                new_total_5 = ((gross_salary_taxable - 500000) * 0.2 + 12500)

            else:
                new_total_5 = 0

            education_cess = new_total_5 * 0.04

            if (new_total_5 + education_cess) > 0:
                new_total_6 = new_total_5 + education_cess
            else:
                new_total_6 = 0

            # Previous Month TDS and remaining Months


            if (users_ref.collection('salaryslips').document(f'sal00{str(current_month - 2)}').get().to_dict()) != None:

                if current_month <= 4:
                    no_of_remaining_month = (12 - 9 - current_month) + 2
                    if current_month <= 2:
                        tds_deducted_till_now = (float((users_ref.collection('salaryslips').document(f'sal00{str(10 + current_month)}').get().to_dict())["tds"])) * (12 - no_of_remaining_month)
                    else:
                        tds_deducted_till_now = (float((users_ref.collection('salaryslips').document(f'sal00{str(current_month - 2)}').get().to_dict())["tds"]) * (12 - no_of_remaining_month))
                elif current_month == 5:
                    no_of_remaining_month = 12
                    tds_deducted_till_now = 0
                else:
                    no_of_remaining_month = (12 - current_month) + 5
                    tds_deducted_till_now = (float((users_ref.collection('salaryslips').document(f'sal00{str(current_month - 2)}').get().to_dict())["tds"]) * (12 - no_of_remaining_month))

            else:
                tds_deducted_till_now = 0
                if current_month <= 4:
                    no_of_remaining_month = (12 - 9 - current_month) + 2
                elif current_month == 5:
                    no_of_remaining_month = 12
                    tds_deducted_till_now = 0
                else:
                    no_of_remaining_month = (12 - current_month) + 5



            # TDS Calculate

            if no_of_remaining_month == 0:
                tds = round(abs(new_total_6), 2)
            else:
                tds = round(abs((new_total_6 - tds_deducted_till_now) / no_of_remaining_month), 2)

            return tds

