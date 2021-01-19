import os
import threading
import cv2
import wget
import pandas as pd

'''
OOP is used over Procedural Programming because is it faster to make
a large data structure global to the instance of the class rather than
pass by value.
'''
fileCnt = 0

class GetData:
	'''
	Get and format all user data from CSV_FILE
	'''
	def __init__(self, FILE_DATA):
		self.FILE_DATA = FILE_DATA

	def getIDs(self):
		self.ids = []
		biggest = 0

		LEN = len(self.allIDs)
		for i in range(LEN):
			index = self.allIDs[i].index(":")
			self.ids.append((self.allIDs[i])[: index])

	def getResponces(self):
		'''
		Put all user responces in userData (<class 'dict'>), so they can
		be put in a comma delimited csv file.
		'''
		conceptIDs = {
			"Concept IDs": [],
			"Answer.annotation_data": []
		}
		KEYWORD = "Answer.Keyword"
		KEYWORD1 = "Answer.annotation_data"
		isKey = True

		for i in self.FILE_DATA[KEYWORD]:
			self.allIDs = i.split("|")
			self.getIDs()
			conceptIDs["Concept IDs"].append(self.ids)
		
		for  i in self.FILE_DATA[KEYWORD1]:
			allAns = (i.split(","))[4]
			data = (allAns.split(":"))[1]
			conceptIDs[KEYWORD1].append(data)

		conceptIdFile = pd.DataFrame(conceptIDs)
		conceptIdFile.to_csv(f"..\\MSU-CS\\results\\filteredConceptIDs{fileCnt}.csv", sep=",")

	def downloadImages(self):
		userData = {}
		IMAGE_FILE = "..\\MSU-CS\\images\\"
		KEYWORD = "Input.image_url"
		KEYWORD1 = "Answer.Keyword"
		prev = ""
		isKey = True

		cnt = 0
		os.system(f"mkdir {IMAGE_FILE}")

		for i in self.FILE_DATA[KEYWORD]:
			if type(i) != str:
				continue

			if i == prev:
				continue

			path = f"{IMAGE_FILE}{cnt}.jpg"

			if isKey:
				userData[KEYWORD] = []
				userData[KEYWORD1] = []
				isKey = False

			try: # if server does not respond error is not fatal
				userData[KEYWORD].append(wget.download(i, path))
			except:
				print(f"\nImage {i} could not be downloaded")
				userData[KEYWORD].append(f"Image {i} could not be downloaded")
				userData[KEYWORD1].append(f"Image {i} could not be downloaded")
				continue

			userData[KEYWORD1].append(self.FILE_DATA[KEYWORD1][cnt])
			cnt += 1
			prev = i

		imagesDataFrame = pd.DataFrame(userData)
		imagesDataFrame.to_csv(f"..\\MSU-CS\\results\\filteredResults{fileCnt}.csv", sep=",")

class FindUnion:
	'''
	Find the union between all the user data given. Then use the data
	to crop an image 
	'''
	def __init__(self, FILE_DATA, THREAD):
		'''
		Get all the cropping values given from user.

		@param <class 'pandas.core.frame.DataFrame'> \n
		@param <class 'threading.Thread'> downloading images thread
		'''
		self.THREAD = THREAD

		self.orignalCroppingValues = {}
		KEYWORD = "Answer.annotation_data"
		IMAGE = "Image"
		cnt = 0

		for i in FILE_DATA[KEYWORD]:
			self.getCropHelper(i)
			self.orignalCroppingValues[cnt] = self.tempValues
			cnt += 1
	
	def getCropHelper(self, DATA):
		'''
		Find numbers in FILE_DATA[KEYWORD][DATA] and add each number to a list.

		@param <class 'str'>
		'''
		self.tempValues = []
		temp = ""
		STOP = len(DATA)-1

		for i in range(STOP):
			if DATA[i].isnumeric():
				temp += DATA[i]

			if((temp != "") and (DATA[i+1].isnumeric() == False)):
				self.tempValues.append(int(temp.replace(" ", "")))
				temp = ""

	def crop(self):
		'''
		crop each image based on the directional values
		found in left, top, width, and height
		'''
		left = []
		top = []
		PATH = "..\\MSU-CS\\images\\"
		KEYWORD = "Input.image_url"
		STOP = len(self.newLeft)

		print("\n")
		os.system(f"mkdir {PATH}croppedImages{fileCnt}\\")

		self.THREAD.join()

		for i in range(STOP):
			if type(self.newLeft[i]) != int:
				continue
			if type(self.newTop[i]) != int:
				continue

			strI = str(i)
			image = cv2.imread(f"{PATH}{strI}.jpg")
			left = (self.newLeft[i]) if self.newLeft[i] > 0 else 1
			top = (self.newTop[i]) if self.newTop[i] > 0 else 1

			cropped = image[top: len(image[0]), left: len(image[0])]
			cv2.imwrite(f"{PATH}croppedImages{fileCnt}\\{strI}.jpg", cropped)
			# cv2.imshow(f"{PATH}{strI}.jpg", image) # to veiw the og image
			# cv2.imshow(f"{PATH}croppedImages{fileCnt}\\{strI}.jpg", cropped) # to view cropped image
			# print(image.shape) # og image size
			# print(cropped.shape) # new image size
			# cv2.waitKey(0) # uncomment to view images

	def helper(self, VALUE, VALUE1):
		'''
		Determin which value is bigger and if the smaller value is
		within the threshold (60%) of the bigger value. If the
		smaller value is not within the threshold, then return
		"No union found" else return the smaller value.

		@param <class 'int'>\n
		@param <class 'int'>\n
		@return <class 'str'> or <class 'int'>
		'''
		THRESHOLD = 0.60

		if VALUE > VALUE1:
			if((VALUE1 >= (VALUE * THRESHOLD)) and (VALUE1 <= VALUE)):
				return VALUE1
			return "No union found"

		if((VALUE >= (VALUE1 * THRESHOLD)) and (VALUE <= VALUE1)):
			return VALUE
		return "No union found"

	def getDirectionData(self, DIRECTION=0, isLast=False):
		'''
		get data for a given direction

		DIRECTION = 0 = left\n
		DIRECTION = 1 = top\n
		DIRECTION = 2 = width\n
		DIRECTION = 3 = height

		@param <class 'int'>\n
		@param <class 'bool>\n
		@return <class 'list'>
		'''
		data = []

		for i in self.croppingValues.keys():
			value = self.croppingValues[i][DIRECTION]
			temp = (i - 1) if isLast else (i + 1)
			value1 = self.croppingValues1[temp][DIRECTION]

			data.append(self.helper(value, value1))

		return data
	
	def reduceDimension(self, INDEX, DIRECTION=0):
		'''
		@param <class 'int'>\n
		@param <class 'int'>\n
		@return <class 'int'> or <class 'str'>
		'''
		direction = []

		if DIRECTION == 0:
			direction = self.left
		elif DIRECTION == 1:
			direction = self.top
		elif DIRECTION == 2:
			direction = self.width
		else:
			direction = self.height
		
		LEN = len(direction)
		lowest = direction[0][INDEX]

		for i in range(1, LEN):
			if type(lowest) == str:
				if type(direction[i][INDEX]) == int:
					lowest = direction[i][INDEX]
			elif type(direction[i][INDEX]) == int:
				if lowest > direction[i][INDEX]:
					lowest = direction[i][INDEX]
		return lowest

	def setValues(self, isFirst=True):
		'''
		@param <class 'bool'>
		'''
		if isFirst:
			for i in range(self.start, self.end, self.USERS_SURVEYED):
				self.croppingValues.update({i: self.orignalCroppingValues[i]})
		else:
			for i in range(self.start, self.end, self.USERS_SURVEYED):
				self.croppingValues1.update({i: self.orignalCroppingValues[i]})

	def findUnion(self):
		self.left = []
		self.top = []
		self.width = []
		self.height = []

		# META DATA CONSTANTS
		NUM_OF_QUESTIONS = 13 # 500
		LENGTH = len(self.orignalCroppingValues.keys())
		self.USERS_SURVEYED = LENGTH // NUM_OF_QUESTIONS

		if self.USERS_SURVEYED < 2: # 5
			raise RuntimeError(f"Number of people surveyed in this study is {self.USERS_SURVEYED}. The number must be 2 or greater")

		'''
		this allows each user's responces to be compared to each
		other and then find the union
		'''
		stop = 0
		isEven = True
		if self.USERS_SURVEYED % 2 == 0:
			stop = int(self.USERS_SURVEYED / 2)
		else:
			stop = int((self.USERS_SURVEYED+1) / 2)
			isEven = False

		for cnt in range(stop):
			self.croppingValues = {}
			self.start = (self.start + 1) if cnt != 0 else 0
			self.end = (self.end + 1) if cnt != 0 else NUM_OF_QUESTIONS*self.USERS_SURVEYED

			self.setValues()

			if((isEven) or (cnt < (stop - 1))):
				self.croppingValues1 = {}
				self.start += 1
				self.end += 1

				self.setValues(False)

				self.left.append(self.getDirectionData())
				self.top.append(self.getDirectionData(1))
				self.width.append(self.getDirectionData(2))
				self.height.append(self.getDirectionData(3))
			else:
				self.left.append(self.getDirectionData(isLast=True))
				self.top.append(self.getDirectionData(1, True))
				self.width.append(self.getDirectionData(2, True))
				self.height.append(self.getDirectionData(3, True))

		if self.USERS_SURVEYED > 2:
			self.newLeft = []
			self.newTop = []
			self.newWidth = []
			self.newHeight = []
			STOP = len(self.left[0])

			for i in range(STOP):
				self.newLeft.append(self.reduceDimension(i))
				self.newTop.append(self.reduceDimension(i, 1))
				self.newWidth.append(self.reduceDimension(i, 2))
				self.newHeight.append(self.reduceDimension(i, 3))
		else:
			self.newLeft = self.left[0]
			self.newTop = self.top[0]
			self.newWidth = self.width[0]
			self.newHeight = self.height[0]

		self.crop()

class Setup:
	def __init__(self):
		pass

	def replaceFile(self):
		'''
		@return <class 'str'> file location of csv file
		'''
		csvFile = input("\nEnter  Each File Location: ")

		while os.path.exists(csvFile) == False:
			print(f"\nThe file {csvFile} does not exist.")
			csvFile = input("\nEach File Location: ")
		return csvFile

	def realFile(self):
		'''
		Check if a file exist. If it does return file. If it does not keep asking
		the user to enter the rigth file.
		'''
		csvFile = input("\nEnter  Each File Location(s) Seprated By A Space: ")
		self.files = csvFile.split(" ")

		for i in range(len(self.files)):
			while os.path.exists(self.files[i]) == False:
				print(f"\nThe file: {self.files[i]} does not exist!")
				self.files[i] = input("\nEnter File Location: ")

	def fileChecker(self):
		'''
		Check if files meets the criteria for being used in the experiment.
		The DataFrame contains all the necessary data from the study.
		'''
		self.dictList = []
		filteredFiles = []

		for i in range(len(self.files)):
			if self.files[i] in filteredFiles:
				continue

			fileData = pd.read_csv(self.files[i])
			# fileData = pd.read_csv(csvFile)
			# type(fileData) is <class 'pandas.core.frame.DataFrame'>
			# type(fileData['nameOfCol']) is <class 'str'>
			# type(fileData['nameOfCol'][rowNumber]) is <class 'str'>

			# csv files created by this code will be comma delimited
			# fileData.to_csv("..\\MSU-CS\\results\\fileName.csv", sep=",")

			while len(fileData) < 1:
				print("\nThe CSV file cannot be empty.")
				self.replaceFile()
				fileData = pd.read_csv(self.files[i])
				if self.files[i] in filteredFiles:
					continue

			filteredFiles.append(self.files[i])
			self.dictList.append(fileData)

	def start(self):
		'''
		@return <class 'bool'> True if another file needs to run through algorithm
		'''
		setup.realFile()
		setup.fileChecker()

		for i in self.dictList:
			getData = GetData(i)

			downloadImagesThread = threading.Thread(target=getData.downloadImages, args=())
			conceptIDsThread = threading.Thread(target=getData.getResponces, args=())

			downloadImagesThread.start()
			conceptIDsThread.start()

			union = FindUnion(i, downloadImagesThread)
			union.findUnion()

			conceptIDsThread.join()

setup = Setup()
setup.start()
