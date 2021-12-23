import time as t
import cv2 as cv

logFile = "monitoringsystem.log"

class item:
	def __init__(self, time, image):
		self.time = time
		self.image = image

def searchIndex(arr, x):
	pos = -1
	for i in range(0, len(arr)):
		if x > int(arr[i].time):
			pos = i
	return pos

def showImages(arr):
	for a in arr:
		image = cv.imread(a.image[:len(a.image)-1])
		cv.imshow("original",image)
		cv.waitKey(0)
	cv.destroyAllWindows() # 会卡住

items = []
fp = open(logFile)
for line in fp.readlines():
	info = line.split(":")
	time = info[2]
	image = info[3]
	items.append(item(time, image))
fp.close()

while 1:
	print("请输入你要查询的起始时间")
	print("示例格式：2021-12-20 6:40:00")
	str = input()
	try:
		timeArray = t.strptime(str, "%Y-%m-%d %H:%M:%S")
		timeStamp1 = int(t.mktime(timeArray))
	except:
		print("时间格式错误 请重新输入")
		continue
	print("请输入你要查询的终止时间")
	print("示例格式：2021-12-20 7:40:00")
	str = input()
	try:
		timeArray = t.strptime(str, "%Y-%m-%d %H:%M:%S")
		timeStamp2 = int(t.mktime(timeArray))
	except:
		print("时间格式错误 请重新输入")
		continue

	selectedItems = []
	startIndex = searchIndex(items, timeStamp1)
	endIndex = searchIndex(items, timeStamp2)
	flag = False
	startIndex = startIndex + 1
	if startIndex <= endIndex:
		selectedItems = items[startIndex:endIndex+1]
	if len(selectedItems) == 0:
		print("此时间段内没有监控数据")
		continue
	showImages(selectedItems)