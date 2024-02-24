import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
base_url = "https://www.makemytrip.com/"
driver = webdriver.Chrome()
driver.get(base_url)
print(driver.title)

class TypeMismatch(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def wait_for_element(identifier=By.CLASS_NAME, value="primaryBtn", clickable=[False, False], wait_time=120)->int:
    try:
        element = WebDriverWait(driver, wait_time).until(
        EC.element_to_be_clickable((identifier, value))
    )
        print("Found: "+value)
        if clickable[0]:
            element.click()
        if clickable[1]:
            wait = WebDriverWait(driver, wait_time)
            div_tags = wait.until(EC.presence_of_all_elements_located((identifier, value)))
            values = []
            for div_tag in div_tags:
                values.append([val.strip() for val in re.findall("₹\s*(\d*\,*\d+)", div_tag.text.strip())][0])
            return values

        return 0
    except:
        print("Error")
        return 1

def click_on_search():
    a = wait_for_element(
        identifier=By.CLASS_NAME, 
        value="primaryBtn", clickable=[True, False], wait_time=60)
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
    finally:
        driver.quit()

if __name__ == '__main__':
    main()
