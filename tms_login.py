from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

st = '111001581' 
profile = webdriver.FirefoxProfile()
profile.set_preference('print.always_print_silent', True)
profile.set_preference('print.print_to_file', True)
profile.set_preference('print.print_to_filename', st)

browser = webdriver.Firefox(profile)
browser.get("https://www.fois.indianrail.gov.in/FoisWebsite/jsp/RMS_Zonal.jsp?txtProjName=TZ")
browser.maximize_window()
time.sleep(8)

frame = browser.find_element_by_xpath('//frame[@name="frmApplLgin"]')
browser.switch_to.frame(frame)
username = browser.find_element_by_name('txtUserId')
password = browser.find_element_by_id('txtPassword')
radiobut = browser.find_element_by_id('txtOptnD')
location = browser.find_element_by_id('txtLocation')
username.send_keys('KURACM')
password.send_keys('pps')
radiobut.click()
location.send_keys('KUR')
login_attempt = browser.find_element_by_id('Submit')
login_attempt.submit()
time.sleep(6)
login_attempt.submit()
time.sleep(12)

newWindow = browser.window_handles[1]
browser.switch_to.window(newWindow)
time.sleep(12)
outward = browser.find_element_by_xpath('//td[. = "Outward"]')
outward.click()
ftdetails = browser.find_element_by_xpath('//td[. = "Freight Details"]')
ftdetails.click()
time.sleep(6)

frame2 = browser.find_element_by_xpath('//iframe[@name="frmInpt"]')
browser.switch_to.frame(frame2)
browser.find_element_by_id('Submit').click()

time.sleep(8)
#frame3 = browser.find_element_by_xpath('//iframe[@name="frmInpt"]')
#browser.switch_to.frame(frame3)
link = browser.find_element_by_link_text(st)
link.click()

time.sleep(8)
frame3 = browser.find_element_by_xpath('//iframe[@name="frmDtls"]')
browser.switch_to.frame(frame3)
frame4 = browser.find_element_by_xpath('//iframe[@src="/foisweb/view/qry/TQ_OwcmViewRRSubOT.jsp"]')
browser.switch_to.frame(frame4)
browser.find_element_by_link_text('print').click()
