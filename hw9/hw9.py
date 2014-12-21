from PIL import Image
import sys, os, random, math, copy
scriptDir = os.path.dirname(os.path.realpath(__file__))


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

def edgeOperator(neighbors, masks, sizes, threshold):
	num = len(masks)
	magnitude = []
	for i in range(0, num):
		r = 0
		for y in xrange(sizes[1]):
			for x in xrange(sizes[0]):
				r += (neighbors[x][y] * masks[i][x][y])
		magnitude.append(r ** 2)
	result = math.sqrt(sum(magnitude))
	return (result > threshold) 

def maxOperator(neighbors, masks, sizes, threshold):
	num = len(masks)
	magnitude = []
	index = 0
	for i in range(0, num):
		r = 0
		for y in xrange(sizes[1]):
			for x in xrange(sizes[0]):
				r += (neighbors[x][y] * masks[i][x][y])
		magnitude.append(r)
	result = max(magnitude)
	return (result > threshold) 

def robertDetector(pixelPosition, pixels, threshold):
	masks = [[[-1, 0], [0, 1]], [[0, -1],[1, 0]]]
	x = pixelPosition[0]
	y = pixelPosition[1]
	neighbors = []
	neighbors.append([pixels[x][y], pixels[x + 1][y]])
	neighbors.append([pixels[x][y + 1], pixels[x + 1][y + 1]])
	return 0 if edgeOperator(neighbors, masks, [2, 2], threshold) is True else 255

def prewittDetector(pixelPosition, pixels, threshold):
	masks = [[[-1, -1, -1], [0, 0, 0], [1, 1, 1]], [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]]
	neighbors = getNeighbors(pixelPosition, pixels, [3, 3])
	return 0 if edgeOperator(neighbors, masks, [3, 3], threshold) is True else 255

def sobelDetector(pixelPosition, pixels, threshold):
	masks = [[[-1, -2, -1], [0, 0, 0], [1, 2, 1]], [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]]
	neighbors = getNeighbors(pixelPosition, pixels, [3, 3])
	return 0 if edgeOperator(neighbors, masks, [3, 3], threshold) is True else 255

def freichenDetector(pixelPosition, pixels, threshold):
	sqrt2 = math.sqrt(2)
	masks = [[[-1, -sqrt2, -1], [0, 0, 0], [1, sqrt2, 1]], [[-1, 0, 1], [-sqrt2, 0, sqrt2], [-1, 0, 1]]]
	neighbors = getNeighbors(pixelPosition, pixels, [3, 3])
	return 0 if edgeOperator(neighbors, masks, [3, 3], threshold) is True else 255

def kirschDetector(pixelPosition, pixels, threshold):
	masks = [[[-3, -3, 5], [-3, 0, 5], [-3, -3, 5]],
		[[-3, 5, 5], [-3, 0, 5], [-3, -3, -3]],
		[[5, 5, 5], [-3, 0, -3], [-3, -3, -3]],
		[[5, 5, -3], [5, 0, -3], [-3, -3, -3]],
		[[5, -3, -3], [5, 0, -3], [5, -3, -3]],
		[[-3, -3, -3], [5, 0, -3], [5, 5, -3]],
		[[-3, -3, -3], [-3, 0, -3], [5, 5, 5]],
		[[-3, -3, -3], [-3, 0, 5], [-3, 5, 5]]]
	neighbors = getNeighbors(pixelPosition, pixels, [3, 3])
	return 0 if maxOperator(neighbors, masks, [3, 3], threshold) is True else 255

def robinsonDetector(pixelPosition, pixels, threshold):
	masks = [[[-1, -2, -1], [0, 0, 0], [1, 2, 1]],
		[[0, -1, -2], [1, 0, -1], [2, 1, 0]],
		[[1, 0, -1], [2, 0, -2], [1, 0, -1]],
		[[2, 1, 0], [1, 0, -1], [0, -1, -2]],
		[[1, 2, 1], [0, 0, 0], [-1, -2, -1]],
		[[0, 1, 2], [-1, 0, 1], [-2, -1, 0]],
		[[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
		[[-2, -1, 0], [-1, 0, 1], [0, 1, 2]]]
	neighbors = getNeighbors(pixelPosition, pixels, [3, 3])
	return 0 if maxOperator(neighbors, masks, [3, 3], threshold) is True else 255
def nevatiababuDetector(pixelPosition, pixels, threshold):
	masks = [[[100, 100, 0, -100, -100], [100, 100, 0, -100, -100], [100, 100, 0, -100, -100], [100, 100, 0, -100, -100], [100, 100, 0, -100, -100]],
	[[100, 100, 100, 32, -100], [100, 100, 92, -78, -100], [100, 100, 0, -100, -100], [100, 78, -92, -100, -100], [100, -32, -100, -100, -100]],		
	[[100, 100, 100, 100, 100], [100, 100, 100, 78, -32], [100, 92, 0, -92, -100], [32, -78, -100, -100, -100], [-100, -100, -100, -100, -100]],
	[[-100, -100, -100, -100, -100], [-100, -100, -100, -100, -100], [0, 0, 0, 0, 0], [100, 100, 100, 100, 100], [100, 100, 100, 100, 100]],
	[[-100, -100, -100, -100, -100], [32, -78, -100, -100, -100], [100, 92, 0, -92, -100], [100, 100, 100, 78, -32], [100, 100, 100, 100, 100]],
	[[100, -32, -100, -100, -100], [100, 78, -92, -100, -100], [100, 100, 0, -100, -100], [100, 100, 92, -78, -100], [100, 100, 100, 32, -100]],
	]
	neighbors = getNeighbors(pixelPosition, pixels, [5, 5])
	return 0 if maxOperator(neighbors, masks, [5, 5], threshold) is True else 255

def getNeighbors(pixelPosition, pixels, sizes):
	x = pixelPosition[0]
	y = pixelPosition[1]
	base = int(sizes[0] / 2)
	neighbors = [[0 for i in range(0, sizes[0])] for j in range(0, sizes[1])]

	for localY in range(y - base, y + base + 1):
		for localX in range(x - base, x + base + 1):
			neighbors[localX - (x - base)][localY - (y - base)] = pixels[localX][localY]
	return neighbors

if len(sys.argv) == 2:

	source_image = Image.open(sys.argv[1])
	source_image_pixels = list(source_image.getdata())


	imageW, imageH = source_image.size
	source_result = [[0 for x in range(0, imageW)] for y in range(0, imageH)]
	
	robert_image = Image.new(source_image.mode, source_image.size, 0)
	robert_result = robert_image.load()
	
	prewitt_image = Image.new(source_image.mode, source_image.size, 0)
	prewitt_result = prewitt_image.load()
	
	sobel_image = Image.new(source_image.mode, source_image.size, 0)
	sobel_result = sobel_image.load()
	
	freichen_image = Image.new(source_image.mode, source_image.size, 0)
	freichen_result = freichen_image.load()

	kirsch_image = Image.new(source_image.mode, source_image.size, 0)
	kirsch_result = kirsch_image.load()

	robinson_image = Image.new(source_image.mode, source_image.size, 0)
	robinson_result = robinson_image.load()

	nevatiababu_image = Image.new(source_image.mode, source_image.size, 0)
	nevatiababu_result = nevatiababu_image.load()

	for y in range(0, imageH):
		for x in range(0, imageW):
			source_result[x][y] = source_image_pixels[y * imageW + x]
	source_extend = extend(source_image.size, [3, 3], source_result)
	source_extend_big = extend(source_image.size, [5, 5], source_result)


	for y in range(0, imageH):
		for x in range(0, imageW):
			startPoint = [x + 1, y + 1]
			robert_result[x, y] = robertDetector(startPoint, source_extend, 12)
			prewitt_result[x, y] = prewittDetector(startPoint, source_extend, 24)
			sobel_result[x, y] = sobelDetector(startPoint, source_extend, 38)
			freichen_result[x, y] = freichenDetector(startPoint, source_extend, 30)
			kirsch_result[x, y] = kirschDetector(startPoint, source_extend, 135)
			robinson_result[x, y] = robinsonDetector(startPoint, source_extend, 43)
			nevatiababu_result[x, y] = nevatiababuDetector([x + 2, y + 2], source_extend_big, 12500)
	robert_image.save("%s/%s.jpg" % (scriptDir, "robert_30"))
	prewitt_image.save("%s/%s.jpg" % (scriptDir, "prewitt_24"))
	sobel_image.save("%s/%s.jpg" % (scriptDir, "sobel_38"))
	freichen_image.save("%s/%s.jpg" % (scriptDir, "freichen_30"))
	kirsch_image.save("%s/%s.jpg" % (scriptDir, "kirsch_135"))
	robinson_image.save("%s/%s.jpg" % (scriptDir, "robinson_43"))
	nevatiababu_image.save("%s/%s.jpg" % (scriptDir, "nevatiababu_12500"))


else:
	print 'please enter the path of source image!'