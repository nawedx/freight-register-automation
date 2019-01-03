from datetime import date, timedelta, datetime
fromdate = str((date.today()-timedelta(3)).day)
todate = str((date.today()-timedelta(1)).day)
print(str(date.today().day)+'-'+str(date.today().month)+'-'+str(date.today().year))

strDate = '12/10/18'
objDate = datetime.strptime(strDate, '%m/%d/%y')
print(objDate)
#datetime.datetime(2018, 2, 4, 0, 0)