import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
base_url = "https://www.makemytrip.com/"

def wait_for_element(identifier=By.CLASS_NAME, value="primaryBtn", clickable=False, wait_time=120)->int:
    try:
        element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((By.CLASS_NAME, value))
    )
        print("Found: "+value)
        if clickable:
            element.click()
        return 0
    except:
        return 1

def click_on_search():
    wait_for_element(By.CLASS_NAME, "primaryBtn", True, wait_time=60)

def is_pop_up():
    """
    <span class="bgProperties  overlayCrossIcon icon20" style="background-image: url(&quot;//jsak.mmtcdn.com/flights/assets/media/cross-icon.8b0f8487.png&quot;);"></span>
    """
    print("Func called")
    wait_for_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/div[2]/div/div/div[3]/button", True, wait_time=60)
    print("Func Exit")

driver = webdriver.Chrome()
driver.get(base_url)
print(driver.title)
# time.sleep(20)
try:
    click_on_search()
    time.sleep(10)
    is_pop_up()
    time.sleep(60)

except:
    print("Error Occured")
finally:
    driver.quit()

