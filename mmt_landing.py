import os
import time
import requests
from selenium import webdriver

base_url = "https://www.makemytrip.com/"

driver = webdriver.Chrome()
driver.get(base_url)
time.sleep(20)
driver.quit()
