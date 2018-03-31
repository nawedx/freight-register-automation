from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import time
import os
import pandas as pd
from pandas import ExcelWriter
pd.set_option('display.max_columns', 100)

'''
folderName = os.path.join(os.path.expanduser("~/"), "freight-register-automation")
fileName = 'RR-'+st
profile = webdriver.FirefoxProfile()
profile.set_preference('print.always_print_silent', True)
profile.set_preference("print_printer", "PDF")
profile.set_preference('print.print_to_file', True)
#profile.set_preference('print.print_to_filename', fileName)
'''

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
rrList = df['RR_NUMBER'].values
listlen = len(rrList)

df_RR_pol = pd.DataFrame(columns=['RR_Num', 'POL'])
j = 0
for i in rrList:
	j = j + 1;
	print("%.2f" % (j*100.0/listlen))
	browser.switch_to.default_content()
	frm = browser.find_element_by_xpath('//iframe[@name="frmInpt"]')
	browser.switch_to.frame(frm)

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
	
	link = None
	while not link:
		try:
			link = browser.find_element_by_link_text(str(i))
		except NoSuchElementException:
			time.sleep(1)
	link.click()

	frame3 = None
	while not frame3:
		try:
			frame3 = browser.find_element_by_xpath('//iframe[@name="frmDtls"]')
		except NoSuchElementException:
			time.sleep(1)

	browser.switch_to.frame(frame3)

	frame4 = None
	while not frame4:
		try:
			frame4 = browser.find_element_by_xpath('//iframe[@src="/foisweb/view/qry/TQ_OwcmViewRRSubOT.jsp"]')
		except NoSuchElementException:
			time.sleep(1)

	browser.switch_to.frame(frame4)

	yo = None
	while not yo:
		try:
			yo = browser.find_element_by_xpath('//html/body/table/tbody/tr[6]/td[1]/table/tbody/tr[1]/td[2]/div/table/tbody/tr[1]/td[8]')
		except NoSuchElementException:
			time.sleep(1)

	df_RR_pol = df_RR_pol.append({'RR_Num': i, 'POL':yo.text}, ignore_index=True)

	#browser.find_element_by_link_text('print').click()

	browser.switch_to.default_content()
	frm = browser.find_element_by_xpath('//iframe[@name="frmInpt"]')
	browser.switch_to.frame(frm)
	frm = browser.find_element_by_xpath('//iframe[@name="frmDtls"]')
	browser.switch_to.frame(frm)
	back = browser.find_element_by_link_text('Back')
	back.click()

print(df_RR_pol)
writer = ExcelWriter('RR-POL.xls')
df_RR_POL.to_excel(writer,'Sheet1')
writer.save()
