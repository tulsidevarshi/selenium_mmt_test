import os
from selenium import webdriver

get_path = os.getcwd()
relative_path = "chromedriver-mac-arm64"
chromeDriver = "chromedriver"

path_for_chrome_driver = os.path.join(get_path, relative_path, chromeDriver)
# print(path_for_chrome_driver)

base_url = "https://www.makemytrip.com/"

driver = webdriver.Chrome(path_for_chrome_driver)
driver.get(base_url)

driver.close()
