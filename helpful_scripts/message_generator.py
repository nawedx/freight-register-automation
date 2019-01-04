import os, time, sys, datetime
import pandas as pd
from pandas import ExcelWriter
pd.set_option('display.max_columns', 10)
#sys.stdout = open('runlog', 'w')

downloadPath = '/home/nawedx/Downloads/'

def readAndClean(filename):
	df = pd.read_table(filename, skiprows=2)
	df.columns = df.columns.str.replace(' ', '_')
	df['INVOICE_NUMB'] = df['INVOICE_NUMB'].fillna(0).astype(int)
	df = df[df.INVOICE_NUMB != 0]
	#print(df)
	print('Invoice Details Loaded\n')
	return df

def writeToExcel(df, i, filename='processed_invoice_details'):
	writer = ExcelWriter(filename+str(i)+'.xls')
	df.to_excel(writer,'Sheet1')
	writer.save()

def writeToTextfile(invoiceDates, rrGen, rrPending):
    with open('rakes_loaded.txt', 'r') as f:
        numberRakeLoaded = f.read().splitlines()

    with open("invoice_generated_datewise.txt", "w+") as text_file:
        print("Sir, freight loading and RR issued on {}.".format(invoiceDates[2]), file=text_file)
        print("Total Rakes Loaded on Dt. {} is {}.".format(invoiceDates[2], numberRakeLoaded[0]), file=text_file)
        for n in reversed(range(0, 3)):
            if rrGen[invoiceDates[n]] != 0:
                print("RR issued on account of {} is {}.".format(invoiceDates[n], rrGen[invoiceDates[n]]), file=text_file)   
        for n in reversed(range(0, 3)):
            if rrPending[invoiceDates[n]] != 0:
                print("Pending RR on account of {} is {}.".format(invoiceDates[n], rrPending[invoiceDates[n]]), file=text_file)   
        print("Regards.", file=text_file)
    print('\nMessage generated and written to text file.\n')

        
filename = 'InvcDtls'
df = readAndClean(downloadPath+filename+'.xls')

invoiceDates = sorted(df['INVOICE_DATE'].unique())
dates = [datetime.datetime.strptime(ts, "%d-%m-%y") for ts in invoiceDates]
dates.sort()
invoiceDates = [datetime.datetime.strftime(ts, "%d-%m-%y") for ts in dates]
print(invoiceDates)

rrGen = {}
rrPending = {}
df['RR_NUMB'] = df['RR_NUMB'].fillna(0).astype(int)
for i in range(3):
    df1 = df[df.INVOICE_DATE == invoiceDates[i]]
    df2 = df1[df1.RR_DATE == invoiceDates[2]]       
    rrGen[invoiceDates[i]] = df2.RR_DATE.count()
    df3 = df1[df1.RR_DATE > invoiceDates[2]]
    df4 = df1[df1.RR_NUMB == 0]
    rrPending[invoiceDates[i]] = df3['INVOICE_DATE'].count() + df4['INVOICE_DATE'].count()
        
print('\nRR generated against dates : ')
print(rrGen)
print('\nRR pending against dates : ')
print(rrPending)
writeToTextfile(invoiceDates, rrGen, rrPending)