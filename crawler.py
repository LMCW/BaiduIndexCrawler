import time
import selenium
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import pytesseract
import os

def openbrowser():
    global browser

    # https://passport.baidu.com/v2/?login
    url = "https://passport.baidu.com/v2/?login&tpl=mn&u=http%3A%2F%2Fwww.baidu.com%2F"
    # Firefox()
    # Chrome()
    browser = webdriver.Chrome()
    browser.get(url)

    browser.find_element_by_id("TANGRAM__PSP_3__footerULoginBtn").click()
    browser.find_element_by_id("TANGRAM__PSP_3__userName").clear()
    browser.find_element_by_id("TANGRAM__PSP_3__password").clear()
    
    account = []
    try:
        fileaccount = open("../baidu/account.txt", encoding='UTF-8')
        accounts = fileaccount.readlines()
        for acc in accounts:
            account.append(acc.strip())
        fileaccount.close()
    except Exception as err:
        print(err)
        exit()
    username = account[0]
    password = account[1]
    browser.find_element_by_id("TANGRAM__PSP_3__userName").send_keys(username)
    time.sleep(1)
    browser.find_element_by_id("TANGRAM__PSP_3__password").send_keys(password)

    # id="TANGRAM__PSP_3__submit"
    browser.find_element_by_id("TANGRAM__PSP_3__submit").click()
    print("ready for new site...")

    print("Verifying")
    select = input("Verified or not(y/n)：")
    while 1:
        if select == "y" or select == "Y":
           print("login success...")
           break
    time.sleep(1)

