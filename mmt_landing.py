import re
import os
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeServ
from webdriver_manager.chrome import ChromeDriverManager

"""
In Future the script will be converted to POM arrangement
If script does not work. comment out the headless command -> few things is
In case of any error a screenshot of the error page will be taken for your display
"""

base_url = "https://www.makemytrip.com/"

chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless=new")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64;  x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation","enable-logging"])


driver = webdriver.Chrome(options=chrome_options, service=ChromeServ(ChromeDriverManager().install()))
driver.maximize_window()
driver.get(base_url)
title_val = driver.title
print(title_val)
# print(driver)

class TypeMismatch(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def wait_for_element(identifier=By.CLASS_NAME, value="primaryBtn", clickable=[False, False], wait_time=120)->int:
    try:
        while True:
            driver.execute_script('scrollBy(0,250)')
            time.sleep(0.5)
            driver.execute_script('scrollBy(0,500)')
            time.sleep(0.25)
            driver.execute_script('scrollBy(0, 200)')
            time.sleep(0.75)
            driver.execute_script('scrollBy(0, -950)')
            break
        # driver.execute_script('document.getElementsByTagName("html")[0].style.scrollBehavior = "auto"')
        element = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((identifier, value))
    )
        print("Found: "+value)
        element.find_element(by=identifier, value=value)
        time.sleep(4)
        if clickable[0]:
            element.click()
        if clickable[1]:
            wait = WebDriverWait(driver, wait_time)
            div_tags = wait.until(EC.presence_of_all_elements_located((identifier, value)))
            values = []
            for div_tag in div_tags:
                values.append([val.strip() for val in re.findall("₹\s+(\d*\,*\d*)", div_tag.text.strip())][0])
            return values

        return 0
    except:
        print(f"Error. Not Found: {value}")
        cwd = os.getcwd()
        curr_tm = "error"+str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S"))+".png"
        file_screen = os.path.join(cwd,"log", curr_tm)
        driver.save_screenshot(file_screen)
        return 0

def click_on_search():
    a = wait_for_element(
        identifier=By.XPATH, 
        value='//*[@id="top-banner"]/div[2]/div/div/div/div[2]/p/a', clickable=[True, False], wait_time=60)
    return a

def is_pop_up():
    """
    <span class="bgProperties  overlayCrossIcon icon20" style="background-image: url(&quot;//jsak.mmtcdn.com/flights/assets/media/cross-icon.8b0f8487.png&quot;);"></span>
    """
    # print("Func called")
    return wait_for_element(
        identifier=By.XPATH, 
        value='//*[@id="root"]/div/div[2]/div[2]/div[2]/div/span', 
        clickable=[True, False], 
        wait_time=60)

def get_all_prices():
    return wait_for_element(
        By.CSS_SELECTOR, 
        '.blackText.fontSize18.blackFont.white-space-no-wrap.clusterViewPrice', 
        [False, True], 
        wait_time=60)

def is_sorted_list(lsA):
    for i in range(1, len(lsA)):
        if lsA[i-1] > lsA[i]:
            print("List is not sorted here: {}".format(str(lsA[i-1:i])))
            return False
    return True

def main():
    try:
        if click_on_search() == 1:
            return
        if is_pop_up() == 1:
            return
        time.sleep(5)
        out = get_all_prices()
        if type(out) is not list:
            raise TypeMismatch("Expected list got integer")
        out = [int(re.sub(',','',a.strip())) for a in out if a.strip()!=""]
        if is_sorted_list(out):
            print("Matched")
        else:
            print("Not sorted list")
    except:
        print("Error Occured")

if __name__ == '__main__':
    main()
    driver.quit()
