from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
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
#I have made the assumption that if submit button is loaded all other fields before it has also been loaded.
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

#Switches to the new window as the Submit opens a new window
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
try:
    WebDriverWait(browser, 3).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')
    alert = browser.switch_to.alert
    alert.accept()
    print("alert accepted")
except TimeoutException:
    print("no alert")

df3 = pd.read_excel('merged_freight_register.xls')
rrList = df3['RR_NUMBER'].values
print(rrList)
listlen = len(rrList)
df_RR_pol = pd.DataFrame(columns=['RR_Num', 'AT_PUN_RATE'])
j = 0

for i in rrList:
	#print(str(i))
	rrDate = df3['RR_DATE'][j]
	browser.switch_to.default_content()
	frm = None
	while not frm:
		try:
			frm = browser.find_element_by_xpath('//iframe[@name="frmInpt"]')
		except NoSuchElementException:
			time.sleep(1)
	browser.switch_to.frame(frm)
	print(1)

	showAll = None
	while not showAll:
		try:
			showAll = browser.find_element_by_link_text('Show All')
		except NoSuchElementException:
			time.sleep(1)
	showAll.click()
	print(2)

	browser.switch_to.default_content()
	frm = None
	while not frm:
		try:
			frm = browser.find_element_by_xpath('//iframe[@name="frmInpt"]')
		except NoSuchElementException:
			time.sleep(1)
	browser.switch_to.frame(frm)
	print(3)

	link = None
	while not link:
		try:
			link = browser.find_element_by_link_text(str(i))
		except NoSuchElementException:
			time.sleep(1)
	link.click()

	browser.switch_to.default_content()
	frm = None
	while not frm:
		try:
			frm = browser.find_element_by_xpath('//iframe[@name="frmInpt"]')
		except NoSuchElementException:
			time.sleep(1)
	browser.switch_to.frame(frm)

	print(4)
	frame3 = None
	while not frame3:
		try:
			frame3 = browser.find_element_by_xpath('//iframe[@name="frmDtls"]')
		except NoSuchElementException:
			time.sleep(1)

	browser.switch_to.frame(frame3)

	print(5)
	frame4 = None
	while not frame4:
		try:
			frame4 = browser.find_element_by_xpath('//iframe[@src="/foisweb/view/qry/TQ_OwcmViewRRSubOT.jsp"]')
		except NoSuchElementException:
			time.sleep(1)

	print(6)
	browser.switch_to.frame(frame4)
	yo = None
	while not yo:
		try:
			yo = browser.find_element_by_xpath('//html/body/table/tbody/tr[6]/td[1]/table/tbody/tr[1]/td[2]/div/table/tbody/tr[1]/td[8]')
		except NoSuchElementException:
			time.sleep(1)

	print(7)
	df_RR_pol = df_RR_pol.append({'RR_Num': i, 'AT_PUN_RATE':yo.text}, ignore_index=True)
	print(df_RR_pol)

	printBut = None
	while not printBut:
		try:
			printBut = 	browser.find_element_by_link_text('print')
		except NoSuchElementException:
			time.sleep(1)

	printBut.click()

	time.sleep(10)
	original = 'C:\\Users\\AZ\\Desktop\\RR-pdfs\\TQ_OwcmViewRRPrntOT.jsp.pdf'
	output = 'C:\\Users\\AZ\\Desktop\\RR-pdfs\\RR-'+str(i)+'--'+str(rrDate)+'.pdf'

	try:
		os.rename(original, output)
	except WindowsError:
		os.remove(output)
		os.rename(original, output)

	#os.rename('C:\\Users\\AZ\\Desktop\\RR-pdfs\\TQ_OwcmViewRRPrntOT.jsp.pdf', 'C:\\Users\\AZ\\Desktop\\RR-pdfs\\RR-'+str(i)+'.pdf')
	print(8)
	browser.switch_to.default_content()
	frm = None
	while not frm:
		try:
			frm = browser.find_element_by_xpath('//iframe[@name="frmInpt"]')
		except NoSuchElementException:
			time.sleep(1)
	browser.switch_to.frame(frm)

	frame3 = None
	while not frame3:
		try:
			frame3 = browser.find_element_by_xpath('//iframe[@name="frmDtls"]')
		except NoSuchElementException:
			time.sleep(1)

	browser.switch_to.frame(frame3)

	print(9)
	backBut = None
	while not backBut:
		try:
			backBut = 	browser.find_element_by_link_text('Back')
		except NoSuchElementException:
			time.sleep(1)

	backBut.click()

	print(10)
	writer = ExcelWriter('RR-POL.xls')
	df_RR_pol.to_excel(writer, 'Sheet1')
	writer.save()

	j = j + 1;
	print 'Number of RR downloaded = ', j, '/', listlen

print(df_RR_pol)

'''
list1 = list(df3)
list1 = list1[:25] + list1[-1:] + list1[25:-2]
#print(list1)
df3 = df3[list1]
#print(df3)
'''

import pun_rate_merger

browser.quit()
