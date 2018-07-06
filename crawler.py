# -*- coding: utf-8 -*-
import time
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
import pytesseract
import os


provinceDict = {'安徽':'928', '澳门':'934', '北京':'911', '重庆':'904', '福建':'909', '广东':'913', '甘肃':'925', '广西':'912', '贵州':'902', 
'河北':'920', '黑龙江':'921', '河南':'927', '湖南':'908', '湖北':'906', '海南':'930', '吉林':'922', '江苏':'916', '江西':'903', '辽宁':'907', 
'内蒙古':'905', '宁夏':'919', '青海':'918', '上海':'910', '四川':'914', '山东':'901', '山西':'929', '陕西':'924', '天津':'923', '台湾':'931', 
'西藏':'932', '香港':'933', '新疆':'926', '云南':'915', '浙江':'917'}

cityDict = {'合肥':'189','滁州':'182','宿州':'179','安庆':'186','六安':'181','蚌埠':'187','亳州':'391','阜阳':'184','芜湖':'188','宣城':'176', 
'巢湖':'177','铜陵':'173','淮南':'178','马鞍山':'185', '淮北':'183','黄山':'174','池州':'175','澳门':'664','北京':'514','上海':'57','天津':'164',
'台湾':'0','重庆':'11','香港':'663','福州':'50','泉州':'55','厦门':'54','漳州':'56','宁德':'87','三明':'52','莆田':'51','南平':'253','龙岩':'53',
'广州':'95','深圳':'94','佛山':'196','惠州':'199','汕头':'212','东莞':'133','茂名':'203','江门':'198','珠海':'200','湛江':'197','肇庆':'209',
'揭阳':'205','中山':'207','韶关':'201','阳江':'202','云浮':'195','梅州':'211','清远':'208','潮州':'204','汕尾':'213','河源':'210','兰州':'166',
'武威':'283','张掖':'285','嘉峪关':'286','天水':'308','平凉':'307','陇南':'344','庆阳':'281','定西':'282','酒泉':'284','白银':'309','金昌':'343'
,'临夏':'346','南宁':'90','柳州':'89','桂林':'91','百色':'131','河池':'119','梧州':'132','贵港':'93','玉林':'118','北海':'128','钦州':'129',
'来宾':'506','贺州':'92','防城港':'130','贵阳':'2','遵义':'59','六盘水':'4','黔南':'3','毕节':'426','安顺':'424','铜仁':'422','黔东南':'61',
'黔西南':'588','石家庄':'141','唐山':'261','保定':'259','沧州':'148','邯郸':'292','衡水':'143','秦皇岛':'146','廊坊':'147','邢台':'293','承德':'145',
'张家口':'144','哈尔滨':'152','大庆':'153','绥化':'324','齐齐哈尔':'319','佳木斯':'320','牡丹江':'322','黑河':'300','鸡西':'323','伊春':'295',
'鹤岗':'301','双鸭山':'359','七台河':'302','大兴安岭':'297','郑州':'168','洛阳':'378','南阳':'262','新乡':'263','信阳':'373','安阳':'370','平顶山':'266',
'驻马店':'371','焦作':'265','三门峡':'381','周口':'375','许昌':'268','开封':'264','商丘':'376','濮阳':'380','漯河':'379','鹤壁':'374','长沙':'43',
'株洲':'46','衡阳':'45','郴州':'49','常德':'68','岳阳':'44','永州':'269','邵阳':'405','怀化':'67','益阳':'48','湘潭':'47','娄底':'66','张家界':'226',
'湘西':'65','武汉':'28','宜昌':'35','荆州':'31','襄樊':'32','十堰':'36','荆门':'34','黄冈':'33','孝感':'41','黄石':'30','咸宁':'40','恩施':'38','随州':'37',
'鄂州':'39','仙桃':'42','潜江':'74','天门':'73','海口':'239','三亚':'243','儋州':'244','万宁':'241','五指山':'582','琼海':'242','东方':'456','长春':'154',
'吉林':'270','延边':'525','四平':'155','白城':'410','通化':'407','松原':'194','白山':'408','辽源':'191','苏州':'126','南京':'125','无锡':'127','徐州':'161',
'镇江':'169','盐城':'160','南通':'163','常州':'162','扬州':'158','泰州':'159','连云港':'156','宿迁':'172','淮安':'157','南昌':'5','赣州':'10','九江':'6',
'上饶':'9','景德镇':'137','吉安':'115','鹰潭':'7','宜春':'256','抚州':'8','萍乡':'136','新余':'246','沈阳':'150','大连':'29','锦州':'217','鞍山':'215',
'辽阳':'224','丹东':'219','营口':'221','本溪':'220','铁岭':'218','抚顺':'222','朝阳':'216','阜新':'223','葫芦岛':'225','盘锦':'151','呼和浩特':'20',
'呼伦贝尔':'25','赤峰':'21','包头':'13','巴彦淖尔':'15','通辽':'22','鄂尔多斯':'14','乌海':'16','乌兰察布':'331','兴安盟':'333','锡林郭勒盟':'19',
'阿拉善盟':'17','银川':'140','吴忠':'395','石嘴山':'472','固原':'396','中卫':'480','西宁':'139','海西':'608','玉树':'659','海东':'652','成都':'97',
'绵阳':'98','乐山':'107','德阳':'106','泸州':'103','达州':'113','眉山':'291','自贡':'111','南充':'104','内江':'102','宜宾':'96','广安':'108','雅安':'114',
'资阳':'109','广元':'99','遂宁':'100','攀枝花':'112','巴中':'101','甘孜':'417','凉山':'479','阿坝':'457','济南':'1','青岛':'77','潍坊':'80','烟台':'78',
'临沂':'79','淄博':'81','泰安':'353','济宁':'352','聊城':'83','东营':'82','威海':'88','德州':'86','滨州':'76','莱芜':'356','枣庄':'85','菏泽':'84',
'日照':'366','太原':'231','运城':'233','吕梁':'237','晋中':'230','临汾':'232','大同':'227','晋城':'234','长治':'228','忻州':'229','阳泉':'236','朔州':'235',
'西安':'165','渭南':'275','咸阳':'277','宝鸡':'273','汉中':'276','榆林':'278','安康':'272','延安':'401','商洛':'274','铜川':'271','拉萨':'466','那曲':'655',
'林芝':'656','日喀则':'516','乌鲁木齐':'467','石河子':'280','塔城':'563','克拉玛依':'317','阿克苏':'315','哈密':'312','巴音郭楞':'499','阿勒泰':'383',
'昌吉':'311','伊犁哈萨克':'660','吐鲁番':'310','喀什':'384','博尔塔拉':'318','克孜勒苏柯尔克孜':'653','和田':'386','五家渠':'661','昆明':'117','红河':'337',
'玉溪':'123','曲靖':'339','大理':'334','文山':'437','保山':'438','丽江':'342','昭通':'335','思茅':'662','临沧':'350','楚雄':'124','杭州':'138','温州':'149',
'宁波':'289','金华':'135','台州':'287','嘉兴':'304','绍兴':'303','湖州':'305','丽水':'134','衢州':'288','舟山':'306'}

monthDict = {'1':'31', '2':'28', '3':'31', '4':'30', '5':'31', '6':'30', '7':'31', '8':'31', '9':'30','10':'31','11':'30','12':'31'}
monthDay = [31,28,31,30,31,30,31,31,30,31,30,31]


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
    time.sleep(1)


def chooseTime(start, end, year):
	browser.find_elements_by_xpath("//div[@class='box-toolbar']/a")[6].click()
	time.sleep(1)
	browser.find_elements_by_xpath("//span[@class='selectA yearA']")[0].click()
	time.sleep(1)
	browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(year) + "']").click()
	time.sleep(1)
	browser.find_elements_by_xpath("//span[@class='selectA monthA']")[0].click()
	time.sleep(1)
	browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + start + "']").click()
	time.sleep(1)

	browser.find_elements_by_xpath("//span[@class='selectA yearA']")[1].click()
	time.sleep(1)
	browser.find_element_by_xpath("//span[@class='selectA yearA slided']//div//a[@href='#" + str(year) + "']").click()
	time.sleep(1)
	browser.find_elements_by_xpath("//span[@class='selectA monthA']")[1].click()
	time.sleep(1)
	browser.find_element_by_xpath("//span[@class='selectA monthA slided']//ul//li//a[@href='#" + end + "']").click()
	time.sleep(1)
	browser.find_element_by_xpath("//input[@value='确定']").click()
	time.sleep(5)

def getDay(num):
	month = 0
	while 1:
		if num - monthDay[month] < 0:
			break
		else:
			num = num - monthDay[month]
			month = month + 1
	return month + 1, num+1 


def getSample(year, month, day, width, sample, xoyelement):
	size = 0
	x_0 = 0
	y_0 = 0

	if month <= 6:
		if year %4 == 0:
			size = width/ 182.0
		else:
			size = width / 181.0
	else:
		size = width / 184.0

	if sample==0:
		x_0 = 2
	else:
		x_0 = (sample - 0.13) *size

	if sample <= 8:
		y_0 = 30
	else:
		y_0 = 5
	print(size)

	ActionChains(browser).move_to_element_with_offset(xoyelement, x_0, y_0).perform()
	time.sleep(1)
	imgelement = browser.find_element_by_xpath('//div[@id="viewbox"]')
	time.sleep(1)
	locations = imgelement.location

	temp = len(keyword)
	l = 0
	for c in keyword:
		if ord(c) > 127:
			l += 1
		else:
			l += 0.43
	l += 1
	if l > 8:
		l = 8
	rangle = (int(int(locations['x'])) + l * 10 + 34, int(int(locations['y'])) + 28, int(int(locations['x'])) + l * 10 + 38 + 75, int(int(locations['y'])) + 56)

	path = "./baidu/"+str(sample)
	browser.save_screenshot(path+".png")

	img = Image.open(str(path) + ".png")
	r,g,b,a = img.split()
	img = Image.merge("RGB",(r,g,b))
	jpg = img.crop(rangle)
	jpg.save(str(path) + ".jpg")

	jpgzoom = Image.open(str(path) + ".jpg")
	(x, y) = jpgzoom.size
	x_s = 60 * 10
	y_s = 20 * 10
	out = jpgzoom.resize((x_s, y_s), Image.ANTIALIAS)
	out.save(path + 'zoom.jpg', 'png', quality=95)

	image = Image.open(str(path) + "zoom.jpg")
	# code = pytesseract.image_to_string(image)
	fn = str(path)+"zoom.jpg"
	fo = str(path)+"out"
	command = "tesseract "+fn+" "+fo+" --oem 0 --psm 7"
	print(command)
	os.system(command)
	fout = open(fo+".txt","r")
	code = fout.read()
	code = "".join(code.split())
	fout.close()

	if code:
		# 去除一些奇奇怪怪的干扰
		# pytesseract识别图片数字的准确率其实不是说特别高
		code = code.replace("S", '5').replace("?", '7').replace(" ", "").replace(",", "").replace("E", "8").replace(".", "").replace("'", "").replace(u"‘", "")\
		.replace("B", "8").replace("\"", "").replace("I", "1").replace("i", "").replace("-", "").replace("$", "8").replace(u"’", "").strip()

	return code




def getIndex(keyword, province, city, length):
	openBrowser()
	time.sleep(2)
	js = 'window.open("http://index.baidu.com");'
	browser.execute_script(js)
	handles = browser.window_handles
	browser.switch_to_window(handles[-1])
	time.sleep(5)

	# input the keyword
	time.sleep(5)
	browser.find_element_by_class_name("search-input").clear()
	browser.find_element_by_class_name("search-input").send_keys(keyword)
	browser.find_element_by_class_name("search-input-cancle").click()
	time.sleep(5) #wait for response
	browser.maximize_window()
	time.sleep(2)


	# choose province and city
	browser.find_element_by_id("compOtharea").click()
	time.sleep(1)
	browser.find_element_by_xpath("//span[@class='selectA provA slided']//div//a[@href='#" + provinceDict[province] + "']").click()
	time.sleep(1)
	browser.find_element_by_xpath("//span[@class='selectA cityA slided']//div//a[@href='#" + cityDict[city] + "']").click()
	time.sleep(4)

	indexFile = open("./baidu/index.txt", "a", encoding='UTF-8')
	print("Start Time: " + str(time.strftime("%H:%M:%S")))
	indexFile.write("Start Time: " + str(time.strftime("%H:%M:%S"))+'\n')

	xoyelement = browser.find_elements_by_css_selector("#trend rect")[2]
	index = []

	try:
		y_0 = 25
		year = 2011
		day = 1
		month = 1

		chooseTime("01","06",year)

		data = browser.execute_script("return document.getElementsByTagName('path')[5].attributes['d']")
		data = data['nodeValue'].split('C')
		yarray = [data[0].split(',')[-1]]
		curves = data[1:]
		for cur in curves:
			yarray.append(cur.split(',')[-1])

		print(yarray)

		miny = 1000
		minpos = 0
		i = 0
		for y in yarray:
			if float(y) < miny:
				miny = float(y)
				minpos = i
			i = i + 1

		maxy = 0
		maxpos = 0
		i = 0

		for y in yarray:
			if float(y) > maxy:
				maxy = float(y)
				maxpos = i
			i = i + 1

		A = [minpos, maxpos]
		print(A)
		realA = []
		curvA = []
		width = int(browser.execute_script("return document.getElementsByTagName('svg')[0].getBBox()['width']"))
		for sample in A:
			curvA.append(yarray[sample])
			month,day = getDay(sample)
			realA.append(getSample(year,month,day,width,sample, xoyelement))
		# print(realA)
		# print(curvA)
		a_param = (int(realA[1])-int(realA[0]))/(float(curvA[1])-float(curvA[0]))
		b_param = int(realA[0]) - a_param * float(curvA[0])
		print(a_param)
		print(b_param)

		count = 0
		for y_data in yarray:
			month,day = getDay(count)
			if month < 10:
				monthName = '0'+str(month)
			else:
				monthName = str(month)

			if day < 10:
				dayName = '0'+str(day)
			else:
				dayName = str(day)

			name = str(year) + monthName + dayName

			realD = a_param * float(y_data) + b_param
			result = province + city+'-' +name +'-'+str(realD)+'\n'
			indexFile.write(result)

			count += 1

	except Exception as e:
		print(e)

	print("End Time: " + str(time.strftime("%H:%M:%S")))
	indexFile.write("End Time: " + str(time.strftime("%H:%M:%S")) + "\n")

	indexFile.close()

if __name__ == "__main__":
	# keyword = input("请输入查询关键字：")
	# province = input("请输入省份：")
	# city = input("请输入城市：")
	# length = int(input("请输入查询天数："))
	keyword = "600660"
	province = "北京"
	city = "北京"
	length = 10000
	getIndex(keyword, province, city, length)




