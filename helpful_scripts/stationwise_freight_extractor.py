import time
import os
import pandas as pd
from pandas import ExcelWriter
pd.set_option('display.max_columns', 100)

df = pd.read_csv('/home/nawedx/Downloads/MisOwtdFrgtRgtr.csv', skiprows=2)
df.columns = df.columns.str.replace(' ', '_')
df['RR_NUMBER'] = df['RR_NUMBER'].fillna(0).astype(int)
df['CMDT_CODE'] = df['CMDT_CODE'].fillna(0).astype(int)
df['INVOICE_NO.'] = df['INVOICE_NO.'].fillna(0).astype(int)
df = df[df.RR_NUMBER != 0]
print('Outward Freight Register Loaded')
#print(df.head())
rrList = df['RR_NUMBER'].values
#print(rrList)
listlen = len(rrList)
df = df[['STATION_FROM', 'STATION_TO', 'RR_NUMBER', 'RR_DATE', 'CMDT_CODE', 'WEIGHT_CHRG', 'FINAL_FRGT_(incl.SrvcTax/GST)']]
df['cop'] = df['STATION_FROM']
#print(df)
df2 = pd.read_table('/home/nawedx/Downloads/TrfcErngLdng.xls', skiprows=2)
df2.columns = df2.columns.str.replace(' ', '_')
print('Traffic Earning Loaded')
df2 = df2[['RR_NUMB', 'RR_DATE', 'CMDT']]

df3 = df.merge(df2, left_on=['RR_NUMBER', 'RR_DATE'], right_on=['RR_NUMB', 'RR_DATE'], how='left')
print('MERGED')

dict2 = {'BBMT':'TLHR', 'ACTR':'TLHR', 'SBCT':'TLHR', 'BCMT':'TLHR', 'MGCT':'TLHR', 'DBCS':'TLHR', 'LMGT':'TLHR', 'BGMT':'TLHR', 'CBSP':'PRDP', 'PPAP':'PRDP', 'PMIP':'PRDP', 'PPTP':'PRDP'}

for i in range(len(df3.index)):
	if df3['STATION_FROM'][i] in dict2:
		df3['STATION_FROM'][i] = dict2[df3['STATION_FROM'][i]]

df3 = df3.sort_values(by=['STATION_FROM','CMDT'], ascending=[True, True])

stnList = sorted(list(set(df3['STATION_FROM'].values)))
print(stnList)

df5 = pd.DataFrame(columns=['STATION_FROM', 'CMDT', 'TOTAL_WEIGHT_CHRG', 'FINAL_FRGT_(incl.SrvcTax/GST)'])

for i in stnList:
	df = df3[df3.STATION_FROM == i]
	cmdtList = df.CMDT.unique()
	for j in cmdtList:
		df1 = df[df.CMDT == j]
		totalCharge = df1['WEIGHT_CHRG'].sum()
		totalFreight = df1['FINAL_FRGT_(incl.SrvcTax/GST)'].sum()
		#print(i, j, totalCharge, totalFreight)
		df5 = df5.append({'STATION_FROM':i, 'CMDT':j, 'TOTAL_WEIGHT_CHRG':totalCharge, 'FINAL_FRGT_(incl.SrvcTax/GST)':totalFreight}, ignore_index=True)
		print(df5)
	
'''
writer = ExcelWriter('merged_freight_register.xls')
df3.to_excel(writer,'Sheet1')
writer.save()
'''
writer = ExcelWriter('merged_sorted_stationwise.xls')
df3.to_excel(writer,'Sheet1')
writer.save()

writer = ExcelWriter('stationwise_total_freight_details.xls')
df5.to_excel(writer,'Sheet1')
writer.save()
print('Done\n')
input()