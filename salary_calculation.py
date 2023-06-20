import calendar
import datetime
from tds_data import TDSData


class SalaryCalculation():

    def __init__(self,db,companyname):
        self.db = db
        self.companyname=companyname
    def generate_salary(self, holidays):

        holidays = holidays

        today = datetime.date.today()
        year = today.year
        day=today.day
        month = today.month
        if day >=26:
            month+=1
        if day<26 and month==1:
            year-=1
        if month == 1:
            prev_month = 11
            current_month = 12
        elif month == 2:
            prev_month = 12
            current_month = 1
        else:
            prev_month = month - 2
            current_month = month - 1
            # Get number of days in the current month and the day of the week of the first day
        first_day, num_days = calendar.monthrange(year, month)
        # Loop through days and count working days
        num_working_days = 0
        Week_off = 0
        working_days_per_week = {}
        # holidays=holidays.keys()
        holiday = 0

        # Get the number of days in the current month
        prev_num_days = calendar.monthrange(year, (prev_month))[1]

        # Create a list of all the dates in the current month
        prev_month_dates = [f"{year:04}-{prev_month:02}-{day:02}" for day in range(26, prev_num_days + 1)]
        current_month_dates = [f"{year:04}-{current_month:02}-{day:02}" for day in range(1, 26)]
        dates = prev_month_dates + current_month_dates

        data_date = []
        if holidays != None:
            for day in range(1, len(prev_month_dates) + 1):
                if current_month_dates[day - 1] in holidays:
                    holiday += 1
                elif calendar.weekday(year, prev_month, day) not in (calendar.SATURDAY, calendar.SUNDAY):
                    data_date.append(current_month_dates[day - 1])
                    num_working_days += 1
                else:
                    Week_off += 1
            for day in range(1, 26):

                if dates[day - 1] in holidays:
                    holiday += 1
                elif calendar.weekday(year, current_month, day) not in (calendar.SATURDAY, calendar.SUNDAY):
                    data_date.append(current_month_dates[day - 1])
                    num_working_days += 1
                else:
                    Week_off += 1

        employee_list_with_increments = (self.db.collection(self.companyname).document('increments').get()).to_dict()

        result = []

        for increment in employee_list_with_increments['increments']:
            effective_date = increment.get('effectiveDate')
            if effective_date:
                increment_month = int(effective_date.split('-')[1])
                increment_date = int(effective_date.split('-')[2])

                if ((increment_month == current_month and (increment_date) <= 25)) or ((increment_month == prev_month and (increment_date) >= 26)):
                    result.append(increment)
        salary_percentage = (self.db.collection(self.companyname).document('salary_calc').get()).to_dict()

        employee_list = {}

        docs = self.db.collection(self.companyname).document(u'employee').collection('employee').stream()
        for doc in docs:

            if 'user_status' not in doc.to_dict():
                self.db.collection(self.companyname).document('employee').collection('employee').document(
                    doc.id).collection(
                    'salaryslips').document(f'sal00{current_month - 1}').delete()
                employee_list.update({doc.id: doc.to_dict()})
            elif doc.to_dict()['user_status'] != 'disable':
                self.db.collection(self.companyname).document('employee').collection('employee').document(
                    doc.id).collection(
                    'salaryslips').document(f'sal00{current_month - 1}').delete()
                employee_list.update({doc.id: doc.to_dict()})
            else:
                self.db.collection(self.companyname).document('employee').collection('employee').document(
                    doc.id).collection(
                    'salaryslips').document(f'sal00{current_month - 1}').delete()

        for key, value in employee_list.items():

            empid = key
            #print(empid)
            emp_data = value
            if emp_data['role']!='Admin':
                emp_name = emp_data['employeeName']

                increment = [d for d in result if d.get('empid') == empid]
                if increment != [] and emp_data['designation']=='Employee':
                    empid = increment[0]['empid']
                    effective_date = increment[0]['effectiveDate']
                    #print("effective_date",effective_date)
                    before_days = 0
                    after_days = 0
                    for date in data_date:
                        if date <= effective_date:
                            before_days += 1
                        else:
                            after_days += 1
                    inc_before_salary = float(increment[0]['grossSalary'])/num_working_days*before_days
                    inc_after_salary = float(increment[0]['total'])/num_working_days*after_days

                    emp_salary_bfr = inc_before_salary

                    lwp_bfr = 0

                    emp_basic_salary_bfr = round((float(emp_salary_bfr) * 0.5), 2)

                    if emp_salary_bfr >= 15000:

                        emp_hra_bfr = 7500

                        emp_da_bfr = 0

                        other_allowance_bfr = emp_salary_bfr - emp_basic_salary_bfr - emp_hra_bfr - emp_da_bfr

                    else:

                        emp_hra_bfr = emp_salary_bfr - emp_basic_salary_bfr

                        emp_da_bfr = 0

                        other_allowance_bfr = emp_salary_bfr - emp_basic_salary_bfr - emp_hra_bfr - emp_da_bfr

                    incentive_bfr = 0

                    arrears_bfr = 0

                    grs_outstanding_adjustment_bfr = 0

                    statutory_bns_bfr = 0

                    gross_salary_bfr = round((
                            emp_basic_salary_bfr + emp_hra_bfr + emp_da_bfr + other_allowance_bfr + incentive_bfr + arrears_bfr + grs_outstanding_adjustment_bfr + statutory_bns_bfr),
                        2)

                    if emp_salary_bfr <= 22000:
                        epfo_bfr = round(((emp_salary_bfr - emp_hra_bfr) * 0.24), 2)

                        if epfo_bfr <= 3600:
                            epfo_bfr = epfo_bfr
                        else:
                            epfo_bfr = 3600

                    else:

                        epfo_bfr = 3600

                    ded_outstanding_adjustment_bfr = 0

                    pt_bfr = 0

                    tds_bfr = TDSData(db=self.db).deduction(id=empid, epfo=epfo_bfr, companyname=self.companyname)
                    other_deduction_bfr = 0
                    leave_deduction_bfr = 0
                    total_deduction_bfr = round(
                        (
                                    epfo_bfr + ded_outstanding_adjustment_bfr + pt_bfr + tds_bfr + other_deduction_bfr + leave_deduction_bfr),
                        2)

                    net_salary_bfr = round((gross_salary_bfr - total_deduction_bfr), 2)

                    salary_slip_data_bfr = {
                        'lwp': lwp_bfr, 'basic': emp_basic_salary_bfr, 'da': emp_da_bfr, 'hra': emp_hra_bfr,
                        'otherAllowance': other_allowance_bfr,
                        'incentive': incentive_bfr, 'grsOutstandingAdjustment': grs_outstanding_adjustment_bfr,
                        'arrears': arrears_bfr,
                        'statutoryBonus': statutory_bns_bfr, 'grossSalary': gross_salary_bfr, 'epfo': epfo_bfr,
                        'dedOutstandingAdjustment': ded_outstanding_adjustment_bfr, 'pt': pt_bfr, 'tds': tds_bfr,
                        'otherDeduction': other_deduction_bfr, 'leaveDeduction': leave_deduction_bfr,
                        'totalDeduction': total_deduction_bfr,
                        'netSalary': net_salary_bfr
                    }

                    emp_salary_aft = inc_after_salary

                    lwp_aft = 0

                    emp_basic_salary_aft = round(float(emp_salary_aft * 0.5), 2)

                    if emp_salary_aft >= 15000:

                        emp_hra_aft = 7500

                        emp_da_aft = 0

                        other_allowance_aft = emp_salary_aft - emp_basic_salary_aft - emp_hra_aft - emp_da_aft

                    else:

                        emp_hra_aft = emp_salary_aft - emp_basic_salary_aft

                        emp_da_aft = 0

                        other_allowance_aft = emp_salary_aft - emp_basic_salary_aft - emp_hra_aft - emp_da_aft

                    incentive_aft = 0

                    arrears_aft = 0

                    grs_outstanding_adjustment_aft = 0

                    statutory_bns_aft = 0

                    gross_salary_aft = round((emp_basic_salary_aft + emp_hra_aft + emp_da_aft + other_allowance_aft + incentive_aft + arrears_aft + grs_outstanding_adjustment_aft + statutory_bns_aft),2)
                    if emp_salary_aft <= 22000:
                        epfo_aft = round(((emp_salary_aft - emp_hra_aft) * 0.24), 2)

                        if epfo_aft <= 3600:
                            epfo_aft = epfo_aft
                        else:
                            epfo_aft = 3600

                    else:

                        epfo_aft = 3600

                    ded_outstanding_adjustment_aft = 0

                    pt_aft = 0

                    tds_aft = TDSData(db=self.db).deduction(id=empid, epfo=epfo_aft, companyname=self.companyname)

                    other_deduction_aft = 0

                    if lwp_aft > 0:
                        leave_deduction_aft = lwp_aft * (
                            round((float(emp_salary_aft) / num_working_days * float(salary_percentage['deductionpercentage'])),2))
                    else:
                        leave_deduction_aft = 0

                    total_deduction_aft = round((epfo_aft + ded_outstanding_adjustment_aft + pt_aft + tds_aft + other_deduction_aft + leave_deduction_aft),2)

                    net_salary_aft = round((gross_salary_aft - total_deduction_aft), 2)

                    salary_slip_data_aft = {
                        'lwp': lwp_aft, 'basic': emp_basic_salary_aft, 'da': emp_da_aft, 'hra': emp_hra_aft,
                        'otherAllowance': other_allowance_aft, 'incentive': incentive_aft,
                        'grsOutstandingAdjustment': grs_outstanding_adjustment_aft, 'arrears': arrears_aft,
                        'statutoryBonus': statutory_bns_aft, 'grossSalary': gross_salary_aft, 'epfo': epfo_aft,
                        'dedOutstandingAdjustment': ded_outstanding_adjustment_aft, 'pt': pt_aft, 'tds': tds_aft,
                        'otherDeduction': other_deduction_aft, 'leaveDeduction': leave_deduction_aft,
                        'totalDeduction': total_deduction_aft, 'netSalary': net_salary_aft
                    }

                    salary_slip_data = {
                        'employeeName': emp_name, 'userID': empid, 'slip_id': f'sal00{current_month}_{year}',
                        'lwp': salary_slip_data_aft['lwp'] + salary_slip_data_bfr['lwp'],
                        'basic': round((salary_slip_data_aft['basic'] + salary_slip_data_bfr['basic']), 2),
                        'da': round((salary_slip_data_aft['da'] + salary_slip_data_bfr['da']), 2),
                        'hra': round((salary_slip_data_aft['hra'] + salary_slip_data_bfr['hra']), 2),
                        'otherAllowance': round((salary_slip_data_aft['otherAllowance'] + salary_slip_data_bfr['otherAllowance']), 2),
                        'incentive': round((salary_slip_data_aft['incentive'] + salary_slip_data_bfr['incentive']), 2),
                        'grsOutstandingAdjustment': round((salary_slip_data_aft['grsOutstandingAdjustment'] + salary_slip_data_bfr['grsOutstandingAdjustment']), 2),
                        'arrears': round((salary_slip_data_aft['arrears'] + salary_slip_data_bfr['arrears']), 2),
                        'statutoryBonus': salary_slip_data_aft['statutoryBonus'] + salary_slip_data_bfr['statutoryBonus'],
                        'grossSalary': round((salary_slip_data_aft['grossSalary'] + salary_slip_data_bfr['grossSalary']), 2),
                        'epfo': salary_slip_data_aft['epfo'] + salary_slip_data_bfr['epfo'],
                        'dedOutstandingAdjustment': salary_slip_data_aft['dedOutstandingAdjustment'] + salary_slip_data_bfr['dedOutstandingAdjustment'],
                        'pt': salary_slip_data_aft['pt'] + salary_slip_data_bfr['pt'],
                        'tds': round((salary_slip_data_aft['tds'] + salary_slip_data_bfr['tds']), 2),
                        'otherDeduction': salary_slip_data_aft['otherDeduction'] + salary_slip_data_bfr['otherDeduction'],
                        'leaveDeduction': salary_slip_data_aft['leaveDeduction'] + salary_slip_data_bfr['leaveDeduction'],
                        'totalDeduction': salary_slip_data_aft['totalDeduction'] + salary_slip_data_bfr['totalDeduction'],
                        'netSalary': round((salary_slip_data_aft['netSalary'] + salary_slip_data_bfr['netSalary']), 2),
                        'month': current_month, 'year': year, 'cosecID': emp_data['cosecID'], 'WO': 0,
                        'UL': 0, 'Auth_OT': "00:00", 'WrkHrs': "00:00", 'CL': 0, 'PL': 0, 'SL': 0,
                        'before_gross':salary_slip_data_bfr['grossSalary'],
                        'after_gross':salary_slip_data_aft['grossSalary'],
                        'incremented_salary':'yes'
                    }
                    users_ref = self.db.collection(self.companyname).document('employee').collection(
                        'employee').document(empid)

                    users_ref.collection('salaryslips').document(f'sal00{current_month}_{year}').set(salary_slip_data)


                elif emp_data['designation']=='Employee' :
                    this_month = int(emp_data['doj'].split('-')[1])
                    this_date = int(emp_data['doj'].split('-')[2])
                    #print(emp_data['doj'])
                    #print(this_month,this_date)
                    #print(current_month,prev_month)
                    if ((this_month == current_month and (this_date) <= 25) or (this_month == prev_month and (this_date) >= 26)):

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

                        pt = 0

                        tds = TDSData(db=self.db).deduction(id=empid,epfo=epfo,companyname=self.companyname)

                        other_deduction = 0

                        if lwp > 0:
                            leave_deduction = lwp * (round((float(emp_salary)/num_working_days * float(salary_percentage['deductionpercentage'])), 2))
                        else:
                            leave_deduction = 0

                        total_deduction = round((epfo + ded_outstanding_adjustment + pt + tds + other_deduction + leave_deduction), 2)

                        net_salary = round((gross_salary - total_deduction), 2)

                        salary_slip_data = {
                            'employeeName': emp_name, 'userID': empid,'slip_id': f'sal00{current_month}_{year}', 'lwp': lwp,
                            'basic': emp_basic_salary, 'da': emp_da, 'hra': emp_hra, 'otherAllowance': other_allowance,
                            'incentive': incentive, 'grsOutstandingAdjustment': grs_outstanding_adjustment, 'arrears': arrears,
                            'statutoryBonus': statutory_bns, 'grossSalary': gross_salary, 'epfo': epfo,
                            'dedOutstandingAdjustment': ded_outstanding_adjustment, 'pt': pt, 'tds': tds,
                            'otherDeduction': other_deduction, 'leaveDeduction': leave_deduction, 'totalDeduction': total_deduction,
                            'netSalary': net_salary, 'month': current_month, 'year': year, 'cosecID': emp_data['cosecID'], 'WO': 0,
                            'UL': 0, 'Auth_OT': "00:00", 'WrkHrs': "00:00", 'CL': 0, 'PL': 0, 'SL': 0
                        }
                        users_ref = self.db.collection(self.companyname).document('employee').collection('employee').document(empid)

                        users_ref.collection('salaryslips').document(f'sal00{current_month}_{year}').set(salary_slip_data)

                month_name = calendar.month_name[current_month]
                if day<26 and month==1:
                     self.db.collection(self.companyname).document('salary_status').update({str(year):{month_name:"None"}})
                self.db.collection(self.companyname).document('salary_status').update({f'{year}.{month_name}': 'None'})













