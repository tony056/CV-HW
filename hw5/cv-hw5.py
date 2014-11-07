from PIL import Image
import sys, os
scriptDir = os.path.dirname(os.path.realpath(__file__))

class Bitmap(object):
	def __init__(self, width, height, centerX, centerY):
		self.width = width
		self.height = height
		self.map = [[1 for i in range(0, width)] for j in range(0, height)]
		# self.reverseMap = [[1 for i in range(0, width)] for j in range(0, height)]
		self.centerX = centerX
		self.centerY = centerY
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
							return False
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
	def outputImage(self, name):
		size = [self.width, self.height]
		output = Image.new('L', size, 0)
		pixel = output.load()
		for y in range(0, self.height):
			for x in range(0, self.width):
				pixel[x, y] = self.map[y][x]
		output.save("%s/%s.jpg" % (scriptDir, name))
		output.show()

if len(sys.argv) == 2:
	source_image = Image.open(sys.argv[1])
	imageW, imageH = source_image.size
	grayscale_source = Bitmap(source_image.size[0], source_image.size[1], 0, 0)
	kernel_bitmap = Bitmap(5, 5, 2, 2)
	kernel_bitmap.makeKernel()
	source_image_pixels = list(source_image.getdata())
	

	for i in range(0, len(source_image_pixels)):
		grayscale_source.map[i / imageW][i % imageW] = source_image_pixels[i]
	
	kernel_bitmap.outputImage('kernel')
	grayscale_source.outputImage('origin')

	dilation_result = grayscale_source.dilation(kernel_bitmap)
	erosion_result = grayscale_source.erosion(kernel_bitmap)

	dilation_bitmap = Bitmap(imageW, imageH, 0, 0)
	dilation_bitmap.copy(dilation_result)
	dilation_bitmap.outputImage('dilation')

	erosion_bitmap = Bitmap(imageW, imageH, 0, 0)
	erosion_bitmap.copy(erosion_result)
	erosion_bitmap.outputImage('erosion')

	opening_result = erosion_bitmap.dilation(kernel_bitmap)
	opening_bitmap = Bitmap(imageW, imageH, 0, 0)
	opening_bitmap.copy(opening_result)
	opening_bitmap.outputImage('opening')

	closing_result = dilation_bitmap.erosion(kernel_bitmap)
	closing_bitmap = Bitmap(imageW, imageH, 0, 0)
	closing_bitmap.copy(closing_result)
	closing_bitmap.outputImage('closing')


else:
	print 'please enter the path of source image!'