#Script to download Outward Freight Register from TMS Queries of FOIS
#Written by Nawed Imroze (nawedx)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
import pandas as pd
from pandas import ExcelWriter
pd.set_option('display.max_columns', 100)

#Firefox profile initialization
profile = webdriver.FirefoxProfile()
profile.set_preference("print_printer", 'Foxit Reader PDF Printer')
profile.set_preference("print.always_print_silent", True)
profile.set_preference("print.show_print_progress", True)

#Initializes the webdriver and starts the browser
browser = webdriver.Firefox(profile)
browser.get("https://www.fois.indianrail.gov.in/FoisWebsite/jsp/RMS_Zonal.jsp?txtProjName=TZ")
#browser.maximize_window()

#Switches to correct frame
frame = None
while not frame:
	try:
		frame = browser.find_element_by_xpath('//frame[@name="frmApplLgin"]')
	except NoSuchElementException:
		time.sleep(1)
browser.switch_to.frame(frame)

#Checks until the Submit button has been loaded
#I have made the assumption that if submit button is loaded all other fields before it has alse been loaded.
login_attempt = None
while not login_attempt:
	try:
		login_attempt = browser.find_element_by_id('Submit')
	except NoSuchElementException:
		time.sleep(1)

#Finds the required login details
username = browser.find_element_by_name('txtUserId')
password = browser.find_element_by_id('txtPassword')
radiobut = None
while not radiobut:
	try:
		radiobut = browser.find_element_by_id('txtOptnD')
	except NoSuchElementException:
		time.sleep(1)

#The credentials for login has been kep in a different file and I won't upload it on github.
#It will only be given to those who want to contribute to this project
import credentials

#Fits the login credentials and clicks on Submit
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

#Switches to the new window as the Submit open a new window
newWindow = browser.window_handles[1]
browser.switch_to.window(newWindow)

#Waits for the page and the elements to load and goes to required page i.e "Freight Details"
outward = None
while not outward:
	try:
		outward = browser.find_element_by_xpath('//td[. = "Outward"]')
	except NoSuchElementException:
		time.sleep(1)
outward.click()
ftdetails = browser.find_element_by_xpath('//td[. = "Freight Details"]')
ftdetails.click()

#Switches to appropriate frame.
frame2 = None
while not frame2:
	try:
		frame2 = browser.find_element_by_xpath('//iframe[@name="frmInpt"]')
	except NoSuchElementException:
		time.sleep(1)
browser.switch_to.frame(frame2)

#Selects the RR-Base radio button
radioRRBut = None
while not radioRRBut:
	try:
		radioRRBut = browser.find_element_by_xpath(".//input[@type='radio' and @value='R']")
	except NoSuchElementException:
		time.sleep(1)
radioRRBut.click()

#Waits until Date range is selected and a key is pressed in the program to continue
print('Please select proper date range and press any key to continue : ')
inp = raw_input()

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

#To confirm that the Freight Register is downloaded
print('Please check whether MisOwtdFrgtRgtr.xls is downloaded and press any key : ')
inp = raw_input()
browser.quit()
