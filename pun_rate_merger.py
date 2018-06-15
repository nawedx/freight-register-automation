from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
import pandas as pd
from pandas import ExcelWriter
pd.set_option('display.max_columns', 100)

df3 = pd.read_excel('merged_freight_register.xls')
df2 = pd.read_excel('RR-POL.xls')

df3 = df3.merge(df2, left_on=['RR_NUMBER'], right_on=['RR_Num'], how='left')
print('MERGED PUN Rate')

writer = ExcelWriter('Final_freight_register.xls')
df3.to_excel(writer, 'Sheet1')
writer.save()
#print(df3.head())
'''
list1 = list(df3)
list1 = list1[:5] + list1[-11:-6] + list1[-15:-13] + list1[6:-17]
#print(list1)
df3 = df3[list1]
'''
