from PIL import Image
import sys, os, csv
scriptDir = os.path.dirname(os.path.realpath(__file__))

if len(sys.argv) is 2:
	source = Image.open(sys.argv[1])
	binaryImage = Image.new(source.mode, source.size, 0)
	imageH, imageW = source.size
	binaryPixels = binaryImage.load()
	pixels = list(source.getdata())
	histogram = [0 for x in xrange(255)]

	for i in xrange(imageH):
		for j in xrange(imageW):
			value = pixels[j + imageW * i]
			if value < 128:
				binaryPixels[j, i] = 0
			elif value >= 128 and value < 255:
				binaryPixels[j, i] = 255
	binaryImage.save("%s/binarize.jpg" % scriptDir)

	for x in pixels:
		histogram[x] += 1
	csvFile = open('%s/hw2.csv' % scriptDir, "w")
	w = csv.writer(csvFile)
	w.writerow(histogram)
	csvFile.close()

	components = [[0 for x in xrange(imageW)] for y in xrange(imageH)]
	classes = 0
	for y in xrange(imageH):
		for x in xrange(imageW):
			if binaryPixels[x, y] is not 0:

				if components[x][y] == 0:
					classes += 1
					components[x][y] = classes
				if x + 1 < imageW:
					if binaryPixels[x, y] == binaryPixels[x + 1, y]:
						components[x + 1][y] = components[x][y]
				elif y + 1 < imageH:
					if binaryPixels[x, y] == binaryPixels[x, y + 1]:
						components[x][y + 1] = components[x][y]
			print components[x][y],
			binaryPixels[x, y] = components[x][y]
		print 
	binaryImage.save("%s/connect.jpg" % scriptDir)




else:
	print "please  enter the path of the source image!"