from PIL import Image
import sys, os, random
scriptDir = os.path.dirname(os.path.realpath(__file__))

class Bitmap(object):
	def __init__(self, width, height, centerX, centerY):
		self.width = width
		self.height = height
		self.map = [[0 for i in range(0, width)] for j in range(0, height)]
		# self.reverseMap = [[1 for i in range(0, width)] for j in range(0, height)]
		self.centerX = centerX
		self.centerY = centerY
	def sourceToPixel(self, source):
		for y in range(0, self.height):
			for x in range(0, self.width):
				self.map[x][y] = source[y * self.width + x]
	def makeKernel(self):
		if self.width == 5 and self.height == 5:
			for i in range(0, self.height):
				for j in range(0, self.width):
					if i == 0 or i == self.height - 1:
						if j >= 1 and j <= 3:
							self.map[i][j] = 0
						else:
							self.map[i][j] = 255
					else:
						self.map[i][j] = 0
		
	def copy(self, lists):
		for y in range(0, self.height):
			for x in range(0, self.width):
				self.map[y][x] = lists[y][x]

	def dilation(self, kernel):
		result = [[0 for i in range(0, self.width)] for j in range(0, self.height)]
		for y in range(0, self.height):
			for x in range(0, self.width):
				# if self.map[y][x] == 1:
				localMax = 0
				grayNum = 0
				for checkY in range(y - kernel.centerY, y + (kernel.height - kernel.centerY)):
					for checkX in range(x - kernel.centerX, x + (kernel.width - kernel.centerX)):
						if (checkY >= 0 and checkY < self.height) and (checkX >= 0 and checkX < self.width):
							if kernel.map[checkY - (y - kernel.centerY)][checkX - (x - kernel.centerX)] == 0 and self.map[checkY][checkX] > 0:
								# result[checkY][checkX] = 1	
								localMax = self.maxValue(self.map[checkY][checkX], localMax)
				
				result[y][x] = localMax
		return result

	def erosion(self, kernel):
		result = [[0 for i in range(0, self.width)] for j in range(0, self.height)]
		for y in range(0, self.height):
			for x in range(0, self.width):
				isMatch, localMin = self.isMatch(kernel, x, y)
				if isMatch == True:
					result[y][x] = localMin 
		return result
	def isMatch(self, kernel, x, y):
		localMin = self.map[y][x]
		for checkY in range(y - kernel.centerY, y + (kernel.height - kernel.centerY)):
			for checkX in range(x - kernel.centerX, x + (kernel.width - kernel.centerX)):

				if (checkY >= 0 and checkY < self.height) and (checkX >= 0 and checkX < self.width):
					if kernel.map[checkY - (y - kernel.centerY)][checkX - (x - kernel.centerX)] == 0:
						if self.map[checkY][checkX] == 0:
							return False, localMin
						else:
							localMin = self.minValue(self.map[checkY][checkX], localMin)

		return True, localMin

	def maxValue(self, a, b):
		num = [a, b]
		num.sort()
		return num[1]
		
	def minValue(self, a, b):
		num = [a, b]
		num.sort()
		return num[0]

	def openingClosing(self, kernel):
		#ed
		self.map = self.erosion(kernel)
		self.map = self.dilation(kernel)
		self.map = self.dilation(kernel)
		self.map = self.erosion(kernel)

	def closingOpening(self, kernel):
		self.map = self.dilation(kernel)
		self.map = self.erosion(kernel)
		self.map = self.erosion(kernel)
		self.map = self.dilation(kernel)

	def outputImage(self, name, index):
		size = [self.width, self.height]
		output = Image.new('L', size, 0)
		pixel = output.load()
		for y in range(0, self.height):
			for x in range(0, self.width):
				pixel[x, y] = self.map[x][y]
		noiseName = ""
		if index == 0:
			noiseName = "GaussianNoise10"
		elif index == 1:
			noiseName = "GaussianNoise30"
		elif index == 2:
			noiseName = "SaltAndPepper0.05"
		elif index == 3:
			noiseName = "SaltAndPepper0.1"
		output.save("%s/%s.jpg" % (scriptDir, name + '_' + noiseName))
		# output.show()

def gaussianNoise(mu, sigma, amplitude, sizes, pixels):
	result = [[0 for x in range(0, sizes[0])] for y in range(0, sizes[1])]
	for y in range(0, sizes[1]):
		for x in range(0, sizes[0]):
			num = amplitude * random.gauss(mu, sigma)
			result[x][y] = num + pixels[y * sizes[0] + x]
	return result

def saltAndPepper(start, end, threshold, sizes, pixels):
	result = [[0 for x in range(0, sizes[0])] for y in range(0, sizes[1])]
	for y in range(0, sizes[1]):
		for x in range(0, sizes[0]):
			num = random.uniform(start, end)
			if num < threshold:
				result[x][y] = 0
			elif num > (1 - threshold):
				result[x][y] = 255
			else:
				result[x][y] = pixels[y * sizes[0] + x]
	return result

def boxFilter(sizes, boxSizes, pixels):
	extend_pixels = extend(sizes, boxSizes, pixels)
	result = [[0 for x in range(0, sizes[0])] for y in range(0, sizes[1])]
	for y in range(0, sizes[1]):
		for x in range(0, sizes[0]):
			average = averageOfNeighbor(x, y, boxSizes, extend_pixels)
			result[x][y] = average
	return result

def averageOfNeighbor(x, y, boxSizes, pixels):
	num = 0
	for localY in range(y - (boxSizes[1] / 2), y + (boxSizes[1] / 2 + 1)):
		for localX in range(x - (boxSizes[0] / 2), x + (boxSizes[0] / 2 + 1)):
			num += pixels[localX][localY]
	return int(num / (boxSizes[0] * boxSizes[1]))  

def medianFilter(sizes, neighborSizes, pixels):
	extend_pixels = extend(sizes, neighborSizes, pixels)
	result = [[0 for x in range(0, sizes[0])] for y in range(0, sizes[1])]
	for y in range(0, sizes[1]):
		for x in range(0, sizes[0]):
			median = medianOfNeighbor(x, y, neighborSizes, extend_pixels)
			result[x][y] = median
	return result

def medianOfNeighbor(x, y, neighborSizes, pixels):
	num = 0
	local = []
	for localY in range(y - (neighborSizes[1] / 2), y + (neighborSizes[1] / 2 + 1)):
		for localX in range(x - (neighborSizes[0] / 2), x + (neighborSizes[0] / 2 + 1)):
			local.append(pixels[localX][localY])
	sortedList = sorted(local)
	return sortedList[int(len(sortedList) / 2)]

def extend(sizes, extendSizes, pixels):
	extendNum = int(extendSizes[0] / 2) * 2
	extend_pixels = [[0 for x in range(0, sizes[0] + extendNum)] for y in range(0, sizes[1] + extendNum)]
	startPoint = int(extendNum / 2)
	for y in range(startPoint, sizes[1] + startPoint):
		for x in range(startPoint, sizes[0] + startPoint):
			extend_pixels[x][y] = pixels[x - startPoint][y - startPoint]

	for y in range(0, startPoint):
		for x in range(startPoint, sizes[0] + startPoint):
			extend_pixels[x][y] = extend_pixels[x][startPoint]

	for x in range(0, startPoint):
		for y in range(startPoint, sizes[1] + startPoint):
			extend_pixels[x][y] = extend_pixels[startPoint][y]

	for y in range(startPoint - 1, 0, -1):
		for x in range(startPoint - 1, 0, -1):
			extend_pixels[x][y] = int((extend_pixels[x + 1][y] + extend_pixels[x][y + 1]) / 2)

	return extend_pixels

def fileNameGenerator(index, size, filterName):
	noiseName = ""
	if index == 0:
		noiseName = "GaussianNoise10"
	elif index == 1:
		noiseName = "GaussianNoise30"
	elif index == 2:
		noiseName = "SaltAndPepper0.05"
	elif index == 3:
		noiseName = "SaltAndPepper0.1"
	string = filterName + '_' + noiseName + '_filterSize-' + str(size)
	return string


if len(sys.argv) == 2:
	
	source_image = Image.open(sys.argv[1])
	source_image_pixels = list(source_image.getdata())

	imageW, imageH = source_image.size

	gaussian10_image = Image.new(source_image.mode, source_image.size, 0)
	gaussian10_image_result = gaussian10_image.load()

	gaussian30_image = Image.new(source_image.mode, source_image.size, 0)
	gaussian30_image_result = gaussian30_image.load()

	saltAndPepperSmall_image = Image.new(source_image.mode, source_image.size, 0)
	saltAndPepperSmall_image_result = saltAndPepperSmall_image.load()

	saltAndPepperBig_image = Image.new(source_image.mode, source_image.size, 0)
	saltAndPepperBig_image_result = saltAndPepperBig_image.load()

	


	boxFilter_image = Image.new(source_image.mode, source_image.size, 0)
	boxFilter_image_result = boxFilter_image.load()

	medianFilter_image = Image.new(source_image.mode, source_image.size, 0)
	medianFilter_image_result = medianFilter_image.load()

	grayscale_source = Bitmap(source_image.size[0], source_image.size[1], 0, 0)
	grayscale_source.sourceToPixel(source_image_pixels)
	kernel_bitmap = Bitmap(5, 5, 2, 2)
	kernel_bitmap.makeKernel()

	noiseImages = []
	noiseImages.append(gaussianNoise(0, 1, 10, [imageW, imageH], source_image_pixels))
	noiseImages.append(gaussianNoise(0, 1, 30, [imageW, imageH], source_image_pixels))
	noiseImages.append(saltAndPepper(0, 1, 0.05, [imageW, imageH], source_image_pixels))
	noiseImages.append(saltAndPepper(0, 1, 0.1, [imageW, imageH], source_image_pixels))


	for y in range(0, imageH):
		for x in range(0, imageW):
			gaussian10_image_result[x, y] = noiseImages[0][x][y]
			gaussian30_image_result[x, y] = noiseImages[1][x][y]
			saltAndPepperSmall_image_result[x, y] = noiseImages[2][x][y]
			saltAndPepperBig_image_result[x, y] = noiseImages[3][x][y]

	box = [[3, 3], [5, 5]]

	for j in range(0, len(noiseImages)):
		for i in box:
			boxResult = boxFilter(source_image.size, i, noiseImages[j])
			medianResult = medianFilter(source_image.size, i, noiseImages[j])
			for y in range(0, imageH):
				for x in range(0, imageW):
					boxFilter_image_result[x, y] = boxResult[x][y]
					medianFilter_image_result[x, y] = medianResult[x][y]
			boxFilter_image.save("%s/%s.jpg" % (scriptDir, fileNameGenerator(j, i[0], 'Boxfilter')))
			medianFilter_image.save("%s/%s.jpg" % (scriptDir, fileNameGenerator(j, i[0], 'Medianfilter')))
	# noiseImages_bitmap = []
	for i in xrange(len(noiseImages)):
		print i
		opening_closing_bitmap = Bitmap(imageW, imageH, 0, 0)
		opening_closing_bitmap.copy(noiseImages[i])
		opening_closing_bitmap.openingClosing(kernel_bitmap)
		opening_closing_bitmap.outputImage('opening-closing', i)

		closing_opening_bitmap = Bitmap(imageW, imageH, 0, 0)
		closing_opening_bitmap.copy(noiseImages[i])
		closing_opening_bitmap.closingOpening(kernel_bitmap)
		closing_opening_bitmap.outputImage('closing-opening', i)
		del opening_closing_bitmap
		del closing_opening_bitmap


	gaussian10_image.save("%s/%s.jpg" % (scriptDir, 'gaussian10'))
	gaussian30_image.save("%s/%s.jpg" % (scriptDir, 'gaussian30'))
	saltAndPepperSmall_image.save("%s/%s.jpg" % (scriptDir, 'saltAndPepper_0.05'))
	saltAndPepperBig_image.save("%s/%s.jpg" % (scriptDir, 'saltAndPepper_0.1'))

else:
	print 'please enter the path of source image!'