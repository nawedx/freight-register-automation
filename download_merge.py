from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
import pandas as pd
from pandas import ExcelWriter
pd.set_option('display.max_columns', 100)

rrList = [10]
folderName = os.path.join(os.path.expanduser("~/"), "freight-register-automation")
fileName = 'RR-'+str(rrList[0])+'.pdf'
profile = webdriver.FirefoxProfile(folderName)
profile.set_preference('print.always_print_silent', True)
profile.set_preference("print_printer", "PDF")
profile.set_preference('print.print_to_file', True)
profile.set_preference('print.print_to_filename', fileName)

import traffic_earning_download

browser = webdriver.Firefox()
browser.get("https://www.fois.indianrail.gov.in/FoisWebsite/jsp/RMS_Zonal.jsp?txtProjName=TZ")
#browser.maximize_window()

frame = None 
while not frame:
	try: 
		frame = browser.find_element_by_xpath('//frame[@name="frmApplLgin"]')
	except NoSuchElementException:
		time.sleep(1)
browser.switch_to.frame(frame)
login_attempt = None
while not login_attempt:
	try: 
		login_attempt = browser.find_element_by_id('Submit')
	except NoSuchElementException:
		time.sleep(1)

username = browser.find_element_by_name('txtUserId')
password = browser.find_element_by_id('txtPassword')
radiobut = None
while not radiobut:
	try: 
		radiobut = browser.find_element_by_id('txtOptnD')
	except NoSuchElementException:
		time.sleep(1)

import credentials
location = browser.find_element_by_id('txtLocation')
username.send_keys(credentials.uname)
password.send_keys(credentials.pwd)
radiobut.click()
location.send_keys(credentials.loc)
login_attempt = browser.find_element_by_id('Submit')
login_attempt.submit()
time.sleep(3)
login_attempt.submit()
time.sleep(3)

newWindow = browser.window_handles[1]
browser.switch_to.window(newWindow)
outward = None
while not outward:
	try:
		outward = browser.find_element_by_xpath('//td[. = "Outward"]')
	except NoSuchElementException:
		time.sleep(1)
outward.click()
ftdetails = browser.find_element_by_xpath('//td[. = "Freight Details"]')
ftdetails.click()

frame2 = None
while not frame2:
	try:
		frame2 = browser.find_element_by_xpath('//iframe[@name="frmInpt"]')
	except NoSuchElementException:
		time.sleep(1)
browser.switch_to.frame(frame2)
submitButton = None
while not submitButton:
	try:
		submitButton = browser.find_element_by_id('Submit')
	except NoSuchElementException:
		time.sleep(1)
submitButton.click()
time.sleep(3)

showAll = None
while not showAll:
	try:
		showAll = browser.find_element_by_link_text('Show All')
	except NoSuchElementException:
		time.sleep(1)
showAll.click()

browser.switch_to.default_content()
frm = browser.find_element_by_xpath('//iframe[@name="frmInpt"]')
browser.switch_to.frame(frm)

excelDown = browser.find_element_by_link_text('Excel')
excelDown.click()
print('Please check whether MisOwtdFrgtRgtr.xls is downloaded and press any key : ')
inp = raw_input()

df = pd.read_table('/home/nawedx/Downloads/MisOwtdFrgtRgtr.xls', skiprows=2)
df.columns = df.columns.str.replace(' ', '_')
df['RR_NUMBER'] = df['RR_NUMBER'].fillna(0).astype(int)
df['CMDT_CODE'] = df['CMDT_CODE'].fillna(0).astype(int)
df['INVOICE_NO.'] = df['INVOICE_NO.'].fillna(0).astype(int)
df = df[df.RR_NUMBER !=0 ]
print('Outward Freight Register Loaded')
rrList = df['RR_NUMBER'].values
listlen = len(rrList)

df2 = pd.read_table('/home/nawedx/Downloads/TrfcErngLdng.xls', skiprows=2)
df2.columns = df2.columns.str.replace(' ', '_')
print('Traffic Earning Loaded')

df3 = df.merge(df2, left_on=['RR_NUMBER', 'RR_DATE'], right_on=['RR_NUMB', 'RR_DATE'], how='left')
print('MERGED')
#print(df3.head())

list1 = list(df3)
list1 = list1[:5] + list1[-11:-6] + list1[-15:-13] + list1[6:-17]
#print(list1)
df3 = df3[list1]

writer = ExcelWriter('merged_freight_register.xls')
df3.to_excel(writer,'Sheet1')
writer.save()

browser.quit()