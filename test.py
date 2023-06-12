import datetime


st=datetime.datetime.now()
squared_numbers = []


for num in range(0,1000):
    squared_numbers.append(num**2)

endt=datetime.datetime.now()



st=datetime.datetime.now()
squared_numbers = [num**2 for num in range(0,1000)]

endt=datetime.datetime.now()




data=["increment_01","increment_02","increment_03","increment_04","increment_05","increment_06"]