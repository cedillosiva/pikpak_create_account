from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
import time
from GmailBox import GmailBox
import json
import pyautogui
import os
import requests

def wait_for_element(driver, xpath, waitS = 1000):
    for i in range(waitS):
        if len(driver.find_elements(By.XPATH, xpath)) > 0:
            break
        time.sleep(1)

def get_email():
    New_Gmail = Gmail.new_email()
    email = New_Gmail.email
    print(email)
    return email

def initialize_driver(url = "https://mypikpak.com/drive/login"):
    options = ChromeOptions()
    print("Extension dir :", f"{os.getcwd()}\\captcha_solver")
    options.add_argument(f"--load-extension={os.getcwd()}\\captcha_solver")
    driver = webdriver.Chrome(options=options)
    driver.minimize_window()
    driver.maximize_window()
    print("Focus to window")
    driver.get(url)
    driver.find_element(By.XPATH, "//button[@class='el-button el-button--primary']").click()
    print("pyautogui sending keys for extension")
    time.sleep(2)
    pyautogui.hotkey('ctrl','shift','Y')
    time.sleep(1)
    pyautogui.hotkey('esc')
    return driver

def sigup(driver):
    try:
        driver.find_element(By.XPATH, "//span[@class='other-login-methods']").click()
    except:
        pass

    driver.find_element(By.XPATH, "//div[@class='icon-email']").click()
    driver.find_element(By.XPATH, "//span[@class='login-header-subtitle link']").click()
    driver.find_element(By.XPATH, "(//input)[1]").send_keys(email)
    driver.find_element(By.XPATH, "//div[@class='count-down-button']").click()
def wait_for_captcha(driver):
    while True:
        if len(driver.find_elements(By.XPATH, "//iframe"))==0:
            break
    print("Frame wait complete")

url = "https://mypikpak.com/drive/login"
password = 'Test@1234'
magnet = 'magnet:?xt=urn:btih:11AE1401C79975F7A9195018EB67CD754344CD27'

Gmail = GmailBox()
email = get_email()
driver = initialize_driver()
sigup(driver)
print("Waiting for capthca to do its job")
time.sleep(5)
wait_for_captcha(driver)
time.sleep(5)
# Start checking the inbox
inbox = Gmail.inbox(email)

while True:
    # If there are messages in the inbox, print them
    if inbox:
        for message in inbox:
            code = str(message).split("verification Code：")[2][:6]
            
        break
    # If no messages were received, print a message
    else:
        print("No Message received with code from PikPak : Retrying!!!")
        try:
            driver.get(url)
            sigup(driver)
            time.sleep(5)
            wait_for_captcha(driver)
        except:
            time.sleep(10)
    time.sleep(10)
print("Gmail wait complete")

driver.switch_to.default_content()
driver.find_element(By.XPATH, "(//input)[2]").send_keys(code)
driver.find_element(By.XPATH, "(//input)[3]").send_keys(password)
driver.find_element(By.XPATH, "(//input)[4]").send_keys(password)

driver.find_element(By.XPATH, "//button[@class='pp-button']").click()

wait_for_element(driver, "//a[contains(text(),'I Know')]")
driver.find_element(By.XPATH, "//a[contains(text(),'I Know')]").click()
time.sleep(1)
wait_for_element(driver, "//a[contains(text(),'I Know')]")
driver.find_element(By.XPATH, "//a[contains(text(),'I Know')]").click()

wait_for_element(driver,"(//button[@class='el-button el-button--primary button'])[1]")
driver.find_element(By.XPATH, "(//button[@class='el-button el-button--primary button'])[1]").click()
driver.find_element(By.XPATH, "//textarea").send_keys(magnet)
els = driver.find_elements(By.XPATH, "//button[@class='el-button el-button--primary']")
els[-1].click()
print(email, code)

#with open('data.json', 'w') as f:
#    json.dump({'email' : email, 'password' : password, 'code' : 'code'}, f)
#host = "http://127.0.0.1:5000"
host = "https://adverse-patrizia-piyushstremio-b2b90014.koyeb.app"
requests.get(f"{host}/update/{email}")
time.sleep(5)
print("Print got 1 day premium")
wait_for_element(driver, "//*[@class=\"el-dialog__body\"]/div[@class='button']")
driver.find_element(By.XPATH, "//*[@class=\"el-dialog__body\"]/div[@class='button']").click()
wait_for_element(driver, "//*[contains(text(), 'Do not display this pop-up')]", 5)
try:
    driver.find_element(By.XPATH, "//*[contains(text(), 'Do not display this pop-up')]").click()
except:
    pass
print("Trying addon 1")
wait_for_element(driver, "(//button[@class='el-button el-button--primary button'])[1]")
driver.find_element(By.XPATH, "(//button[@class='el-button el-button--primary button'])[1]").click()
time.sleep(5)
print("Trying addon 2")
driver.switch_to.window(driver.window_handles[-1])
wait_for_element(driver, "//a[@class='chrome']")
time.sleep(2)
driver.find_element(By.XPATH,"//a[@class='chrome']").click()
time.sleep(5)
driver.switch_to.window(driver.window_handles[2])
driver.find_element(By.XPATH,"//span[contains(text(),'Add to Chrome')]").click()
time.sleep(5)
pyautogui.hotkey('tab')
pyautogui.hotkey('enter')
print("Completed creating task : emal : ", email)
time.sleep(20)
driver.quit()