import math
import os

def rmse(array1, array2):
	N = len(array1)
	sqSum = 0
	count = 0
	for i in range(N):
		if (math.fabs(array1[i]-array2[i]) < 10):
			sqSum += (array2[i]-array1[i])**2
			count += 1
		else:
			print(i,array1[i],array2[i])
	return math.sqrt(sqSum/count)
	

if __name__ == '__main__':
	f1 = open('./baidu/index.txt',"r")
	data1 = f1.read().split('\n')
	for i in range(2557):
		data1[i] = float(data1[i].split('-')[-1])

	f2 = open('./baidu/index_alltest.txt',"r")
	data2 = f2.read().split('\n')
	for i in range(2557):
		try:
			data2[i] = int(data2[i].split('-')[-1])
		except Exception as e:
			data2[i] = 0
		

	print(rmse(data1,data2))

