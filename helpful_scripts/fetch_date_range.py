from datetime import date, timedelta
fromdate = str((date.today()-timedelta(3)).day)
todate = str((date.today()-timedelta(1)).day)
print(str(date.today().day)+'-'+str(date.today().month)+'-'+str(date.today().year))