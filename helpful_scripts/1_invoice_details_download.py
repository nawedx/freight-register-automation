#Script to Download Invoice Details from RMS Queries of FOIS
#Written by Nawed Imroze (nawedx)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
import pandas as pd
from pandas import ExcelWriter
pd.set_option('display.max_columns', 100)

#Initializes the webdriver and starts the browser
browser = webdriver.Firefox()
browser.get("http://fois.indianrail.gov.in/rmsdqweb/view/GG_LoginMainPrtlRQ.jsp")
#browser.maximize_window()

#Checks until the Submit button has been loaded
#I have made the assumption that if submit button is loaded all other fields before it has alse been loaded.
login_attempt = None
while not login_attempt:
	try:
		login_attempt = browser.find_element_by_xpath('//*[@id="Submit"]')
	except NoSuchElementException:
		time.sleep(1)

#Finds the required login details
username = browser.find_element_by_xpath('//*[@id="txtUserId"]')
password = browser.find_element_by_xpath('//*[@id="txtPassword"]')
location = browser.find_element_by_xpath('//*[@id="txtLocation"]')


#The credentials for login has been kep in a different file and I won't upload it on github.
#It will only be given to those who want to contribute to this project
import credentials

#Fits the login credentials and clicks on Submit
username.send_keys(credentials.uname)
password.send_keys(credentials.pwd)
location.send_keys(credentials.loc)
login_attempt.submit()
time.sleep(3)
login_attempt.submit()
time.sleep(3)

#Waits for the page and the elements to load and goes to required page i.e "Invoice Details"
invc = None
while not invc:
	try:
		invc = browser.find_element_by_xpath('//td[. = "Operations Control"]')
	except NoSuchElementException:
		time.sleep(1)
invc.click()
ftdetails = browser.find_element_by_xpath('//td[. = "Miscelleneous"]')
ftdetails.click()
ftdetails = browser.find_element_by_xpath('//td[. = "Invoice Details"]')
ftdetails.click()

#Switches to appropriate frame.
frame2 = None
while not frame2:
	try:
		frame2 = browser.find_element_by_xpath('//iframe[@name="frmInpt"]')
	except NoSuchElementException:
		time.sleep(1)
browser.switch_to.frame(frame2)

#Waits until Date range is selected and a key is pressed in the program to continue
print('Please select proper date range and press any key to continue : ')



inp = input()

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
time.sleep(1)
excelDown = browser.find_element_by_link_text('Excel')
excelDown.click()

#To confirm that Invoice Details is downloaded
print('Please check whether InvcDtls.xls is downloaded and press any key : ')
inp = input()

browser.switch_to.default_content()

invc = None
while not invc:
	try:
		invc = browser.find_element_by_xpath('//td[. = "Managerial Set"]')
	except NoSuchElementException:
		time.sleep(1)
invc.click()
ftdetails = browser.find_element_by_xpath('//td[. = "Demand"]')
ftdetails.click()
ftdetails = browser.find_element_by_xpath('//td[. = "Area wise Loading/Unloading (Details)"]')
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


total = None
while not total:
	try:
		total = browser.find_element_by_xpath('/html/body/center/div[2]/table/tbody/tr[1]/td[1]').text
	except NoSuchElementException:
		time.sleep(1)

i=1
while total != 'TOTAL':
	total = browser.find_element_by_xpath('/html/body/center/div[2]/table/tbody/tr['+str(i)+']/td[1]').text
	i = i + 1

rakesLoaded = browser.find_element_by_xpath('/html/body/center/div[2]/table/tbody/tr['+str(i-1)+']/td[8]').text
with open("rakes_loaded.txt", "w+") as text_file:
	print("{}".format(rakesLoaded), file=text_file)

print("Done")

inp = input()

browser.quit()