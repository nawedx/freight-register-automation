from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
import pandas as pd
from pandas import ExcelWriter
pd.set_option('display.max_columns', 100)

df = pd.read_excel('/home/nawedx/Downloads/MisOwtdFrgtRgtr.xls', skiprows=2)
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

df2 = pd.read_table('/home/nawedx/Downloads/TrfcErngLdng.xls', skiprows=2)
df2.columns = df2.columns.str.replace(' ', '_')
print('Traffic Earning Loaded')

df3 = df.merge(df2, left_on=['RR_NUMBER', 'RR_DATE'], right_on=['RR_NUMB', 'RR_DATE'], how='left')
print('MERGED')

#print(df3.head())
'''
list1 = list(df3)
list1 = list1[:5] + list1[-11:-6] + list1[-15:-13] + list1[6:-17]
#print(list1)
df3 = df3[list1]
'''
writer = ExcelWriter('merged_freight_register.xls')
df3.to_excel(writer,'Sheet1')
writer.save()

raw_input()
