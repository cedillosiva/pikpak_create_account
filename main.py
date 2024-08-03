from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.support import expected_conditions as EC
import time
from GmailBox import GmailBox
import json
import pyautogui
import os

def wait_for_element(driver, xpath, waitS = 60):
    for i in range(waitS):
        if len(driver.find_elements(By.XPATH, xpath)) > 0:
            break
        time.sleep(1)

Gmail = GmailBox()
New_Gmail = Gmail.new_email()
email = New_Gmail.email
print(email)
password = 'Test@1234'
magnet = 'magnet:?xt=urn:btih:3928fc19fef800d3b164eabbfe3ef9aac4432c5b'

options = ChromeOptions()
print("Extension dir :", f"{os.getcwd()}\\captcha_solver")
options.add_argument(f"--load-extension={os.getcwd()}\\captcha_solver")
driver = webdriver.Chrome(options=options)
driver.minimize_window()
driver.maximize_window()
print("Focus to window")
driver.get("https://mypikpak.com/drive/login")
try:
    driver.find_element(By.XPATH, "//span[@class='other-login-methods']").click()
except:
    pass

driver.find_element(By.XPATH, "//div[@class='icon-email']").click()
driver.find_element(By.XPATH, "//span[@class='login-header-subtitle link']").click()
driver.find_element(By.XPATH, "(//input)[1]").send_keys(email)
driver.find_element(By.XPATH, "//div[@class='count-down-button']").click()
print("pyautogui sending keys for extension")
time.sleep(1)
pyautogui.hotkey('ctrl','shift','Y')
time.sleep(1)
pyautogui.hotkey('esc')
print("Waiting for capthca to do its job")
while True:
    if len(driver.find_elements(By.XPATH, "//iframe"))==0:
        break
time.sleep(5)
# Start checking the inbox
inbox = Gmail.inbox(email)
# If there are messages in the inbox, print them
if inbox:
    for message in inbox:
        code = str(message).split("verification Code：")[2][:6]
# If no messages were received, print a message
else:
    print(f' [!] No messages were received.')

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

wait_for_element(driver,"(//button[@class='el-button el-button--primary button'])[1]", 300)
driver.find_element(By.XPATH, "(//button[@class='el-button el-button--primary button'])[1]").click()
driver.find_element(By.XPATH, "//textarea").send_keys(magnet)
els = driver.find_elements(By.XPATH, "//button[@class='el-button el-button--primary']")
els[-1].click()
time.sleep(1)
print(email, code)
with open('data.json', 'w') as f:
    json.dump({'email' : email, 'password' : password, 'code' : 'code'}, f)
time.sleep(100000)