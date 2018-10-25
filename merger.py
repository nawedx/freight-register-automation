from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
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
df = df[['STATION_FROM', 'STATION_TO', 'RR_NUMBER', 'RR_DATE', 'CMDT_CODE', 'WEIGHT_CHRG', 'TOTAL_FRGT']]
print(df)
df2 = pd.read_table('/home/nawedx/Downloads/TrfcErngLdng.xls', skiprows=2)
df2.columns = df2.columns.str.replace(' ', '_')
print('Traffic Earning Loaded')
df2 = df2[['RR_NUMB', 'RR_DATE', 'CMDT']]

df3 = df.merge(df2, left_on=['RR_NUMBER', 'RR_DATE'], right_on=['RR_NUMB', 'RR_DATE'], how='left')
print('MERGED')

writer = ExcelWriter('merged_freight_register.xls')
df3.to_excel(writer,'Sheet1')
writer.save()

input()
