# -*- coding: utf-8 -*-
import time
from selenium import webdriver
import os

provinceDict = {'安徽':'928', '澳门':'934', '北京':'911', '重庆':'904', '福建':'909', '广东':'913', '甘肃':'925', '广西':'912', '贵州':'902', 
'河北':'920', '黑龙江':'921', '河南':'927', '湖南':'908', '湖北':'906', '海南':'930', '吉林':'922', '江苏':'916', '江西':'903', '辽宁':'907', 
'内蒙古':'905', '宁夏':'919', '青海':'918', '上海':'910', '四川':'914', '山东':'901', '山西':'929', '陕西':'924', '天津':'923', '台湾':'931', 
'西藏':'932', '香港':'933', '新疆':'926', '云南':'915', '浙江':'917'}

def openBrowser():
	global browser

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
		fileaccount = open("./baidu/account.txt", encoding='UTF-8')
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
	time.sleep(3)

def getAddressCode():
	fd = open("city_list.txt","w")
	openBrowser()
	browser.execute_script('window.open("http://index.baidu.com");')
	handles = browser.window_handles
	browser.switch_to_window(handles[-1])
	time.sleep(5)

	# input the keyword
	browser.find_element_by_class_name("search-input").clear()
	browser.find_element_by_class_name("search-input").send_keys("600660")
	browser.find_element_by_class_name("search-input-cancle").click()
	time.sleep(5) #wait for response
	browser.maximize_window()
	time.sleep(2)

	for key in provinceDict:
		browser.find_element_by_id("compOtharea").click()
		time.sleep(1)
		browser.find_element_by_xpath("//span[@class='selectA provA slided']//div//a[@href='#" + provinceDict[key] + "']").click()
		time.sleep(1)
		cities = browser.find_elements_by_xpath("//span[@class='selectA cityA slided']//div//dd//a")
		for city in cities:
			cityNo = city.get_attribute('href')
			fd.write(provinceDict[key] + ' ' + cityNo.split('#')[-1] + ' ' + city.text + '\n')
		time.sleep(1)
	fd.close()

	browser.quit()

if __name__ == '__main__':
	getAddressCode()








