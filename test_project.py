
from selenium import webdriver

firefox_options = webdriver.FirefoxOptions()
firefox_options.set_headless()
browser = webdriver.Firefox(firefox_options=firefox_options)

browser.get("http://localhost:8000")
# browser.get("http://www.baidu.com")

assert 'Django' in browser.title
