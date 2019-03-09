from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

url ='https://biosciences.stanford.edu/faculty/biosciences-faculty-database/'
driver = webdriver.Firefox()
driver.get(url)

delay = 5 # seconds

try:
#     WebDriverWait(driver, delay).until(EC.presence_of_element_located(driver.find_elements_by_xpath('..//elementid')))
    WebDriverWait(driver, delay)
    print "Page is ready!" 
    for image in driver.find_elements_by_xpath('//*[@id="fn_id9558"]/td[2]'):
        print image.get_attribute('src')
except TimeoutException:
    print "Couldn't load page"