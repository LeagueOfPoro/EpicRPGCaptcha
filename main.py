from tabnanny import check
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import chromedriver_autoinstaller
import time
from pprint import pprint
import requests
import captcha
import random

WORK_CMD="rpg chop"
HUNT_CMD="rpg hunt"
DATA_DIR="C:/Users/PC/AppData/Local/Google/Chrome/User Data"
PROFILE_DIR="Profile 1"
DISCORD_CHANNEL="https://discord.com/channels/493694955184926720/931492715865397073"


def sendText(driver: webdriver, text):
    inputArea = driver.find_element(by=By.CSS_SELECTOR, value="div[class^=textArea]")
    innerInputArea = driver.find_element(by=By.CSS_SELECTOR, value="div[class^=textArea] div div[role^=textbox]")
    inputArea.click()
    innerInputArea.send_keys(text)
    innerInputArea.send_keys(Keys.RETURN)

def checkMessages(driver, text):
    messages = driver.find_elements(by=By.CSS_SELECTOR, value="div[id^=message-content]")
    if len(messages) >= 10:
        lastMessages = messages[-10:]
        for msg in lastMessages:
            if text in msg.text:
                return True
    return False

def isInJail(driver):
    return checkMessages(driver, "jail")

def backToWork(driver):
    return checkMessages(driver, "I solemnly swear that I am up to no good")

def killBot(driver):
    return checkMessages(driver, "Mischief managed")

def shouldBeHealing(driver):
    if checkMessages(driver, "Start healing"):
        return True
    elif checkMessages(driver, "Stop healing"):
        return False
    return None

def changeWorkCommand(driver):
    messages = driver.find_elements(by=By.CSS_SELECTOR, value="div[id^=message-content]")
    if len(messages) >= 10:
        lastMessages = messages[-10:]
        for msg in lastMessages:
            if "chwrk " in msg.text:
                return msg.text[6:]
    return None

def checkCaptcha(driver):
    messages = driver.find_elements(by=By.CSS_SELECTOR, value="div[class^=message]")
    if len(messages) >= 5:
        lastMessages = messages[-5:]
        for msg in lastMessages:
            try:
                content = msg.find_element(by=By.CSS_SELECTOR, value="div[id^=message-content]")
                if "We have to check" in content.text:
                    image = msg.find_element(by=By.CSS_SELECTOR, value="div[class^=imageWrapper] a")
                    try:
                        resImg = requests.get(image.get_attribute("href"))
                        with open("captcha.png", "wb") as f:
                            f.write(resImg.content)
                        return True
                    except Exception as e:
                        print(e)
            except Exception as e:
                pass
    return False

def heal(driver):
    sendCommand(driver, "rpg heal")

def sendCommand(driver, cmd):
    sendText(driver, cmd)
    time.sleep(3)
    if checkCaptcha(driver):
        for answer in captcha.solveCaptcha():
            sendText(driver, answer)

###################################################
chromedriver_autoinstaller.install()

options = webdriver.ChromeOptions() 
options.add_argument(f"user-data-dir={DATA_DIR}")
options.add_argument(f'--profile-directory={PROFILE_DIR}')
driver = webdriver.Chrome(options=options)
driver.get(DISCORD_CHANNEL)
time.sleep(10)

lastRunWork = time.time()
inJail = False
isHealing = False

while not killBot(driver):
    while not isInJail(driver) and not inJail:
        sendCommand(driver, HUNT_CMD)
        isHealing = shouldBeHealing(driver)
        if isHealing:
            heal(driver)
        time.sleep(2 + random.uniform(0,2))  

        work = changeWorkCommand(driver)
        if work:
            WORK_CMD = work
            sendCommand(driver, f"Changing work command to {WORK_CMD}")
        if time.time() - lastRunWork > 300:
            sendCommand(driver, WORK_CMD)
            lastRunWork = time.time()

        time.sleep(56 + random.uniform(0,5))


    inJail = True
    # sendCommand(driver, "Wake me up when the sentence ends")
    time.sleep(20)
    if backToWork(driver):
        inJail = False
        sendCommand(driver, "Messrs. Moony, Wormtail, Padfoot, and Prongs, Purveyors of Aids to Magical Mischief-Makers are proud to present Epic RPG Bot Bot.")
        
sendCommand(driver, "THE END")
driver.quit()



