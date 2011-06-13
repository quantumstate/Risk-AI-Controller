import sys
import Image, ImageFilter, ImageDraw, ImageChops
import math, random
pi = math.pi

mapSize = (600,400)
numContinents = 7
numContinents = 50

def circle(radius):
	if radius == 0:
		return [[0,0]]
	points = []
	for i in range(int(2*pi*radius)+1):
		points.append([int(radius * math.cos(i/float(radius))),int(radius * math.sin(i/float(radius)))])
		
	return points

def expand(points, colors, pix, imSize):
	for i in range(0,imSize[0]):
		circ = circle(i/3.0)
		for p in circ:
			for i in range(len(points)):
				q = (points[i][0]+p[0], points[i][1]+p[1])
				if 0 <= q[0] < imSize[0] and 0 <= q[1] < imSize[1]:
					if pix[q[0],q[1]] == (0,0,0):
						pix[q[0],q[1]] = colors[i]


im = Image.new("RGB", mapSize, "black")
pix = im.load()

#pick random continent centres
continents = []
contCols = [(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255),(188,188,188)]
for i in range(numContinents):
	continents.append([random.randint(0,mapSize[0]-1), random.randint(0,mapSize[1]-1)])

expand(continents, contCols, pix, mapSize)


countries = []

for i in range(numCountries):
	countries.append([random.randint(0,mapSize[0]-1), random.randint(0,mapSize[1]-1)])

im.save("map.png")
