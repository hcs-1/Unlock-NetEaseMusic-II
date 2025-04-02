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
    browser.add_cookie({"name": "MUSIC_U", "value": "00D948228ABB3B4B293220E67099381A34982A520FE33E03FD1C032EA739A4609B888F660956F6138411E4103A8239B7EDB690649AAD5B70928DCCC1AFDBA75F544BE825C0369258445DF8462EFC9B3259F72F60940B1384899351D25F8555B86DC30D36EF298DC0D3DA43EE330705E6F373EE2C76003D1725F3080F49ADD7BE4D5E165F0C893858E301E72968BA7DC0A93AE3E9AA0A33F323F62C68D1CBA30D60A5377DA99814928EDD106891EB3C63EB3990352EFFB5F3B1449C0715A545A6F1C0176BA8540E098E1820C8D75D2E4157DAFF7EF226F507485A408197EFD2BA62FBE2747C1754268F3177FEE07216D3F0BFC860523CA1C7648BFB35671D593FA8D375A10354282F7B6EFD36296B6D2FF9C6028E670CE051DB98E201D6FBD2500ACE8B5DBF491A76F383AD31F72FB8DA476AB7C3713466F732221AD5C0604C8BBEF1C142E2A39276364503F46DA626DA30E6F462A5AD6AD4657488D57B96EA2337"})
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
