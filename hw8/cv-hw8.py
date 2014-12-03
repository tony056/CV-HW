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

	gaussianNoisesTen = gaussianNoise(0, 1, 10, [imageW, imageH], source_image_pixels)
	gaussianNoisesThirty = gaussianNoise(0, 1, 30, [imageW, imageH], source_image_pixels)
	saltAndPepperSmall = saltAndPepper(0, 1, 0.05, [imageW, imageH], source_image_pixels)
	saltAndPepperBig = saltAndPepper(0, 1, 0.1, [imageW, imageH], source_image_pixels)

	for y in range(0, imageH):
		for x in range(0, imageW):
			gaussian10_image_result[x, y] = gaussianNoisesTen[x][y]
			gaussian30_image_result[x, y] = gaussianNoisesThirty[x][y]
			saltAndPepperSmall_image_result[x, y] = saltAndPepperSmall[x][y]
			saltAndPepperBig_image_result[x, y] = saltAndPepperBig[x][y]

	gaussian10_image.save("%s/%s.jpg" % (scriptDir, 'gaussian10'))
	gaussian10_image.show()

	gaussian30_image.save("%s/%s.jpg" % (scriptDir, 'gaussian30'))
	gaussian30_image.show()

	saltAndPepperSmall_image.save("%s/%s.jpg" % (scriptDir, 'saltAndPepper_0.05'))
	saltAndPepperSmall_image.show()

	saltAndPepperBig_image.save("%s/%s.jpg" % (scriptDir, 'saltAndPepper_0.1'))
	saltAndPepperBig_image.show()


else:
	print 'please enter the path of source image!'