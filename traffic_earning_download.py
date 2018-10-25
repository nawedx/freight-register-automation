#Script to Download Traffic Earnings from RMS Queries of FOIS
#Written by Nawed Imroze (nawedx)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
import pandas as pd
from pandas import ExcelWriter
pd.set_option('display.max_columns', 100)

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

#Waits for the page and the elements to load and goes to required page i.e "Traffic Earnings"
traffic = None
while not traffic:
	try:
		traffic = browser.find_element_by_xpath('//td[. = "Managerial Set"]')
	except NoSuchElementException:
		time.sleep(1)
traffic.click()
ftdetails = browser.find_element_by_xpath('//td[. = "Demand"]')
ftdetails.click()
ftdetails = browser.find_element_by_xpath('//td[. = "Traffic Earnings"]')
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

#To confirm that the Freight Register is downloaded
print('Please check whether TrfcErngLdng.xls is downloaded and press any key : ')
inp = input()
browser.quit()