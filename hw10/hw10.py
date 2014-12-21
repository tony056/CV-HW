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

def getNeighbors(pixelPosition, pixels, sizes):
	x = pixelPosition[0]
	y = pixelPosition[1]
	base = int(sizes[0] / 2)
	neighbors = [[0 for i in range(0, sizes[0])] for j in range(0, sizes[1])]

	for localY in range(y - base, y + base + 1):
		for localX in range(x - base, x + base + 1):
			neighbors[localX - (x - base)][localY - (y - base)] = pixels[localX][localY]
	return neighbors

def checkNeighbors(position, data, sizes):
	x = position[0]
	y = position[1]
	if data[x][y] == 1:
		neighbors = getNeighbors(position, data, sizes)
		for y in xrange(sizes[1]):
			for x in xrange(sizes[0]):
				if neighbors[x][y] == -1:
					return 0

	return 255 

def laplaceOperating(neighbors, mask, sizes, threshold, alpha):
	ans = 0
	for y in range(0, sizes[1]):
		for x in range(0, sizes[0]):
			ans += (neighbors[x][y] * mask[x][y])
	ans *= alpha		
	if ans > threshold:
		return 1
	elif ans < -threshold:
		return -1
	else:
		return 0

if len(sys.argv) == 2:

	source_image = Image.open(sys.argv[1])
	source_image_pixels = list(source_image.getdata())


	imageW, imageH = source_image.size
	source_result = [[0 for x in range(0, imageW)] for y in range(0, imageH)]

	for y in range(0, imageH):
		for x in range(0, imageW):
			source_result[x][y] = source_image_pixels[y * imageW + x]
	source_extend = extend(source_image.size, [3, 3], source_result)
	source_extend_big = extend(source_image.size, [11, 11], source_result)

	laplacian1_image = Image.new(source_image.mode, source_image.size, 0)
	laplacian1_result = laplacian1_image.load()
	laplacian1_record = [[0 for i in range(0, imageW + 2)] for j in range(0, imageH + 2)]

	laplacian2_image = Image.new(source_image.mode, source_image.size, 0)
	laplacian2_result = laplacian2_image.load()
	laplacian2_record = [[0 for i in range(0, imageW + 2)] for j in range(0, imageH + 2)]

	minimum_var_lap_image = Image.new(source_image.mode, source_image.size, 0)
	minimum_var_lap_result = minimum_var_lap_image.load()
	minimum_var_lap_record = [[0 for i in range(0, imageW + 2)] for j in range(0, imageH + 2)]

	log_image = Image.new(source_image.mode, source_image.size, 0)
	log_result = log_image.load()
	log_record = [[0 for i in range(0, imageW + 10)] for j in range(0, imageH + 10)]

	dog_image = Image.new(source_image.mode, source_image.size, 0)
	dog_result = dog_image.load()
	dog_record = [[0 for i in range(0, imageW + 10)] for j in range(0, imageH + 10)]

	mask1 = [[0, 1, 0], [1, -4, 1], [0, 1, 0]]
	mask2 = [[1, 1, 1], [1, -8, 1], [1, 1, 1]]
	min_mask = [[2, -1, 2], [-1, -4, -1], [2, -1, 2]]
	gaussian_mask = [
		[0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0],
		[0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
		[0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
		[-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
		[-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
		[-2, -9, -23, -1, 103, 178, 103, -1, -23, -9, -2],
		[-1, -8, -22, -14, 52, 103, 52, -14, -22, -8, -1],
		[-1, -4, -15, -24, -14, -1, -14, -24, -15, -4, -1],
		[0, -2, -7, -15, -22, -23, -22, -15, -7, -2, 0],
		[0, 0, -2, -4, -8, -9, -8, -4, -2, 0, 0],
		[0, 0, 0, -1, -1, -2, -1, -1, 0, 0, 0]
	]
	dog_mask = [
		[-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1],
		[-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
		[-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
		[-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
		[-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
		[-8, -13, -17, 15, 160, 283, 160, 15, -17, -13, -8],
		[-7, -13, -17, 0, 85, 160, 85, 0, -17, -13, -7],
		[-6, -11, -16, -16, 0, 15, 0, -16, -16, -11, -6],
		[-4, -8, -12, -16, -17, -17, -17, -16, -12, -8, -4],
		[-3, -5, -8, -11, -13, -13, -13, -11, -8, -5, -3],
		[-1, -3, -4, -6, -7, -8, -7, -6, -4, -3, -1]
	]
	for y in range(1, imageH + 1):
		for x in range(1, imageW + 1):
			center = [x, y]
			# laplacian1_record[x][y] = laplaceOperating(getNeighbors(center, source_extend, [3, 3]), mask1, [3, 3], 15, 1)
			# laplacian2_record[x][y] = laplaceOperating(getNeighbors(center, source_extend, [3, 3]), mask2, [3, 3], 15, 1/3.0)
			# minimum_var_lap_record[x][y] = laplaceOperating(getNeighbors(center, source_extend, [3, 3]), min_mask, [3, 3], 20, 1/3.0)
			# log_record[x + 4][y + 4] = laplaceOperating(getNeighbors([x + 4, y + 4], source_extend_big, [11, 11]), gaussian_mask, [11, 11], 3000, 1)
			dog_record[x + 4][y + 4] = laplaceOperating(getNeighbors([x + 4, y + 4], source_extend_big, [11, 11]), dog_mask, [11, 11], 1, 1)
	for y in range(0, imageH):
		for x in range(0, imageW):
			# laplacian1_result[x, y] = checkNeighbors([x + 1, y + 1], laplacian1_record, [3, 3])
			# laplacian2_result[x, y] = checkNeighbors([x + 1, y + 1], laplacian2_record, [3, 3])
			# minimum_var_lap_result[x, y] = checkNeighbors([x + 1, y + 1], minimum_var_lap_record, [3, 3])
			# log_result[x, y] = checkNeighbors([x + 5, y + 5], log_record, [11, 11])
			dog_result[x, y] = checkNeighbors([x + 5, y + 5], dog_record, [11, 11])

	# laplacian1_image.save("%s/%s.jpg" % (scriptDir, "laplacian_mask1_15"))
	# laplacian1_image.show()

	# laplacian2_image.save("%s/%s.jpg" % (scriptDir, "laplacian_mask2_15"))
	# laplacian2_image.show()

	# minimum_var_lap_image.save("%s/%s.jpg" % (scriptDir, "minimum_variance_20"))
	# minimum_var_lap_image.show()

	# log_image.save("%s/%s.jpg" % (scriptDir, "LOG_3000"))
	# log_image.show()

	dog_image.save("%s/%s.jpg" % (scriptDir, "DOG_1"))
	dog_image.show()
