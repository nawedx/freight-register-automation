#Script to Download Invoice Details from RMS Queries of FOIS
#Written by Nawed Imroze (nawedx)

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from datetime import date, timedelta
import os, time

downloadPath = '/home/nawedx/Downloads/'

fromdate = str((date.today()-timedelta(3)).day)
todate = str((date.today()-timedelta(1)).day)

currentMonth = str(date.today().month)
fromMonth = str((date.today()-timedelta(3)).month)
toMonth = str((date.today()-timedelta(1)).month)
print(currentMonth, fromMonth, toMonth, fromdate, todate)

options = webdriver.FirefoxProfile();
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel");

def getElementByXpath(xpth, ele):
	browserElement = None
	while not browserElement:
		try:
			print(ele)
			browserElement = browser.find_element_by_xpath(xpth)
			return browserElement
		except NoSuchElementException:
			time.sleep(1)

def getElementByID(iD, ele):
	browserElement = None
	while not browserElement:
		try:
			print(ele)
			browserElement = browser.find_element_by_id(iD)
			return browserElement
		except NoSuchElementException:
			time.sleep(1)


#Initializes the webdriver and starts the browser
browser = webdriver.Firefox(options)
browser.get("http://fois.indianrail.gov.in/rmsdqweb/view/GG_LoginMainPrtlRQ.jsp")
#browser.maximize_window()

#Checks until the Submit button has been loaded
#I have made the assumption that if submit button is loaded all other fields before it has alse been loaded.
login_attempt = getElementByXpath('//*[@id="Submit"]', 'Login Submit Button')

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
invc = getElementByXpath('//td[. = "Operations Control"]', 'Operations Control')
invc.click()
ftdetails = browser.find_element_by_xpath('//td[. = "Miscelleneous"]')
ftdetails.click()
ftdetails = browser.find_element_by_xpath('//td[. = "Invoice Details"]')
ftdetails.click()

#Switches to appropriate frame.
frame2 = getElementByXpath('//iframe[@name="frmInpt"]', 'Changing iframe to select dates')
browser.switch_to.frame(frame2)

fromDateImage = getElementByXpath('/html/body/form[1]/table/tbody/tr[2]/td/fieldset/img[1]', 'From Date Picker')
fromDateImage.click()

if fromMonth != currentMonth:
	fromDate = getElementByXpath('//td[. = "<"]', 'Previous Month for from date')
	fromDate.click()

fromDate = getElementByXpath('//td[. = "'+fromdate+'"]', 'From Date')
fromDate.click()

toDateImage = getElementByXpath('/html/body/form[1]/table/tbody/tr[2]/td/fieldset/img[2]', 'To Date Picker')
toDateImage.click()

if toMonth != currentMonth:
	toDate = getElementByXpath('//td[. = "<"]', 'Previous Month for to date')
	toDate.click()

toDate = getElementByXpath('//td[. = "'+todate+'"]', 'To Date')
toDate.click()

submitButton = getElementByID('Submit', 'Submit on invoice details date page')
submitButton.click()
time.sleep(3)

browser.switch_to.default_content()
frm = browser.find_element_by_xpath('//iframe[@name="frmInpt"]')
browser.switch_to.frame(frm)
time.sleep(1)

ts = time.time()
currentTimeStamp = datetime.fromtimestamp(ts).strftime('%d-%m-%Y--%H-%M-%S')

filename = 'InvcDtls'
newFileName = filename+str(currentTimeStamp)+'.xls'
if os.path.exists(downloadPath+filename):
    os.rename(downloadPath+filename+'.xls', downloadPath+newFileName+'.xls')
    print('Renamed existing file '+filename+'.xls as'+newFileName+'.xls')

excelDown = browser.find_element_by_link_text('Excel')
excelDown.click()
time.sleep(5)
if os.path.exists('/home/nawedx/Downloads/'+filename+'.xls'):
	print('Invoice details downloaded successfully')

#To confirm that Invoice Details is downloaded
#print('Please check whether InvcDtls.xls is downloaded and press any key : ')

browser.switch_to.default_content()

invc = getElementByXpath('//td[. = "Managerial Set"]', 'Managerial Set')
invc.click()
ftdetails = browser.find_element_by_xpath('//td[. = "Demand"]')
ftdetails.click()
ftdetails = browser.find_element_by_xpath('//td[. = "Area wise Loading/Unloading (Details)"]')
ftdetails.click()

frame2 = getElementByXpath('//iframe[@name="frmInpt"]', 'Frame switch in area wise loading')
browser.switch_to.frame(frame2)
time.sleep(2)

submitButton = getElementByID('Submit', 'Submit on area wise loading date page')
submitButton.click()
time.sleep(3)

showAll = None
while not showAll:
	try:
		showAll = browser.find_element_by_link_text('Show All')
	except NoSuchElementException:
		time.sleep(1)
showAll.click()

total = getElementByXpath('/html/body/center/div[2]/table/tbody/tr[1]/td[1]', 'Getting total as text').text

i=1
while total != 'TOTAL':
	total = browser.find_element_by_xpath('/html/body/center/div[2]/table/tbody/tr['+str(i)+']/td[1]').text
	i = i + 1

rakesLoaded = browser.find_element_by_xpath('/html/body/center/div[2]/table/tbody/tr['+str(i-1)+']/td[8]').text
print('Rakes Loaded : ', rakesLoaded)
with open("rakes_loaded.txt", "w+") as text_file:
	print("{}".format(rakesLoaded), file=text_file)

print("Invoice Details downloaded and rakes loaded extracted")

browser.quit()