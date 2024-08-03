from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome, ChromeOptions, EdgeOptions, FirefoxOptions
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from GmailBox import GmailBox
import json
from selenium.webdriver.common.keys import Keys
import pyautogui

def wait_for_element(driver, xpath, waitS = 10):
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
options.add_argument(r"--load-extension=E:\\Wspace\\pikpak\\captcha_solver")
driver = webdriver.Chrome(options=options)
driver.maximize_window()

driver.get("https://mypikpak.com/drive/login")

try:
    driver.find_element(By.XPATH, "//span[@class='other-login-methods']").click()
except:
    pass

driver.find_element(By.XPATH, "//div[@class='icon-email']").click()
driver.find_element(By.XPATH, "//span[@class='login-header-subtitle link']").click()
driver.find_element(By.XPATH, "(//input)[1]").send_keys(email)
driver.find_element(By.XPATH, "//div[@class='count-down-button']").click()

driver.minimize_window()
driver.maximize_window()
time.sleep(1)
pyautogui.hotkey('ctrl','shift','Y')
time.sleep(1)
pyautogui.hotkey('esc')

while True:
    if len(driver.find_elements(By.XPATH, "//iframe"))==0:
        break

# Start checking the inbox
inbox = Gmail.inbox(email)
# If there are messages in the inbox, print them
if inbox:
    for message in inbox:
        code = str(message).split("verification Code：")[2][:6]
        print(code)
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

wait_for_element(driver,"(//button[@class='el-button el-button--primary button'])[1]")
driver.find_element(By.XPATH, "(//button[@class='el-button el-button--primary button'])[1]").click()
driver.find_element(By.XPATH, "//textarea").send_keys(magnet)
els = driver.find_elements(By.XPATH, "//button[@class='el-button el-button--primary']")
els[-1].click()
time.sleep(1)
driver.quit()