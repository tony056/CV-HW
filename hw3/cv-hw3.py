from PIL import Image
import sys, os, csv
scriptDir = os.path.dirname(os.path.realpath(__file__))

if len(sys.argv) == 2:
	source_image = Image.open(sys.argv[1])
	histogramEq_image = Image.new(source_image.mode, source_image.size, 0)
	histogramEq_image_pixels = histogramEq_image.load()

	imageW, imageH = source_image.size
	source_image_pixels = list(source_image.getdata())

	histogram = [0 for x in xrange(256)]
	new_histogram = [0 for x in xrange(256)]
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
	num = 0
	for y in xrange(imageH):
		for x in xrange(imageW):
			value = int((cdf[source_image_pixels[x + y * imageW]]) / float((imageW * imageH)) * 255)
			histogramEq_image_pixels[x, y] = value
			new_histogram[value] += 1
			# print cdf[source_image_pixels[x + y * imageW]]
	histogramEq_image.save("%s/histogram_equalization.jpg" % scriptDir)
	histogramEq_image.show()
	source_image.show()

	oldcsvFile = open('%s/original_histogram.csv' % scriptDir, 'w')
	csvFile = open('%s/new_histogram.csv' % scriptDir, 'w')
	oldw = csv.writer(oldcsvFile)
	oldw.writerow(histogram)
	# w = csv.writer(csvFile)
	# w.writerow(new_histogram)
	for val in new_histogram:
		csvFile.write(str(val) + '\n')
	oldcsvFile.close()
	csvFile.close()
else:
	print 'please enter the path of source image!'
