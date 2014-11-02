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
							self.map[i][j] = 1
						else:
							self.map[i][j] = 0
					else:
						self.map[i][j] = 1
	def makeSmallKernel(self):
		self.map = [[1, 1], [0, 1]]

	def hitMiss(self, j, k):
		for y in range(0, self.height):
			for x in range(0, self.width):
				if j[y][x] != 1 or k[y][x] != 1:
					self.map[y][x] = 0

		
	def copy(self, lists):
		for y in range(0, self.height):
			for x in range(0, self.width):
				self.map[y][x] = lists[y][x]

	def dialtion(self, kernel):
		result = [[0 for i in range(0, self.width)] for j in range(0, self.height)]
		for y in range(0, self.height):
			for x in range(0, self.width):
				if self.map[y][x] == 1:
					for checkY in range(y - kernel.centerY, y + (kernel.height - kernel.centerY)):
						for checkX in range(x - kernel.centerX, x + (kernel.width - kernel.centerX)):
							if (checkY >= 0 and checkY < self.height) and (checkX >= 0 and checkX < self.width):
								if kernel.map[checkY - (y - kernel.centerY)][checkX - (x - kernel.centerX)] == 1:
									result[checkY][checkX] = 1
		return result

	def erosion(self, kernel):
		result = [[0 for i in range(0, self.width)] for j in range(0, self.height)]
		for y in range(0, self.height):
			for x in range(0, self.width):
				if self.isMatch(kernel, x, y) == True:
					result[y][x] = 1
		return result
	def isMatch(self, kernel, x, y):
		for checkY in range(y - kernel.centerY, y + (kernel.height - kernel.centerY)):
			for checkX in range(x - kernel.centerX, x + (kernel.width - kernel.centerX)):
				if (checkY >= 0 and checkY < self.height) and (checkX >= 0 and checkX < self.width):
					if kernel.map[checkY - (y - kernel.centerY)][checkX - (x - kernel.centerX)] == 1:
						if self.map[checkY][checkX] != 1:
							return False
		return True
		

	def outputImage(self, name):
		size = [self.width, self.height]
		output = Image.new('L', size, 0)
		pixel = output.load()
		for y in range(0, self.height):
			for x in range(0, self.width):
				pixel[x, y] = self.map[y][x] * 255
		output.save("%s/%s.jpg" % (scriptDir, name))
		output.show()

if len(sys.argv) == 2:
	source_image = Image.open(sys.argv[1])
	imageW, imageH = source_image.size
	binary_source = Bitmap(source_image.size[0], source_image.size[1], 0, 0)
	reverse_binary = Bitmap(source_image.size[0], source_image.size[1], 0, 0)
	kernel_bitmap = Bitmap(5, 5, 2, 2)
	kernel_bitmap.makeKernel()
	source_image_pixels = list(source_image.getdata())
	

	for i in range(0, len(source_image_pixels)):
		if source_image_pixels[i] < 128:
			binary_source.map[i / imageW][i % imageW] = 0
		else:
			reverse_binary.map[i / imageW][i % imageW] = 0
	kernel_bitmap.outputImage('kernel')
	binary_source.outputImage('origin')

	dialtion_result = binary_source.dialtion(kernel_bitmap)
	erosion_result = binary_source.erosion(kernel_bitmap)

	dialtion_bitmap = Bitmap(imageW, imageH, 0, 0)
	dialtion_bitmap.copy(dialtion_result)
	dialtion_bitmap.outputImage('dialtion')

	erosion_bitmap = Bitmap(imageW, imageH, 0, 0)
	erosion_bitmap.copy(erosion_result)
	erosion_bitmap.outputImage('erosion')

	opening_result = erosion_bitmap.dialtion(kernel_bitmap)
	opening_bitmap = Bitmap(imageW, imageH, 0, 0)
	opening_bitmap.copy(opening_result)
	opening_bitmap.outputImage('opening')

	closing_result = dialtion_bitmap.erosion(kernel_bitmap)
	closing_bitmap = Bitmap(imageW, imageH, 0, 0)
	closing_bitmap.copy(closing_result)
	closing_bitmap.outputImage('closing')

	jKernel = Bitmap(2, 2, 1, 0)
	jKernel.makeSmallKernel()
	kKernel = Bitmap(2, 2, 0, 1)
	kKernel.makeSmallKernel()

	jPart_result = binary_source.erosion(jKernel)
	kPart_result = reverse_binary.erosion(kKernel)

	hm_bitmap = Bitmap(imageW, imageH, 0, 0)
	hm_bitmap.hitMiss(jPart_result, kPart_result)
	hm_bitmap.outputImage('hit&miss')


else:
	print 'please enter the path of source image!'