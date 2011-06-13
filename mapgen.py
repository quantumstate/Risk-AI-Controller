import sys
import Image, ImageFilter, ImageDraw, ImageChops
import math, random
pi = math.pi

mapSize = (600,400)
numContinents = 7

def circle(radius):
	points = []
	for i in range(int(6*pi*radius)):
		points.append([int(radius * math.cos(i/(6*pi))),int(radius * math.sin(i/(6*pi)))])
		
	return points

def expand(points, colors, pix):
	mindist_2 = 0
	#for i in range(len(points)):
		#for j in range(i+1, len(points)):
	for i in range(0,600):
		circle = circle	


im = Image.new("RGB", mapSize, "black")
pix = im.load()

#pick random continent centres
continents = []
contCols = [(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255),(188,188,188)]
for i in range(numContinents):
	continents.append([random.randint(0,mapSize[0]-1), random.randint(0,mapSize[1]-1)])

i = 0
for p in continents:
	pix[p[0],p[1]] = contCols[i]
	i += 1



#circle fill test
#for r in range(200):
#	circ = circle(r/2.0)
#	for p in circ:
#		pix[150+p[0],150+p[1]] = (255,255,255)
print circle(0)
print circle(1)

im.save("map.png")
