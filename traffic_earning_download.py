from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
import pandas as pd
from pandas import ExcelWriter
pd.set_option('display.max_columns', 100)

browser = webdriver.Firefox()
browser.get("https://www.fois.indianrail.gov.in/FoisWebsite/jsp/RMS_Zonal.jsp?txtProjName=RQ")
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
location = browser.find_element_by_id('txtLocation')
username.send_keys('KURACM')
password.send_keys('pps')
radiobut.click()
location.send_keys('KUR')
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
		outward = browser.find_element_by_xpath('//td[. = "Managerial Set"]')
	except NoSuchElementException:
		time.sleep(1)
outward.click()
ftdetails = browser.find_element_by_xpath('//td[. = "Demand"]')
ftdetails.click()
ftdetails = browser.find_element_by_xpath('//td[. = "Traffic Earnings"]')
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
print('Please check whether TrfcErngLdng.xls is downloaded and press any key : ')
inp = raw_input()
browser.quit()