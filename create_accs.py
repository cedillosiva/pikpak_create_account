from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import time
from tempmail import EMail
import pyautogui
import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

def wait_for_element(driver, xpath, waitS = 60):
    for i in range(waitS):
        if len(driver.find_elements(By.XPATH, xpath)) > 0:
            break
        time.sleep(1)

def initialize_driver(url = "https://mypikpak.com/drive/login"):
    options = ChromeOptions()
    #print("Extension dir :", f"{os.getcwd()}\\captcha_solver")
    options.add_argument(f"--load-extension={os.getcwd()}\\captcha_solver")
    driver = webdriver.Chrome(options=options)
    driver.minimize_window()
    driver.maximize_window()
    driver.get(url)
    driver.find_element(By.XPATH, "//button[@class='el-button el-button--primary']").click()
    #print("pyautogui sending keys for extension")
    time.sleep(2)
    pyautogui.hotkey('ctrl','shift','Y')
    time.sleep(1)
    pyautogui.hotkey('esc')
    return driver

def sigup(driver, email):
    wait_for_element(driver,"//span[@class='other-login-methods']", 3)
    try:
        driver.find_element(By.XPATH, "//span[@class='other-login-methods']").click()
    except:
        pass

    driver.find_element(By.XPATH, "//div[@class='icon-email']").click()
    driver.find_element(By.XPATH, "//span[@class='login-header-subtitle link']").click()
    try:
        driver.find_element(By.XPATH, "//div[@class='icon-clearable']").click()
    except:
        pass
    driver.find_element(By.XPATH, "(//input)[1]").send_keys(email)
    driver.find_element(By.XPATH, "//div[@class='count-down-button']").click()

def wait_for_captcha(driver):
    while True:
        if len(driver.find_elements(By.XPATH, "//iframe"))==0:
            break

def create_account(driver):
    url = "https://mypikpak.com/drive/login"
    password = 'Test@1234'
    magnet = 'magnet:?xt=urn:btih:11AE1401C79975F7A9195018EB67CD754344CD27'
    email1Sec = EMail()
    email = email1Sec.address
    sigup(driver, email)
    time.sleep(5)
    wait_for_captcha(driver)
    time.sleep(5)
    
    msg = email1Sec.wait_for_message()
    code = msg.body.split("<h2>")[2].split("</h2>")[0]

    driver.switch_to.default_content()
    driver.find_element(By.XPATH, "(//input)[2]").send_keys(code)
    driver.find_element(By.XPATH, "(//input)[3]").send_keys(password)
    driver.find_element(By.XPATH, "(//input)[4]").send_keys(password)

    driver.find_element(By.XPATH, "//button[@class='pp-button']").click()
    wait_for_element(driver, "//span[contains(text(),'Cloud Download')]")
    signOut(driver)
    write_email(email)
    print(email)

def signOut(driver):
    element_to_hover_over = driver.find_element(By.XPATH, "(//div[@class = 'placeholder'])[1]")
    hover = ActionChains(driver).move_to_element(element_to_hover_over)
    hover.perform()
    driver.find_element(By.XPATH, "//a[contains(text(),'Sign out')]").click()
    driver.find_element(By.XPATH, "(//button[@class='el-button el-button--primary'])[2]").click()

def write_email(email):
    global postgres_engine
    df = pd.DataFrame([{"email" : email}])
    df.to_sql(name='email', con=postgres_engine, if_exists='append', index=False)


postgres_engine = create_engine("postgresql://avnadmin:AVNS_YsXFiJNy-_YpeUoyZQM@stremio-stremio.l.aivencloud.com:22806/defaultdb?sslmode=require", poolclass=NullPool)

driver = initialize_driver()
for i in range(20):
    try:
        create_account(driver)
    except:
        continue