import os
import math

def merge():
	fo = open('./city_list.txt',"r")
	fw = open('./baidu/index_600660.txt','w')
	cities = fo.readlines()

	src = './baidu/data/index_'
	for city in cities:
		city = city.strip('\n')
		name_data = city.split(' ')
		filename = src+name_data[0]+'_'+name_data[1]+'.txt'
		print(filename)
		fc = open(filename,'r')
		try:
			content = fc.readlines()
		except Exception as e:
			content = []	
		for line in content:
			line = line.strip('\n')
			if 'Time' in line:
				continue
			else:
				fw.write('600660-'+name_data[2]+'-'+line+'\n')

		fc.close()

	fo.close()
	fw.close()

	
if __name__ == '__main__':
	merge()