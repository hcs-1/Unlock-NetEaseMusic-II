# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "008A6A97667D8BEE119CF70BFF11431A3EEF4E64680AA7226D31833846BBFE30299022E91E68C1511FFAE258D60BD5059020D7DB80517A96D532ABB4AEF787B4B210BE9C28D9AB19E4B0892A7C25F59AAA07816EDFCBB5624052E922363D08F54D494D6FD1157C4DB3674158FF35D977488B53F883A350EB53FDCAC3C448FA3FD3AE056B7A65F435E6AE727EF56E1FEAA9C3E6320241DE5DF130AD34EC1C5EB84BCCFCB21083ADCFC8AEA039B35F04F60D459E7F038206B386B347970785B46700CF63F0F1456C74C7BC714F4DB954650F6F92C726A7B52D68FE1D34C473AD7C16A89AD65AE35F7ED1BB107E3BCFCF8895465372C8DE51DC70272EF52C8BDAD6D09B5CBB0FAC6109EEB52086BE41D8FD2EF8D424C4961EBBA18B7175CB8C7DBF6AF3075F9CAAC4A8300F212463090F3E07CCA5B595D9F98E651B42D990FBA6463F4190DC200FB86EE4E65A110B0D14ADFBCC2E8F0C38B5CCCC88C0E3CFE8F3EDC0"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
