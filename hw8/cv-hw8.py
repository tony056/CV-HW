from PIL import Image
import sys, os, random
scriptDir = os.path.dirname(os.path.realpath(__file__))

def binarize(pixels, width, height):
	result = [[0 for x in range(0, width)] for y in range(0, height)]
	for i in range(0, len(pixels)):
		if pixels[i] < 128:
			result[i % width][i / height] = 0
		else:
			result[i % width][i / height] = 1
	return result

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
			median = medianOfNeighbor(x, y, extend_pixels)
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
	return extend_pixels

# def toImage(imageList):


if len(sys.argv) == 2:
	
	source_image = Image.open(sys.argv[1])
	source_image_pixels = list(source_image.getdata())

	imageW, imageH = source_image.size

	binary_image_pixels = binarize(source_image_pixels, source_image.size[0], source_image.size[1])

	binary_image = Image.new(source_image.mode, source_image.size, 0)
	binary_image_result = binary_image.load()

	gaussian10_image = Image.new(source_image.mode, source_image.size, 0)
	gaussian10_image_result = gaussian10_image.load()

	gaussian30_image = Image.new(source_image.mode, source_image.size, 0)
	gaussian30_image_result = gaussian30_image.load()

	saltAndPepperSmall_image = Image.new(source_image.mode, source_image.size, 0)
	saltAndPepperSmall_image_result = saltAndPepperSmall_image.load()

	saltAndPepperBig_image = Image.new(source_image.mode, source_image.size, 0)
	saltAndPepperBig_image_result = saltAndPepperBig_image.load()

	boxFilterSmall_image = Image.new(source_image.mode, source_image.size, 0)
	boxFilterSmall_image_result = boxFilterSmall_image.load()

	boxFilterBig_image = Image.new(source_image.mode, source_image.size, 0)
	boxFilterBig_image_result = boxFilterBig_image.load()

	gaussianNoisesTen = gaussianNoise(0, 1, 10, [imageW, imageH], source_image_pixels)
	gaussianNoisesThirty = gaussianNoise(0, 1, 30, [imageW, imageH], source_image_pixels)
	saltAndPepperSmall = saltAndPepper(0, 1, 0.05, [imageW, imageH], source_image_pixels)
	saltAndPepperBig = saltAndPepper(0, 1, 0.1, [imageW, imageH], source_image_pixels)

	boxFilterSmall = boxFilter(source_image.size, [3, 3], gaussianNoisesTen)
	boxFilterBig = boxFilter(source_image.size, [5, 5], gaussianNoisesTen)

	for y in range(0, imageH):
		for x in range(0, imageW):
			gaussian10_image_result[x, y] = gaussianNoisesTen[x][y]
			gaussian30_image_result[x, y] = gaussianNoisesThirty[x][y]
			saltAndPepperSmall_image_result[x, y] = saltAndPepperSmall[x][y]
			saltAndPepperBig_image_result[x, y] = saltAndPepperBig[x][y]
			boxFilterSmall_image_result[x, y] = boxFilterSmall[x][y]
			boxFilterBig_image_result[x, y] = boxFilterBig[x][y]

	gaussian10_image.save("%s/%s.jpg" % (scriptDir, 'gaussian10'))
	# gaussian10_image.show()

	gaussian30_image.save("%s/%s.jpg" % (scriptDir, 'gaussian30'))
	# gaussian30_image.show()

	saltAndPepperSmall_image.save("%s/%s.jpg" % (scriptDir, 'saltAndPepper_0.05'))
	# saltAndPepperSmall_image.show()

	saltAndPepperBig_image.save("%s/%s.jpg" % (scriptDir, 'saltAndPepper_0.1'))
	# saltAndPepperBig_image.show()

	boxFilterSmall_image.save("%s/%s.jpg" % (scriptDir, 'boxForGaussian'))
	boxFilterSmall_image.show()

	boxFilterBig_image.save("%s/%s.jpg" % (scriptDir, 'boxForGaussianBig'))
	boxFilterBig_image.show()

else:
	print 'please enter the path of source image!'