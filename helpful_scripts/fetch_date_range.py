from datetime import date, timedelta, datetime
import time
fromdate = str((date.today()-timedelta(3)).month)
todate = str((date.today()-timedelta(1)).month)
#print(str(date.today().day)+'-'+str(date.today().month)+'-'+str(date.today().year))
print(fromdate, todate)

strDate = '12/10/18'
objDate = datetime.strptime(strDate, '%m/%d/%y')
print(objDate)
#datetime.datetime(2018, 2, 4, 0, 0)

ts = time.time()
currentTimeStamp = datetime.fromtimestamp(ts).strftime('%d-%m-%Y--%H-%M-%S')
print(str(currentTimeStamp))