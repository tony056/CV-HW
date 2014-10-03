from PIL import Image
import sys, os, csv
scriptDir = os.path.dirname(os.path.realpath(__file__))

class Point(object):
	def __init__(self, x, y, val):
		self.x = x
		self.y = y
		self.val = val
	def setClass(self, val):
		self.val = val
	def getClass(self):
		return self.val
	def getPosition(self):
		return self.x, self.y

if len(sys.argv) is 2:
	source = Image.open(sys.argv[1])
	binaryImage = Image.new(source.mode, source.size, 0)
	connectImage = Image.new('RGB', source.size, 0)
	conected = connectImage.load()
	imageH, imageW = source.size
	binaryPixels = binaryImage.load()
	pixels = list(source.getdata())
	histogram = [0 for x in xrange(255)]

	for i in xrange(imageH):
		for j in xrange(imageW):
			value = pixels[j + imageW * i]
			if value < 128:
				binaryPixels[j, i] = 0
			elif value >= 128 and value <= 255:
				binaryPixels[j, i] = 255
	binaryImage.save("%s/binarize.jpg" % scriptDir)

	for x in pixels:
		histogram[x] += 1
	csvFile = open('%s/hw2.csv' % scriptDir, "w")
	w = csv.writer(csvFile)
	w.writerow(histogram)
	csvFile.close()
	pts = []
	components = [[-1 for x in xrange(imageW)] for y in xrange(imageH)]
	classes = 0
	for y in xrange(imageH):
		for x in xrange(imageW):
			#print 'u'
			if binaryPixels[x, y] is not 0:
				if x - 1 >= 0 and binaryPixels[x, y] == binaryPixels[x - 1, y]:
					components[x][y] = components[x - 1][y]
				elif y - 1 >= 0 and binaryPixels[x, y] == binaryPixels[x, y - 1]: 
					components[x][y] = components[x][y - 1]
				else:
					classes += 1
					components[x][y] = classes
							#print components[classes]
	num = [[] for x in xrange(classes + 1)]
	adjacement = [[] for x in xrange(classes + 1)]
	for y in xrange(imageH):
		for x in xrange(imageW):
			if components[x][y] > 0:
				num[components[x][y]].append(Point(x, y, components[x][y]))
				# conected[x, y] = 0
			# else:
			# 	conected[x, y] = (255, 255, 255)
	for index in xrange(len(num)):
		for element in num[index]:
			posx, posy = element.getPosition()
			if posy + 1 < imageH:
				if components[posx][posy + 1] > 0 and components[posx][posy + 1] != element.getClass():
					# print 'judge' + str(components[posx][posy - 1] in adjacement[index])
					if components[posx][posy + 1] not in adjacement[index] and index not in adjacement[components[posx][posy + 1]]:
						adjacement[index].append(components[posx][posy + 1])
						
			if posx - 1 >= 0:
				if components[posx - 1][posy] > 0 and components[posx - 1][posy] != element.getClass():
					# print 'judge' + str(components[posx][posy - 1] in adjacement[index])
					if components[posx - 1][posy] not in adjacement[index] and index not in adjacement[components[posx - 1][posy]]:
						adjacement[index].append(components[posx - 1][posy])
						
			if posx + 1 < imageW:
				if components[posx + 1][posy] > 0 and components[posx + 1][posy] != element.getClass():
					# print 'judge' + str(components[posx][posy - 1] in adjacement[index])
					if components[posx + 1][posy] not in adjacement[index] and index not in adjacement[components[posx + 1][posy]]:
						adjacement[index].append(components[posx + 1][posy])
			if posy - 1 >= 0:
				if components[posx][posy - 1] > 0 and components[posx][posy - 1] != element.getClass():
					# print 'judge' + str(components[posx][posy - 1] in adjacement[index])
					if components[posx][posy - 1] not in adjacement[index] and index not in adjacement[components[posx][posy - 1]]:
						adjacement[index].append(components[posx][posy - 1])
	for index in xrange(len(adjacement) - 1, -1, -1):
		if len(adjacement[index]) > 0:
			for i in xrange(len(adjacement[index]) - 1, -1, -1):
				num[index].extend(num[adjacement[index][i]])
				num[adjacement[index][i]] = []
				for j in xrange(0, index):
					if adjacement[index][i] in adjacement[j]:
						adjacement[j][adjacement[j].index(adjacement[index][i])] = index
	total = 0
	for x in num:
	 	if len(x) >= 500:
	 		total += 1
			x1 = imageW
			y1 = imageH
			x2 = 0 
			y2 = 0
			for point in x:
			 	posx, posy = point.getPosition()
			 	if posx < x1:
			 		x1 = posx
			 	if posx > x2:
			 		x2 = posx
			 	if posy < y1:
			 		y1 = posy
			 	if posy > y2:
			 		y2 = posy
			print 'x1: ' + str(x1) + 'x2: ' + str(x2) + 'y1: ' + str(y1) + 'y2: ' + str(y2)
			midx = int((x1 + x2) / 2)
			midy = int((y1 + y2) / 2)
			for i in xrange(x1, x2 + 1):
				for j in xrange(y1, y2 + 1):
					if i < (midx + 11) and i >= (midx - 10):
						if j < (midy + 5) and j > (midy - 5):
							conected[i, j] = (255, 0, 0)
						if i < (midx + 5) and i > (midx - 5):
							if j < (midy + 11) and j >= (midy - 10):
								conected[i, j] = (255, 0, 0)
					else:
						if binaryPixels[i, j] == 255:
							conected[i, j] = (0, 0, 0) 
						elif binaryPixels[i, j] == 0:
							conected[i, j] = (255, 255, 255) 
	print 'total: ' + str(total)
	connectImage.save("%s/connect12.jpg" % scriptDir)

else:
	print "please  enter the path of the source image!"