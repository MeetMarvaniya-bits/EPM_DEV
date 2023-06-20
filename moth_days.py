import datetime
import calendar


class MonthCount():

    def __init__(self):
        pass

    def count(self, holidays):
        """ COUNT CURRENT MONTH WORKING DAYS FOR DASHBOARD """
        # Get current year and month
        today = datetime.date.today()
        year = today.year
        month = today.month
        if month==1:
            prev_month=11
            current_month=12
        elif month == 2:
            prev_month=12
            current_month=1
        else:
            prev_month=month-2
            current_month=month-1

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
        prev_month_dates = [f"{year:04}-{prev_month:02}-{day:02}" for day in range(26, prev_num_days+1)]
        current_month_dates=[f"{year:04}-{current_month:02}-{day:02}" for day in range(1, 26)]
        dates=prev_month_dates+current_month_dates
        #print(dates)
        data_date = []
        if holidays != None:
            for day in range(1, len(prev_month_dates)+1):
                if current_month_dates[day-1] in holidays:
                    holiday += 1
                elif calendar.weekday(year, prev_month, day) not in (calendar.SATURDAY, calendar.SUNDAY):
                    data_date.append(current_month_dates[day-1])
                    num_working_days += 1
                else:
                    Week_off += 1
            for day in range(1,26):
                #print(current_month_dates[day-1])
                if dates[day - 1] in holidays:
                    holiday += 1
                elif calendar.weekday(year, current_month, day) not in (calendar.SATURDAY, calendar.SUNDAY):
                    data_date.append(current_month_dates[day-1])
                    num_working_days += 1
                else:
                    Week_off += 1

        data = {
            'weekoff': Week_off,
            'workingDays': num_working_days,
            'holydays': holiday
        }


        #print(data_date)
        target_date = '2023-05-12'

        lesser_dates = 0
        greater_dates = 0

        for date in data_date:
            if date <= target_date:
                lesser_dates += 1
            else:
                greater_dates += 1

        #print("Number of dates <= target date:", lesser_dates)
        #print("Number of dates > target date:", greater_dates)
        #print('curreent',data)
        return data
    # def count(self, holidays):
    #     """ COUNT CURRENT MONTH WORKING DAYS FOR DASHBOARD """
    #     # Get current year and month
    #     today = datetime.date.today()
    #     year = today.year
    #     month = today.month
    #     # Get number of days in the current month and the day of the week of the first day
    #     first_day, num_days = calendar.monthrange(year, month)
    #     # Loop through days and count working days
    #     num_working_days = 0
    #     Week_off = 0
    #     working_days_per_week = {}
    #     # holidays=holidays.keys()
    #     holiday = 0
    #
    #     # Get the number of days in the current month
    #     num_days = calendar.monthrange(year, month)[1]
    #
    #     # Create a list of all the dates in the current month
    #     dates = [f"{year:04}-{month:02}-{day:02}" for day in range(1, num_days + 1)]
    #
    #     data = {}
    #     if holidays != None:
    #         for day in range(1, num_days + 1):
    #             # print(dates[day - 1])
    #
    #             if dates[day - 1] in holidays:
    #                 holiday += 1
    #             elif calendar.weekday(year, month, day) not in (calendar.SATURDAY, calendar.SUNDAY):
    #                 num_working_days += 1
    #             else:
    #                 Week_off += 1
    #
    #         data = {
    #             'weekoff': Week_off,
    #             'workingDays': num_working_days,
    #             'holydays': holiday
    #         }
    #     return data

    def count_previous(self, holidays):
        """ COUNT CURRENT MONTH WORKING DAYS FOR DASHBOARD """
        # Get current year and month
        today = datetime.date.today()
        year = today.year
        month = today.month
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
        #print(dates)
        data = {}
        if holidays != None:
            for day in range(1, len(prev_month_dates) + 1):
                # print(dates[day - 1])
                #print(current_month_dates[day - 1])
                if current_month_dates[day - 1] in holidays:
                    holiday += 1
                elif calendar.weekday(year, prev_month, day) not in (calendar.SATURDAY, calendar.SUNDAY):
                    num_working_days += 1
                else:
                    Week_off += 1
            for day in range(1, 26):
                #print(current_month_dates[day - 1])
                if dates[day - 1] in holidays:
                    holiday += 1
                elif calendar.weekday(year, current_month, day) not in (calendar.SATURDAY, calendar.SUNDAY):
                    num_working_days += 1
                else:
                    Week_off += 1

        data = {
            'weekoff': Week_off,
            'workingDays': num_working_days,
            'holydays': holiday
        }
        #print('curreent', data)
        return data

    def count_previous_month(self, holidays, salid):
        """ COUNT SALARYID MONTH WORKING DAYS FOR SALARY SLIP """
        # Get current year and month
        today = datetime.date.today()
        year=today.year
        #print(salid.split("_"))
        salid=salid.split("_")[0]
        #print(salid)
        month = int(salid[-3:])
        #print(month)
        if month == 1:
            prev_month = 12
            current_month = 1
        else:
            prev_month = month - 1
            current_month = month

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
        #print(dates)
        data = {}
        if holidays != None:
            for day in range(1, len(prev_month_dates) + 1):
                # print(dates[day - 1])
                #print(current_month_dates[day - 1])
                if current_month_dates[day - 1] in holidays:
                    holiday += 1
                elif calendar.weekday(year, prev_month, day) not in (calendar.SATURDAY, calendar.SUNDAY):
                    num_working_days += 1
                else:
                    Week_off += 1
            for day in range(1, 26):
                #print(current_month_dates[day - 1])
                if dates[day - 1] in holidays:
                    holiday += 1
                elif calendar.weekday(year, current_month, day) not in (calendar.SATURDAY, calendar.SUNDAY):
                    num_working_days += 1
                else:
                    Week_off += 1

        data = {
            'weekoff': Week_off,
            'workingDays': num_working_days,
            'holydays': holiday
        }
        #print('curreent', data)
        return data

    def get_holidays(self, holidays):
        # Convert the date strings to datetime objects
        sorted_data = {}
        if holidays != None:
            date_objs = [datetime.datetime.strptime(date_str, '%Y-%m-%d') for date_str in holidays.keys()]
            # Group the data by month
            data_by_month = {}
            for date_obj, value in zip(date_objs, holidays.values()):
                month_str = date_obj.strftime('%B %Y')
                if month_str not in data_by_month:
                    data_by_month[month_str] = {}
                data_by_month[month_str][date_obj] = value

            # Sort the data by month and date
            for month_str in sorted(data_by_month.keys(), key=lambda x: datetime.datetime.strptime(x, '%B %Y')):
                sorted_data[month_str] = {}
                for date_obj in sorted(data_by_month[month_str].keys()):
                    date_str = date_obj.strftime('%Y-%m-%d')
                    value = data_by_month[month_str][date_obj]
                    sorted_data[month_str][date_str] = value
        return sorted_data




