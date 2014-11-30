from PIL import Image
import sys, os
scriptDir = os.path.dirname(os.path.realpath(__file__))

def binarize(pixels, width, height):
	result = [[0 for x in range(0, width)] for y in range(0, height)]
	for i in range(0, len(pixels)):
		if pixels[i] < 128:
			result[i % width][i / height] = 0
		else:
			result[i % width][i / height] = 1
	return result

def partA(pixels,sizes):
	change = False
	record = []
	for x in range(1, sizes[0] + 1):
		for y in range(1, sizes[1] + 1):
			if pixels[x][y] == 1:
				neighborNum = getNeighborNum(pixels, x, y)
				if neighborNum >= 2 and neighborNum <= 6:
					if adjacentNum(pixels, x, y) == 1:
						if pixels[x - 1][y] * pixels[x][y + 1] * pixels[x + 1][y] == 0:
							if pixels[x][y + 1] * pixels[x + 1][y] * pixels[x][y - 1] == 0:
								record.append([x, y])
								change = True
	if len(record) > 0:
		for i in record:
			pixels[i[0]][i[1]] = 0
		del record[:]
	return change

def partB(pixels, sizes):
	change = False
	record = []
	for x in range(1, sizes[0] + 1):
		for y in range(1, sizes[1] + 1):
			if pixels[x][y] == 1:
				neighborNum = getNeighborNum(pixels, x, y)
				if neighborNum >= 2 and neighborNum <= 6:
					if adjacentNum(pixels, x, y) == 1:
						if pixels[x - 1][y] * pixels[x][y + 1] * pixels[x][y - 1] == 0:
							if pixels[x - 1][y] * pixels[x + 1][y] * pixels[x][y - 1] == 0:
								record.append([x, y])
								change = True
	if len(record) > 0:
		for i in record:
			pixels[i[0]][i[1]] = 0
		del record[:]
	return change

def getNeighborNum(pixels, x, y):
	num = 0
	for localX in range(x - 1, x + 2):
		for localY in range(y - 1, y + 2):
			num += pixels[localX][localY]
	
	return num - pixels[x][y]

def adjacentNum(pixels, x, y):
	local = []
	num = 0
	local.append(pixels[x - 1][y])
	local.append(pixels[x - 1][y + 1])
	local.append(pixels[x][y + 1])
	local.append(pixels[x + 1][y + 1])
	local.append(pixels[x + 1][y])	
	local.append(pixels[x + 1][y - 1])
	local.append(pixels[x][y - 1])
	local.append(pixels[x - 1][y - 1])
	local.append(pixels[x - 1][y])
	for i in range(0, len(local)):
		if i + 1 < len(local):
			if local[i] - local[i + 1] == -1:
				num += 1
	return num




if len(sys.argv) == 2:
	source_image = Image.open(sys.argv[1])
	source_image_pixels = list(source_image.getdata())

	binary_image_pixels = binarize(source_image_pixels, source_image.size[0], source_image.size[1])
	extend_image_pixels = [[0 for x in range(0, source_image.size[0] + 2)] for y in range(0, source_image.size[1] + 2)]
	for x in range(1, source_image.size[0] + 1):
		for y in range(1, source_image.size[1] + 1):
			extend_image_pixels[x][y] = binary_image_pixels[x - 1][y - 1]

	state = False

	while 1:
		state = partA(extend_image_pixels, source_image.size)
		state = partB(extend_image_pixels, source_image.size)
		if state == False:
			break
	


	binary_image = Image.new(source_image.mode, source_image.size, 0)
	binary_image_result = binary_image.load()

	for x in range(0, source_image.size[0]):
		for y in range(0, source_image.size[1]):
			binary_image_result[x, y] = extend_image_pixels[x + 1][y + 1] * 255

	binary_image.save("%s/%s.jpg" % (scriptDir, 'thinning'))
	binary_image.show()


else:
	print 'please enter the path of source image!'
