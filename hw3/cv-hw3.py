from PIL import Image
import sys, os
scriptDir = os.path.dirname(os.path.realpath(__file__))

if len(sys.argv) == 2:
	source_image = Image.open(sys.argv[1])
	histogramEq_image = Image.new(source_image.mode, source_image.size, 0)
	histogramEq_image_pixels = histogramEq_image.load()

	imageW, imageH = source_image.size
	source_image_pixels = list(source_image.getdata())

	histogram = [0 for x in xrange(256)]
	cdf = {}
	for x in source_image_pixels:
		histogram[x] += 1
	for i in range(0, 256):
		if histogram[i] != 0:
			cdf[i] = histogram[i]
	for i in range(0, len(cdf)):
		if i != 0:
			cdf[cdf.keys()[i]] += cdf[cdf.keys()[i - 1]]
	# print cdf	
	for y in xrange(imageH):
		for x in xrange(imageW):
			histogramEq_image_pixels[x, y] = int((cdf[source_image_pixels[x + y * imageW]]) / float((imageW * imageH)) * 255)
			# print cdf[source_image_pixels[x + y * imageW]]
	histogramEq_image.save("%s/histogram_equalization.jpg" % scriptDir)
	histogramEq_image.show()
	source_image.show()
else:
	print 'please enter the path of source image!'
