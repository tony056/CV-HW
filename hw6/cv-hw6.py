from PIL import Image
import sys, os
scriptDir = os.path.dirname(os.path.realpath(__file__))

def binarize(pixels, width):
	result = [[0 for x in range(0, width)] for y in range(0, width)]
	for i in range(0, len(pixels)):
		if pixels[i] < 128:
			result[i % width][i / width] = 0
		else:
			result[i % width][i / width] = 255
	return result

def downSample(pixels, width, height, unitWidth, unitHeight, samplePointX, samplePointY):
	result = [[0 for x in range(0, width / unitWidth)] for y in range(0, height / unitHeight)]
	for x in range(0, width / unitWidth):
		for y in range(0, height / unitHeight):
			result[x][y] = pixels[x * unitWidth + samplePointX][y * unitHeight + samplePointY]
	return result

def yokoi(pixels, size):
	result = [[' ' for x in range(0, size[0])] for y in range(0, size[1])]
	for x in range(0, size[0]):
		for y in range(0, size[1]):
			if pixels[x][y] == 255:
				neighbors = [[-1, -1, -1],
							 [-1, pixels[x][y], -1],
							 [-1, -1, -1]]
				if x + 1 < size[0]:
					if y - 1 >= 0:
						neighbors[2][0] = pixels[x + 1][y - 1]
					if y + 1 < size[1]:
						neighbors[2][2] = pixels[x + 1][y + 1]
					neighbors[2][1] = pixels[x + 1][y]
				if x - 1 >= 0:
					neighbors[0][1] = pixels[x - 1][y]
					if y - 1 >= 0:
						neighbors[0][0] = pixels[x - 1][y - 1]
					if y + 1 < size[1]:
						neighbors[0][2] = pixels[x - 1][y + 1]
				if y - 1 >= 0:
					neighbors[1][0] = pixels[x][y - 1]
				if y + 1 < size[1]:
					neighbors[1][2] = pixels[x][y + 1]

				a1 = hFunction(neighbors[1][1], neighbors[2][1], neighbors[2][0], neighbors[1][0])
				a2 = hFunction(neighbors[1][1], neighbors[1][0], neighbors[0][0], neighbors[0][1])
				a3 = hFunction(neighbors[1][1], neighbors[0][1], neighbors[0][2], neighbors[1][2])
				a4 = hFunction(neighbors[1][1], neighbors[1][2], neighbors[2][2], neighbors[2][1])

				num = fFunction(a1, a2, a3, a4)
				if num != 0:
					result[x][y] = str(num)
			else:
				result[x][y] = ' '
	return result

def hFunction(b, c, d, e):
	# q: 0, r: 1, s: 2
	if b == c:
		if b == d and b == e:
			return 1
		else:
			return 0
	else:
		return 2

def fFunction(a, b, c, d):
	print str(a) + ', ' + str(b) + ', ' + str(c) + ', ' + str(d)
	if a == 1:
		if b == 1 and c == 1 and d == 1:
			return 5
		else:
			return calculate([b, c, d])
	else:
		return calculate([a, b, c, d])

def calculate(data):
	num = 0
	for d in data:
		if d == 0:
			num += 1
	return num



if len(sys.argv) == 2:
	source_image = Image.open(sys.argv[1])
	source_image_pixels = list(source_image.getdata())

	binary_image_pixels = binarize(source_image_pixels, source_image.size[0])
	binary_image = Image.new(source_image.mode, source_image.size, 0)
	binary_image_result = binary_image.load()

	downSample_size = [64, 64]
	downSample_image = Image.new(source_image.mode, downSample_size, 0)
	downSample_image_pixels = downSample(binary_image_pixels, source_image.size[0], source_image.size[1], 8, 8, 0, 0)
	downSample_image_result = downSample_image.load()

	yokoi_pixels = yokoi(downSample_image_pixels, downSample_size)
	result_file = open('yokoi.txt', 'w')

	for x in range(0, downSample_size[0]):
		for y in range(0, downSample_size[1]):
			result_file.write(yokoi_pixels[y][x])
		result_file.write('\n')
	result_file.close()

else:
	print 'please enter the path of source image!'