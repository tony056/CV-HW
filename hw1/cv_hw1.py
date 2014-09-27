from PIL import Image
import sys, os
scriptDir = os.path.dirname(os.path.realpath(__file__)) + '/bin'

if len(sys.argv) == 2:
	im = Image.open(sys.argv[1])
	upsideDownImage = Image.new(im.mode, im.size, 0)
	upsideDownPixels = upsideDownImage.load()
	rightsideLeftImage = Image.new(im.mode, im.size, 0)
	rightsideLeftPixels = rightsideLeftImage.load()
	diagonallyImage = Image.new(im.mode, im.size, 0)
	diagonallyPixels = diagonallyImage.load()

	imageW, imageH = im.size
	pixels = list(im.getdata())
	im.show()

	for y in range(0, imageH):
		for x in range(0, imageW):
			pixel = pixels[x + imageW * y]
			upsideDownPixels[x, imageH - 1 - y] = pixel
			rightsideLeftPixels[imageW - 1 - x, y] = pixel
			diagonallyPixels[y, x] = pixel
	upsideDownImage.save("%s/updown.jpg" % scriptDir)
	rightsideLeftImage.save("%s/rightleft.jpg" % scriptDir)
	diagonallyImage.save("%s/diagonally.jpg" % scriptDir)
	upsideDownImage.show()
	rightsideLeftImage.show()
	diagonallyImage.show()
else:
	print "please enter the absolute path of the source picture as arg1"