from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

desired_cap = {
'browserName': 'iPhone',
'device': 'iPhone 7',
'realMobile': 'true',
'os_version': '10.3'
}


driver = webdriver.Chrome()
driver.get("localhost:5000/")
assert "Got Game?" in driver.title
# elem = driver.find_element_by_name("q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# 
print 'The /welcome route loaded successfully for the user'
driver.close()
# driver = webdriver.Remote(
   # command_executor='http://USERNAME:ACCESS_KEY@hub.browserstack.com:80/wd/hub',
   # desired_capabilities=desired_cap)

# driver.get("http://www.google.com")
# if not "Google" in driver.title:
#     raise Exception("Unable to load google page!")
# elem = driver.find_element_by_name("q")
# elem.send_keys("BrowserStack")
# elem.submit()
# print driver.title
# driver.quit()