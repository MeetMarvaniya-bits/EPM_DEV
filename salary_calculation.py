import calendar
import datetime
from tds_data import TDSData
from month_days import MonthCount
count_days=MonthCount()
class SalaryCalculation():

    def __init__(self,db,companyname):
        self.db = db
        self.companyname=companyname
    def generate_salary(self, holidays,startdate,enddate):
        print("start")
        # if int(enddate.split('_')[1])==4:
        total_days=count_days.total_days_count(enddate,holidays)
        print("total_days",total_days)


        startday = int(startdate.split("-")[-1])
        startmonth = int(startdate.split("-")[1])
        startyear = int(startdate.split("-")[0])

        endday = int(enddate.split("-")[-1])
        endmonth = int(enddate.split("-")[1])
        endyear = int(enddate.split("-")[0])

        print(type(endyear), endday, endmonth)
        print(startyear, startday, startyear)

        num_working_days = 0
        Week_off = 0
        working_days_per_week = {}
        # holidays=holidays.keys()
        holiday = 0
        salary_total = {
            'netSalary': 0,
            'grossSalary': 0,
            'epfo': 0,
            'pt': 0,
            'tds': 0,
        }
        # Get the number of days in the current month
        prev_num_days = calendar.monthrange(year, (prev_month))[1]

        # Create a list of all the dates in the current month
        prev_month_dates = [f"{year:04}-{prev_month:02}-{day:02}" for day in range(26, prev_num_days + 1)]
        current_month_dates = [f"{year:04}-{current_month:02}-{day:02}" for day in range(1, 26)]
        dates = prev_month_dates + current_month_dates

        data_date = []
        if holidays != None:
            if startmonth != endmonth:
                count = 0
                for day in range(0, len(dates)):
                    print(dates[day], 'day')
                    # print(endmonth_dates[day - 1])
                    if calendar.weekday(int(dates[day - 1].split('-')[0]), int(dates[day - 1].split('-')[1]),
                                        int(dates[day - 1].split('-')[2])) in (
                            calendar.SATURDAY, calendar.SUNDAY):
                        Week_off += 1
                    elif  str(datetime.datetime.strptime(dates[day-1], "%Y-%m-%d").date()) in holidays:
                        data_date.append(dates[day])
                        print(dates[day] ,"hol")
                        holiday += 1
                    elif calendar.weekday(int(dates[day - 1].split('-')[0]), int(dates[day - 1].split('-')[1]),
                                          int(dates[day - 1].split('-')[2])) not in (
                    calendar.SATURDAY, calendar.SUNDAY):
                        data_date.append(dates[day])
                        num_working_days += 1


            else:
                print(holidays)
                for day in range(startday, endday + 1):

                    if calendar.weekday(endyear, endmonth, day) in (calendar.SATURDAY, calendar.SUNDAY):
                        print(dates[day - startday], type(dates[day - startday]))
                        Week_off += 1
                    elif str(datetime.datetime.strptime(dates[day-startday], "%Y-%m-%d").date()) in holidays:
                        data_date.append(day - startday)
                        print(dates[day - startday],"hol")
                        holiday += 1
                    elif calendar.weekday(endyear, endmonth, day) not in (calendar.SATURDAY, calendar.SUNDAY):
                        print(dates[day - startday], "wd")

                        data_date.append(day - startday)
                        num_working_days += 1
        data = {
            'weekoff': Week_off,
            'workingDays': num_working_days,
            'holydays': holiday
                }
        print(data,"from start date to end")
        salary_total = {
            'netSalary': 0,
            'grossSalary': 0,
            'epfo': 0,
            'pt': 0,
            'tds': 0,
        }
        employee_list_with_increments = (self.db.collection(self.companyname).document('increments').get()).to_dict()

        result = []
        if employee_list_with_increments == None or employee_list_with_increments == {}:
            pass
        else:
            for increment in employee_list_with_increments['increments']:
                effective_date = increment.get('effectiveDate')
                if effective_date:
                    increment_month = int(effective_date.split('-')[1])
                    increment_date = int(effective_date.split('-')[2])
                    increment_year=int(effective_date.split('-')[0])

                    if ((increment_month == endmonth and (increment_date) <= endday and increment_year==endyear)) or ((increment_month == startmonth and (increment_date) >= startday) and increment_year==startyear):
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


        ''' TOTAL MONTHLY WORKING DAYS 26-25 CYCLE'''
        total_month_salary_days=total_days['workingDays']+total_days['holydays']
        print("month total days",total_month_salary_days)

        '''SALARY DAYS FROM START DATE TO END DATE'''
        salary_days=data['workingDays']+data['holydays']
        print("salary_dayes",salary_days)
        for key, value in employee_list.items():

            empid = key
            #print(empid)
            emp_data = value
            if emp_data['role']!='Admin':
                emp_name = emp_data['employeeName']

                increment = [d for d in result if d.get('empid') == empid]
                if increment != [] and emp_data['role']=='Employee':
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
                    inc_before_salary = float(increment[0]['grossSalary'])/total_month_salary_days*before_days
                    inc_after_salary = float(increment[0]['total'])/total_month_salary_days*after_days

                    emp_salary_bfr = inc_before_salary

                    lwp_bfr = 0

                    emp_basic_salary_bfr = round((float(emp_salary_bfr) * 0.5), 2)

                    if emp_salary_bfr >= 15000:

                        emp_hra_bfr = 7500

                        emp_da_bfr = 0

                        other_allowance_bfr = round((emp_salary_bfr - emp_basic_salary_bfr - emp_hra_bfr - emp_da_bfr), 2)

                    else:

                        emp_hra_bfr = round((emp_salary_bfr - emp_basic_salary_bfr), 2)

                        emp_da_bfr = 0

                        other_allowance_bfr = round((emp_salary_bfr - emp_basic_salary_bfr - emp_hra_bfr - emp_da_bfr), 2)

                    incentive_bfr = 0

                    arrears_bfr = 0

                    grs_outstanding_adjustment_bfr = 0

                    statutory_bns_bfr = 0


                    if emp_data['epfo_status'] == 'True':

                        if emp_salary_bfr <= 22000:
                            epfo_bfr = round(((emp_salary_bfr - emp_hra_bfr) * 0.24), 2)

                            if epfo_bfr <= 3600:
                                epfo_bfr = epfo_bfr
                            else:
                                epfo_bfr = 3600

                        else:

                            epfo_bfr = 3600

                        if emp_data['abry'] == 'True':

                            epfo_earning = epfo_bfr

                        else:

                            epfo_earning = 0

                    else:
                        epfo_bfr = 0
                        epfo_earning = 0


                    ded_outstanding_adjustment_bfr = 0

                    pt_bfr = 0

                    tds_bfr = round((TDSData(db=self.db).deduction(id=empid, epfo=epfo_bfr, companyname=self.companyname)), 2)
                    other_deduction_bfr = 0
                    leave_deduction_bfr = 0

                    gross_salary_bfr = round((
                            emp_basic_salary_bfr + emp_hra_bfr + emp_da_bfr + other_allowance_bfr + incentive_bfr + arrears_bfr + grs_outstanding_adjustment_bfr + statutory_bns_bfr + epfo_earning),
                        2)

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

                        other_allowance_aft = round((emp_salary_aft - emp_basic_salary_aft - emp_hra_aft - emp_da_aft), 2)

                    else:

                        emp_hra_aft = round((emp_salary_aft - emp_basic_salary_aft), 2)

                        emp_da_aft = 0

                        other_allowance_aft = round((emp_salary_aft - emp_basic_salary_aft - emp_hra_aft - emp_da_aft), 2)

                    incentive_aft = 0

                    arrears_aft = 0

                    grs_outstanding_adjustment_aft = 0

                    statutory_bns_aft = 0

                    if emp_data['epfo_status'] == 'True':

                        if emp_salary_aft <= 22000:
                            epfo_aft = round(((emp_salary_aft - emp_hra_aft) * 0.24), 2)

                            if epfo_aft <= 3600:
                                epfo_aft = epfo_aft
                            else:
                                epfo_aft = 3600

                        else:

                            epfo_aft = 3600

                        if emp_data['abry'] == 'True':

                            epfo_earning = epfo_aft

                        else:

                            epfo_earning = 0

                    else:
                        epfo_aft = 0
                        epfo_earning = 0

                    ded_outstanding_adjustment_aft = 0

                    pt_aft = 0

                    tds_aft = round((TDSData(db=self.db).deduction(id=empid, epfo=epfo_aft, companyname=self.companyname)), 2)

                    other_deduction_aft = 0

                    if lwp_aft > 0:
                        leave_deduction_aft = lwp_aft * (
                            round((float(emp_salary_aft) / num_working_days * float(salary_percentage['deductionpercentage'])),2))
                    else:
                        leave_deduction_aft = 0
                    gross_salary_aft = round((emp_basic_salary_aft + emp_hra_aft + emp_da_aft + other_allowance_aft + incentive_aft + arrears_aft + grs_outstanding_adjustment_aft + statutory_bns_aft + epfo_earning),2)

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
                        'UL': 0, 'OT': "00:00", 'WrkHrs': "00:00", 'CL': 0, 'PL': 0, 'SL': 0, 'totalLeave': 0, 'overtimeAmount': 0,
                        'totalSalary': round((float(increment[0]['total'])), 2),
                        'before_gross':salary_slip_data_bfr['grossSalary'],
                        'after_gross':salary_slip_data_aft['grossSalary'],
                        'incremented_salary':'yes'
                    }
                    salary_total.update({

                        'netSalary': round(salary_total['netSalary'] + float(salary_slip_data["netSalary"]), 2),
                        'grossSalary': round(
                            salary_total['grossSalary'] + float(salary_slip_data["grossSalary"]), 2),
                        'epfo': round(salary_total['epfo'] + float(salary_slip_data["epfo"]), 2),
                        'pt': round(salary_total['pt'] + float(salary_slip_data["pt"]), 2),
                        'tds': round((salary_total['tds'] + float(salary_slip_data["tds"])), 2)
                    })


                    users_ref = self.db.collection(self.companyname).document('employee').collection(
                        'employee').document(empid)

                    users_ref.collection('salaryslips').document(f'sal00{current_month}_{year}').set(salary_slip_data)


                elif emp_data['role']=='Employee' :
                    this_month = int(emp_data['doj'].split('-')[1])
                    this_date = int(emp_data['doj'].split('-')[2])
                    this_year = int(emp_data['doj'].split('-')[0])
                    if ((this_month <= current_month and (this_date) <= 25) or (this_month <= prev_month and (this_date) >= 26) or year>this_year ):

                        emp_salary = round((emp_data['salary'] / 12/total_month_salary_days*salary_days), 2)

                        lwp = 0

                        emp_basic_salary = round(float(emp_salary * 0.5), 2)

                        if emp_salary >= 15000:

                            emp_hra = 7500

                            emp_da = 0

                            other_allowance = round((emp_salary - emp_basic_salary - emp_hra - emp_da), 2)

                        else:

                            emp_hra = round((emp_salary - emp_basic_salary), 2)

                            emp_da = 0

                            other_allowance = round((emp_salary - emp_basic_salary - emp_hra - emp_da), 2)

                        incentive = 0

                        arrears = 0

                        grs_outstanding_adjustment = 0

                        statutory_bns = 0

                        overtime_amount = 0

                        print( emp_data['cosecID'])

                        print(emp_data['epfo_status'], emp_data['cosecID'])

                        if emp_data['epfo_status'] == 'True':
                            if emp_salary <= 22000:
                                epfo = round(((emp_salary - emp_hra) * 0.24), 2)

                                if epfo <= 3600:
                                    epfo=epfo
                                else:
                                    epfo=3600
                            else:
                                epfo = 3600

                            if emp_data['abry'] == 'True':
                                epfo_earning = epfo

                            else:
                                epfo_earning = 0

                        else:

                            epfo = 0

                            epfo_earning = 0

                        ded_outstanding_adjustment = 0

                        pt = 0

                        tds = round((TDSData(db=self.db).deduction(id=empid,epfo=epfo,companyname=self.companyname)), 2)

                        other_deduction = 0

                        leave_deduction = 0

                        gross_salary = round((emp_basic_salary + emp_hra + emp_da + other_allowance + incentive + arrears + grs_outstanding_adjustment + statutory_bns + overtime_amount + epfo_earning), 2)

                        total_deduction = round((epfo + ded_outstanding_adjustment + pt + tds + other_deduction + leave_deduction), 2)

                        net_salary = round((gross_salary - total_deduction), 2)

                        salary_slip_data = {
                            'employeeName': emp_name, 'userID': empid,'slip_id': f'sal00{current_month}_{year}', 'lwp': lwp,
                            'basic': emp_basic_salary, 'da': emp_da, 'hra': emp_hra, 'otherAllowance': other_allowance,
                            'incentive': incentive, 'grsOutstandingAdjustment': grs_outstanding_adjustment, 'arrears': arrears,
                            'statutoryBonus': statutory_bns, 'grossSalary': gross_salary, 'epfo': epfo,
                            'totalSalary': emp_salary,
                            'dedOutstandingAdjustment': ded_outstanding_adjustment, 'pt': pt, 'tds': tds,
                            'otherDeduction': other_deduction, 'leaveDeduction': leave_deduction, 'totalDeduction': total_deduction,
                            'netSalary': net_salary, 'month': current_month, 'year': year, 'cosecID': emp_data['cosecID'], 'WO': 0,
                            'UL': 0, 'OT': "00:00", 'WrkHrs': "00:00", 'CL': 0, 'PL': 0, 'SL': 0, 'totalLeave': 0, 'overtimeAmount': overtime_amount

                        }
                        salary_total.update({

                            'netSalary': round(salary_total['netSalary'] + float(
                                salary_slip_data["netSalary"]), 2),
                            'grossSalary': round(
                                salary_total['grossSalary'] + float(
                                    salary_slip_data["grossSalary"]), 2),
                            'epfo': round(
                                salary_total['epfo'] + float(salary_slip_data["epfo"]),
                                2),
                            'pt': round(
                                salary_total['pt'] + float(salary_slip_data["pt"]), 2),
                            'tds': round(
                                (salary_total['tds'] + float(salary_slip_data["tds"])),
                                2)
                        })
                        users_ref = self.db.collection(self.companyname).document('employee').collection('employee').document(empid)

                        users_ref.collection('salaryslips').document(f'sal00{current_month}_{year}').set(salary_slip_data)

        month_name = calendar.month_name[slipid_month]
        salary_total.update({"startdate":startdate})
        salary_total.update({"enddate":enddate})
        print(salary_total)
        self.db.collection(self.companyname).document('salary_status').update({f'{slipid_year}.{month_name}': 'None',"excel_upload":False})
        self.db.collection(self.companyname).document('monthly_salary_total').update({str(f'{slipid_year}.sal00{slipid_month}_{slipid_year}'): salary_total})

    def excel_calculation(self, salid, excel_data_all, holidays,startdate,enddate):

        startday = int(startdate.split("-")[-1])
        startmonth = int(startdate.split("-")[1])
        startyear = int(startdate.split("-")[0])

        endday = int(enddate.split("-")[-1])
        endmonth = int(enddate.split("-")[1])
        endyear = int(enddate.split("-")[0])


        num_working_days = 0
        Week_off = 0
        working_days_per_week = {}

        holiday = 0
 # # Get the number of days in the current month
        prev_num_days = calendar.monthrange(year, (prev_month))[1]

        prev_month_dates = []
        slipid_month = startmonth
        slipid_year = endyear
        if startmonth != endmonth:
            prev_num_days = calendar.monthrange(startyear, (startmonth))[1]
            # Create a list of all the dates in the current month
            prev_month_dates = [f"{startyear:04}-{startmonth:02}-{day:02}" for day in
                                range(startday, prev_num_days + 1)]
            endmonth_dates = [f"{endyear}-{endmonth}-{day}" for day in range(1, int(endday) + 1)]

            if len(prev_month_dates) > len(endmonth_dates):
                slipid_month = startmonth
                slipid_year = startyear
        else:
            endmonth_dates = [f"{endyear}-{endmonth}-{day}" for day in range(startday, int(endday) + 1)]

        data_date = []
        if holidays != None:
            if startmonth != endmonth:
                count = 0
                for day in range(0, len(dates)):
                    print(dates[day], 'day')
                    # print(endmonth_dates[day - 1])
                    if calendar.weekday(int(dates[day - 1].split('-')[0]), int(dates[day - 1].split('-')[1]),
                                        int(dates[day - 1].split('-')[2])) in (
                            calendar.SATURDAY, calendar.SUNDAY):
                        Week_off += 1
                    elif str(datetime.datetime.strptime(dates[day - 1], "%Y-%m-%d").date()) in holidays:
                        data_date.append(dates[day])
                        print(dates[day], "hol")
                        holiday += 1
                    elif calendar.weekday(int(dates[day - 1].split('-')[0]), int(dates[day - 1].split('-')[1]),
                                          int(dates[day - 1].split('-')[2])) not in (
                            calendar.SATURDAY, calendar.SUNDAY):
                        data_date.append(dates[day])
                        num_working_days += 1


            else:
                print(holidays)
                for day in range(startday, endday + 1):

                    if calendar.weekday(endyear, endmonth, day) in (calendar.SATURDAY, calendar.SUNDAY):
                        print(dates[day - startday], type(dates[day - startday]))
                        Week_off += 1
                    elif str(datetime.datetime.strptime(dates[day - startday], "%Y-%m-%d").date()) in holidays:
                        data_date.append(day - startday)
                        print(dates[day - startday], "hol")
                        holiday += 1
                    elif calendar.weekday(endyear, endmonth, day) not in (calendar.SATURDAY, calendar.SUNDAY):
                        print(dates[day - startday], "wd")

                        data_date.append(day - startday)
                        num_working_days += 1
        data = {
            'weekoff': Week_off,
            'workingDays': num_working_days,
            'holydays': holiday
        }
        salary_total = {'netSalary': 0, 'grossSalary': 0, 'epfo': 0, 'pt': 0, 'tds': 0}

        employee_list_with_increments = (self.db.collection(self.companyname).document('increments').get()).to_dict()

        for data in excel_data_all:
            # print(data)
            new_data = self.db.collection(self.companyname).document(u'employee').collection('employee').where(
                'cosecID', '==', data[" User ID"]).get()
            if len(new_data) != 0:
                emp_data = new_data[0].to_dict()

                empid = emp_data['userID']

                excel_data = {'cosecID': data[" User ID"], 'WO': data["WO"], 'UL': data["UL"],
                              'OT': data["OT"], 'WrkHrs': data[" WrkHrs"], 'paidLeave': data["PL"], 'CL': data["C_L"],
                              'PL': data["P_L"], 'SL': data["S_L"]}

                user_ref = self.db.collection(self.companyname).document('employee').collection('employee').document(
                    empid)

                salary_data = user_ref.collection('salaryslips').document(salid).get().to_dict()

                if salary_data != None:

                    basic = float(salary_data['basic'])

                    hra = float(salary_data['hra'])

                    da = float(salary_data['da'])

                    otherAllowance = float(salary_data['otherAllowance'])

                    arrears = float(salary_data['arrears'])

                    incentive = float(salary_data['incentive'])

                    grsOutstandingAdjustment = float(salary_data['grsOutstandingAdjustment'])
                    statutoryBonus = float(salary_data['statutoryBonus'])

                    statutoryBonus = float(salary_data['statutoryBonus'])

                    totalSalary = float(salary_data['totalSalary'])

                    epfo = float(salary_data['epfo'])

                    if emp_data['abry'] == 'True':
                        epfo_earning = epfo
                    else:
                        epfo_earning = 0

                    pt = float(salary_data['pt'])

                    tds = float(salary_data['tds'])

                    otherDeduction = float(salary_data['otherDeduction'])

                    dedOutstandingAdjustment = float(salary_data['dedOutstandingAdjustment'])

                    working_days = num_working_days

                    month_working_hrs = round((working_days * 9), 2)

                    salary_per_hrs = round((totalSalary / month_working_hrs), 2)

                    unpaid_leaves = float(excel_data['UL'])

                    paid_leaves = float(excel_data['paidLeave'])

                    # emp_working_hrs = float(excel_data['WrkHrs'].split(':')[0]) + round((float(excel_data['WrkHrs'].split(':')[1]) / 60), 2)
                    emp_working_hrs = float(excel_data['WrkHrs'])

                    leave_hrs = (unpaid_leaves + paid_leaves) * 9

                    need_working_hrs = month_working_hrs - leave_hrs

                    lwp = 0

                    leave_deduction = 0

                    if emp_working_hrs < need_working_hrs:
                        remaining_hrs = need_working_hrs - emp_working_hrs

                        lwp += round((remaining_hrs / 9), 2)

                        remaining_hrs_ded = round((remaining_hrs * salary_per_hrs * 2.5), 2)

                        leave_deduction += remaining_hrs_ded

                    if unpaid_leaves > 0:
                        lwp += round(unpaid_leaves, 2)

                        lwp_deduction = round((unpaid_leaves * salary_per_hrs * 9), 2)

                        leave_deduction += lwp_deduction

                    overtime_hrs = float(excel_data['OT'].split(':')[0]) + round(
                        (float(excel_data['OT'].split(':')[1]) / 60), 2)

                    overtime_amount = round((overtime_hrs * salary_per_hrs), 2)

                    gross_salary = round((basic + hra + da + otherAllowance + incentive + arrears + grsOutstandingAdjustment + statutoryBonus + overtime_amount + epfo_earning) , 2)

                    total_deduction = round((epfo + pt + tds + leave_deduction + otherDeduction + dedOutstandingAdjustment), 2)

                    net_salary = round((gross_salary - total_deduction), 2)

                    salary_slip_data = {
                        'lwp': lwp,
                        'basic': basic, 'da': da, 'hra': hra, 'otherAllowance': otherAllowance,
                        'incentive': incentive, 'grsOutstandingAdjustment': grsOutstandingAdjustment,
                        'arrears': arrears,
                        'statutoryBonus': statutoryBonus, 'grossSalary': gross_salary, 'epfo': epfo,
                        'dedOutstandingAdjustment': dedOutstandingAdjustment, 'pt': pt, 'tds': tds,
                        'otherDeduction': otherDeduction, 'leaveDeduction': leave_deduction,
                        'totalDeduction': total_deduction,
                        'netSalary': net_salary, 'overtimeAmount': overtime_amount, 'totalLeave': paid_leaves
                    }

                    salary_slip_data.update(excel_data)

                    user_ref.collection('salaryslips').document(salid).update(salary_slip_data)

                    salary_total.update({
                        'netSalary': round(salary_total['netSalary'] + float(salary_slip_data["netSalary"]), 2),
                        'grossSalary': round(salary_total['grossSalary'] + float(salary_slip_data["grossSalary"]), 2),
                        'epfo': round(salary_total['epfo'] + float(salary_slip_data["epfo"]), 2),
                        'pt': round(salary_total['pt'] + float(salary_slip_data["pt"]), 2),
                        'tds': round((salary_total['tds'] + float(salary_slip_data["tds"])), 2)
                    })

        month_name = calendar.month_name[slipid_month]
        salary_total.update({"startdate": startdate})
        salary_total.update({"enddate": enddate})
        print(salary_total)
        self.db.collection(self.companyname).document('salary_status').update(
            {f'{slipid_year}.{month_name}': 'None', "excel_upload": False})
        self.db.collection(self.companyname).document('monthly_salary_total').update(
            {str(f'{slipid_year}.sal00{slipid_month}_{slipid_year}'): salary_total})

    def erp_excel_calculation(self, salid, excel_data_all, holidays,startdate,enddate):
        startday = int(startdate.split("-")[-1])
        startmonth = int(startdate.split("-")[1])
        startyear = int(startdate.split("-")[0])

        endday = int(enddate.split("-")[-1])
        endmonth = int(enddate.split("-")[1])
        endyear = int(enddate.split("-")[0])

        num_working_days = 0
        Week_off = 0
        working_days_per_week = {}

        holiday = 0

        prev_month_dates = []
        slipid_month = startmonth
        slipid_year = endyear
        if startmonth != endmonth:
            prev_num_days = calendar.monthrange(startyear, (startmonth))[1]
            # Create a list of all the dates in the current month
            prev_month_dates = [f"{startyear:04}-{startmonth:02}-{day:02}" for day in
                                range(startday, prev_num_days + 1)]
            endmonth_dates = [f"{endyear}-{endmonth}-{day}" for day in range(1, int(endday) + 1)]

            if len(prev_month_dates) > len(endmonth_dates):
                slipid_month = startmonth
                slipid_year = startyear
        else:
            endmonth_dates = [f"{endyear}-{endmonth}-{day}" for day in range(startday, int(endday) + 1)]

        # print(endmonth_dates)
        dates = prev_month_dates + endmonth_dates
        print(dates)
        data = {}
        data_date = []
        if holidays != None:
            if startmonth != endmonth:
                count = 0
                for day in range(0, len(dates)):
                    print(dates[day], 'day')
                    # print(endmonth_dates[day - 1])
                    if calendar.weekday(int(dates[day - 1].split('-')[0]), int(dates[day - 1].split('-')[1]),
                                        int(dates[day - 1].split('-')[2])) in (
                            calendar.SATURDAY, calendar.SUNDAY):
                        Week_off += 1
                    elif str(datetime.datetime.strptime(dates[day - 1], "%Y-%m-%d").date()) in holidays:
                        data_date.append(dates[day])
                        print(dates[day], "hol")
                        holiday += 1
                    elif calendar.weekday(int(dates[day - 1].split('-')[0]), int(dates[day - 1].split('-')[1]),
                                          int(dates[day - 1].split('-')[2])) not in (
                            calendar.SATURDAY, calendar.SUNDAY):
                        data_date.append(dates[day])
                        num_working_days += 1


            else:
                print(holidays)
                for day in range(startday, endday + 1):

                    if calendar.weekday(endyear, endmonth, day) in (calendar.SATURDAY, calendar.SUNDAY):
                        print(dates[day - startday], type(dates[day - startday]))
                        Week_off += 1
                    elif str(datetime.datetime.strptime(dates[day - startday], "%Y-%m-%d").date()) in holidays:
                        data_date.append(day - startday)
                        print(dates[day - startday], "hol")
                        holiday += 1
                    elif calendar.weekday(endyear, endmonth, day) not in (calendar.SATURDAY, calendar.SUNDAY):
                        print(dates[day - startday], "wd")

                        data_date.append(day - startday)
                        num_working_days += 1
        data = {
            'weekoff': Week_off,
            'workingDays': num_working_days,
            'holydays': holiday
        }
        salary_total = {'netSalary': 0, 'grossSalary': 0, 'epfo': 0, 'pt': 0, 'tds': 0}

        employee_list_with_increments = (
            self.db.collection(self.companyname).document('increments').get()).to_dict()

        for key, value in excel_data_all.items():

            work_email = key

            wrk_min = value

            # Calculate the hours and minutes
            hours = wrk_min // 60
            minutes = wrk_min % 60

            # Format the hours and minutes as HH:MM
            formatted_time = "{:02d}:{:02d}".format(hours, minutes)

            emp_working_hrs = formatted_time

            new_data = self.db.collection(self.companyname).document(u'employee').collection('employee').where(
                'workEmail', '==', work_email).get()

            if len(new_data) != 0:
                emp_data = new_data[0].to_dict()

                empid = emp_data['userID']

                user_ref = self.db.collection(self.companyname).document('employee').collection(
                    'employee').document(empid)

                salary_data = user_ref.collection('salaryslips').document(salid).get().to_dict()

                if salary_data != None and emp_data['location'] == 'WFH':

                    basic = float(salary_data['basic'])

                    hra = float(salary_data['hra'])

                    da = float(salary_data['da'])

                    otherAllowance = float(salary_data['otherAllowance'])

                    arrears = float(salary_data['arrears'])

                    incentive = float(salary_data['incentive'])

                    grsOutstandingAdjustment = float(salary_data['grsOutstandingAdjustment'])

                    statutoryBonus = float(salary_data['statutoryBonus'])

                    totalSalary = float(salary_data['totalSalary'])

                    epfo = float(salary_data['epfo'])

                    if emp_data['abry'] == 'True':

                        epfo_earning = epfo

                    else:

                        epfo_earning = 0

                    pt = float(salary_data['pt'])

                    tds = float(salary_data['tds'])

                    otherDeduction = float(salary_data['otherDeduction'])

                    dedOutstandingAdjustment = float(salary_data['dedOutstandingAdjustment'])

                    working_days = num_working_days

                    month_working_hrs = round((working_days * 9), 2)

                    salary_per_hrs = round((totalSalary / month_working_hrs), 2)

                    unpaid_leaves = float(salary_data['lwp'])

                    paid_leaves = float(salary_data['totalLeave'])

                    emp_working_hrs = float(emp_working_hrs.split(':')[0]) + round(
                        (float(emp_working_hrs.split(':')[1]) / 60), 2)

                    leave_hrs = (unpaid_leaves + paid_leaves) * 9

                    need_working_hrs = month_working_hrs - leave_hrs

                    lwp = unpaid_leaves

                    leave_deduction = float(salary_data['leaveDeduction'])

                    if emp_working_hrs < need_working_hrs:
                        remaining_hrs = need_working_hrs - emp_working_hrs

                        lwp += round((remaining_hrs / 9), 2)

                        remaining_hrs_ded = round((remaining_hrs * salary_per_hrs * 2.5), 2)

                        leave_deduction += remaining_hrs_ded

                    if unpaid_leaves > 0:
                        lwp += round(unpaid_leaves, 2)

                        lwp_deduction = round((unpaid_leaves * salary_per_hrs * 9), 2)

                        leave_deduction += lwp_deduction

                    overtime_hrs = salary_data['OT']

                    overtime_amount = salary_data['overtimeAmount']

                    gross_salary = round((
                                                     basic + hra + da + otherAllowance + incentive + arrears + grsOutstandingAdjustment + statutoryBonus + overtime_amount + epfo_earning),
                                         2)

                    total_deduction = round(
                        (epfo + pt + tds + leave_deduction + otherDeduction + dedOutstandingAdjustment), 2)

                    net_salary = round((gross_salary - total_deduction), 2)

                    salary_slip_data = {
                        'lwp': lwp,
                        'basic': basic, 'da': da, 'hra': hra, 'otherAllowance': otherAllowance,
                        'incentive': incentive, 'grsOutstandingAdjustment': grsOutstandingAdjustment,
                        'arrears': arrears,
                        'statutoryBonus': statutoryBonus, 'grossSalary': gross_salary, 'epfo': epfo,
                        'dedOutstandingAdjustment': dedOutstandingAdjustment, 'pt': pt, 'tds': tds,
                        'otherDeduction': otherDeduction, 'leaveDeduction': leave_deduction,
                        'totalDeduction': total_deduction,
                        'netSalary': net_salary, 'overtimeAmount': overtime_amount, 'totalLeave': paid_leaves,
                        'WrkHrs': emp_working_hrs
                    }

                    user_ref.collection('salaryslips').document(salid).update(salary_slip_data)

                    salary_total.update({
                        'netSalary': round(salary_total['netSalary'] + float(salary_slip_data["netSalary"]), 2),
                        'grossSalary': round(salary_total['grossSalary'] + float(salary_slip_data["grossSalary"]),
                                             2),
                        'epfo': round(salary_total['epfo'] + float(salary_slip_data["epfo"]), 2),
                        'pt': round(salary_total['pt'] + float(salary_slip_data["pt"]), 2),
                        'tds': round((salary_total['tds'] + float(salary_slip_data["tds"])), 2)
                    })



                elif salary_data != None and emp_data['location'] == 'WFO':

                    salary_total.update({
                        'netSalary': round(salary_total['netSalary'] + float(salary_data["netSalary"]), 2),
                        'grossSalary': round(salary_total['grossSalary'] + float(salary_data["grossSalary"]), 2),
                        'epfo': round(salary_total['epfo'] + float(salary_data["epfo"]), 2),
                        'pt': round(salary_total['pt'] + float(salary_data["pt"]), 2),
                        'tds': round((salary_total['tds'] + float(salary_data["tds"])), 2)
                    })

        month_name = calendar.month_name[slipid_month]
        salary_total.update({"startdate": startdate})
        salary_total.update({"enddate": enddate})
        print(salary_total)
        self.db.collection(self.companyname).document('salary_status').update(
            {f'{slipid_year}.{month_name}': 'None', "excel_upload": False})
        self.db.collection(self.companyname).document('monthly_salary_total').update(
            {str(f'{slipid_year}.sal00{slipid_month}_{slipid_year}'): salary_total})