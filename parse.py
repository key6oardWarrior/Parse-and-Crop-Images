#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 07 11:39:28 2019
@author: key6oardWarrior (https://github.com/key6oardWarrior)
"""

import urllib.request
import csv
import cv2
import os

def crop(top, bottom, left, right, fileName): # crop image
	image = cv2.imread("C:/Research/Bio/images/image" + fileName)
	cropped = image[top: bottom, left: right]

	cv2.imwrite("C:/Research/Bio/images/cropped/new" + fileName, cropped)
	# cv2.imshow("C:/Research/images/image" + fileName, image) # to veiw the og image
	# cv2.imshow("C:/Research/images/cropped/new" + fileName, cropped) # to view cropped image
	print(image.shape) # og image size
	print(cropped.shape) # new image size
	# cv2.waitKey(0) # uncomment to view images 

def downloadImage(url, imageFile): # download all images from internet
	imageFile = "C:/Research/Bio/images/image" + str(imageFile) + ".jpg"

	try:
		urllib.request.urlretrieve(url, imageFile)
	except:
		pass

def getInt(strRow, startPoint, i): # get ints in results file
	integer = 0

	try:
		integer = int(strRow[startPoint: i])
		i += 1
		return getInt(strRow, startPoint, i)
	except:
		i -= 1
		return int(strRow[startPoint: i])

def croppingValue(strRow, keyWord): # get values to crop image
	findStr = strRow.find(keyWord)
	value = 0

	if findStr != -1:
		if keyWord == '"height":':
			value = getInt(strRow, findStr+9, findStr+10)
		elif keyWord == '"top":':
			value = getInt(strRow, findStr+6, findStr+7)
		elif keyWord == '"left":':
			value = getInt(strRow, findStr+7, findStr+8)
		else:
			value = getInt(strRow, findStr+8, findStr+9)
		print(keyWord + " ", value)
		return value
	return value

def order(left, right, top, bottom, fileName): # order cropping values
	if (left < right) and (top < bottom):
		crop(top, bottom, left, right, fileName)
	elif (left > right) and (top > bottom):
		crop(bottom, top, right, left, fileName)
	elif (left > right) and (top < bottom):
		crop(top, bottom, right, left, fileName)
	elif (top > bottom) and (left < right):
		crop(bottom, top, left, right, fileName)

def countCommas(strRow):
	cnt = 0

	for i in strRow:
		if i == ",":
			cnt += 1

	return cnt

def stripRow(strRow, cnt): # remove unessary data from results (after copy was made)
	index = strRow.find(",")

	cnt += 1
	if cnt <= 5:
		return stripRow(strRow[index+1:], cnt)
	else:
		print("stripRow\n" + strRow)
		return strRow

def findUnionHelper(intervals, lenArr): # find intersection
	l = intervals[0][0]
	r = intervals[0][1]

	for i in range(1, lenArr):
		if (intervals[i][0] > r or intervals[i][1] < l):
			return -1
		else:
			l = max(l, intervals[i][0])
			r = min(r, intervals[i][1])

	lst = [l, r]
	return lst

def findUnion(strRow, left, right, top, bottom, cnt, fileName): # find union of number pairs
	if right > left:
		temp = left
		left = right
		right = temp

	if bottom > top:
		temp = top
		top = bottom
		bottom = temp

	left2Right = [
		[left, right]
	]

	top2Bottom = [
		[top, bottom]
	]

	cnt = cnt // 5

	for i in range(1, cnt): # populate lists with data from results
		strRow = stripRow(strRow, 0)

		left = croppingValue(strRow, '"left":')
		right = croppingValue(strRow, '"width":')
		if left <= right:
			left2Right.append([left, right])
		else:
			left2Right.append([right, left])

		top = croppingValue(strRow, '"top":')
		bottom = croppingValue(strRow, '"height":')
		if top <= bottom:
			top2Bottom.append([top, bottom])
		else:
			top2Bottom.append([bottom, top])

	left2Right.sort()
	top2Bottom.sort()
	print(left2Right, top2Bottom)

	lengthOfArr = len(left2Right[0])
	left2Right = findUnionHelper(left2Right, lengthOfArr)

	lengthOfArr = len(top2Bottom[0])
	top2Bottom = findUnionHelper(top2Bottom, lengthOfArr)

	if (left2Right != -1) and (top2Bottom != -1): # determin was arguments are need order function needs
		order(left2Right[0], left2Right[1], top2Bottom[0], top2Bottom[1], fileName)
	elif (left2Right != -1) and (top2Bottom == -1):
		order(left2Right[0], left2Right[1], 0, 0, fileName)
	elif (left2Right == -1) and (top2Bottom != -1):
		order(0, 0, top2Bottom[0], top2Bottom[1], fileName)
	else: # if (left2Right == -1) and (top2Bottom == -1):
		pass

# Open file and read data
with open("C:/Research/Bio/results/result.csv") as csvfile:
	readCSV = csv.reader(csvfile, delimiter = ",")
	strRow = ""
	left = 0
	right = 0
	top = 0
	bottom = 0
	i = 0

	for row in readCSV:
		# Open file and write
		with open("C:/Research/Bio/results/results.csv", "w", newline = "") as new_csvfile:
			writer = csv.writer(new_csvfile)
			writer.writerows(row)

		print("Image:\n", row[27: 28], "\nCords: \n", row[70: 71])
		strRow = str(row[70: 71]) + ","
		temp = 0

		left = croppingValue(strRow, '"left":')
		right = croppingValue(strRow, '"width":')
		top = croppingValue(strRow, '"top":')
		bottom = croppingValue(strRow, '"height":')

		# download image
		downloadImage(str(row[27: 28])[2: len(row[27: 28])-3], i)
		fileName = str(i) + ".jpg"

		commas = countCommas(strRow)
		if commas <= 5: # if there is no over lap
			if os.path.exists("C:/Research/Bio/images/image" + fileName):
				order(left, right, top, bottom, fileName)
			else:
				continue
		else:
			findUnion(strRow, left, right, top, bottom, commas, fileName)

		i += 1