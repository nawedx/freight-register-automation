from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
browser = webdriver.Firefox()
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
time.sleep(3)
login_attempt.submit()
time.sleep(10)

newWindow = browser.window_handles[1]
browser.switch_to.window(newWindow)
outward = browser.find_element_by_xpath('//td[. = "Outward"]')
outward.click()
ftdetails = browser.find_element_by_xpath('//td[. = "Freight Details"]')
ftdetails.click()
time.sleep(6)

frame2 = browser.find_element_by_xpath('//iframe[@name="frmInpt"]')
browser.switch_to.frame(frame2)
browser.find_element_by_xpath('.//input[@type="radio" and @value="R"]').click()
browser.find_element_by_id('Submit').click()

