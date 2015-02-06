from browsermobproxy import Server
server = Server("path/to/browsermob-proxy")
server.start()
proxy = server.create_proxy

from selenium import webdriver
profile  = webdriver.FirefoxProfile()
profile.set_proxy(proxy.selenium_proxy())
driver = webdriver.Firefox(firefox_profile=profile)

proxy.new_har("google")
driver.get("http://www.google.co.uk")
proxy.har # returns a HAR JSON blob

proxy.stop()
#driver.quit()
