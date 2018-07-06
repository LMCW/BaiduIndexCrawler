import math
import os

def rmse(array1, array2):
	N = len(array1)
	sqSum = 0
	count = 0
	for i in range(N):
		if (math.fabs(array1[i]-array2[i]) < 100):
			sqSum += (array2[i]-array1[i])**2
			count += 1
	return math.sqrt(sqSum/count)
	

if __name__ == '__main__':
	f1 = open('./baidu/index.txt',"r")
	data1 = f1.read().split('\n')
	for i in range(181):
		data1[i] = float(data1[i])

	f2 = open('./baidu/index_2011.txt',"r")
	data2 = f2.read().split('\n')
	for i in range(181):
		data2[i] = int(data2[i].split('-')[-1])

	print(data1)
	print(data2[0:181])
	print(rmse(data1,data2[0:181]))

