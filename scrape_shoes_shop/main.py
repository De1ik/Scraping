from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import pandas as pd
import time

proxy = "149.36.41.202:6969"
# proxy = "194.99.22.21:3128"
# proxy = "95.216.205.32:8118"

options = webdriver.ChromeOptions()
options.add_argument(f'--proxy-server=http://{proxy}')
options.add_argument('--disable-blink-features=AutomationControlled') # Убираем сигнатуру Selenium
# options.add_argument('--headless')  # Запуск в фоновом режиме
# options.add_argument('--disable-gpu')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36')
driver = webdriver.Chrome(options=options)

baseurl = 'https://stockx.com/'


if __name__ == '__main__':

    driver.get(f'https://stockx.com/adidas-yeezy-slide-azure')
    page_title = driver.title
    print(page_title)
    if "Access to this page has been denied" in page_title:
        input("Solve the captcha:")
    else:
        time.sleep(2)

    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "h1"))
        )
        name = driver.find_element(By.TAG_NAME, 'h1').text
        print("Name:", name)
    except:
        print("All Size Button is not here")


    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="trade-box-buy-amount"]'))
        )
        price = driver.find_element(By.CSS_SELECTOR, '[data-testid="trade-box-buy-amount"]').text
        print("Price:", price)
    except:
        print("All Size Button is not here")


    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#menu-button-pdp-size-selector"))
        )
        size_btn = driver.find_element(By.CSS_SELECTOR, "#menu-button-pdp-size-selector")
        actions = ActionChains(driver)
        actions.move_to_element(size_btn).click().perform()
        print("All Size Button clicked")
    except:
        print("All Size Button is not here")


    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="selector-label"]'))
        )
        size_buttons = driver.find_elements(By.CSS_SELECTOR, '[data-testid="selector-label"]')

        print("Find All Size Button")
        print(len(size_buttons))
        all_sizes = []
        for button in size_buttons:
            print("SIZE:", button.text)
            # print("Button:", button)
            all_sizes.append(button.text)
        print(all_sizes)
    except:
        print("Size buttons are not here")




    # try:
    #     WebDriverWait(driver, 15).until(
    #         EC.presence_of_element_located((By.CSS_SELECTOR, '[aria-label="Read More"]'))
    #     )
    #     read_more = driver.find_elements(By.CSS_SELECTOR, '[aria-label="Read More"]')
    #     actions = ActionChains(driver)
    #     actions.move_to_element(read_more).click().perform()
    #
    #     print("Read More CLicked")
    #
    #
    #
    # except:
    #     print("Size buttons are not here")



