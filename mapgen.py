import sys
import Image, ImageFilter, ImageDraw, ImageChops
import math, random
pi = math.pi

mapSize = (600,400)
numContinents = 7
contCols = [(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255),(188,188,188)]
numCountries = 50

class country:
	def __init__(self, centre, color, continent = -1, neighbours = []):
		self.centre = centre
		self.continent = continent
		self.neighbours = []
		self.color = color
		
	def addNeighbour(self, n):
		if self.neighbours.count(n) == 0:
			self.neighbours.append(n)
			
def breakConnection(countries, i, j):
	countries[i].neighbours.remove(j)
	countries[j].neighbours.remove(i)

def circle(radius):
	if radius == 0:
		return [[0,0]]
	points = []
	for i in range(int(2*pi*radius)+1):
		points.append([int(radius * math.cos(i/float(radius))),int(radius * math.sin(i/float(radius)))])
		
	return points

def expand(points, colors, pix, imSize, radius):
	for i in range(0,radius):
		circ = circle(i/3.0)
		for p in circ:
			for i in range(len(points)):
				q = (points[i][0]+p[0], points[i][1]+p[1])
				if 0 <= q[0] < imSize[0] and 0 <= q[1] < imSize[1]:
					if pix[q[0],q[1]] == (0,0,0):
						pix[q[0],q[1]] = colors[i]


im = Image.new("RGB", mapSize, "black")
pix = im.load()
imC = Image.new("RGB", mapSize, "black")
pixC = imC.load()
drawC = ImageDraw.Draw(imC)
borders = Image.new("RGB", mapSize, "black")
pixB = borders.load()


#pick random continent centres
continentPoints = []

for i in range(numContinents):
	continentPoints.append([random.randint(0,mapSize[0]-1), random.randint(0,mapSize[1]-1)])

expand(continentPoints, contCols, pix, mapSize, mapSize[0])


countries = []
countryPoints = []
countryColors = []

for i in range(numCountries):
	p = [random.randint(0,mapSize[0]-1), random.randint(0,mapSize[1]-1)]
	if pix[p[0],p[1]] != (0,0,0):
		countryPoints.append(p)
		while True:
			r1 = random.random()*0.7 + 0.3
			col = (int(255-r1*(255-pix[p[0],p[1]][0])),int(255-r1*(255-pix[p[0],p[1]][1])),int(255-r1*(255-pix[p[0],p[1]][2])))
			if countryColors.count(col) == 0:
				break

		countryColors.append(col)
		countries.append(country(p, col, contCols.index(pix[p[0],p[1]])))
		
expand(countryPoints, countryColors, pixC, mapSize, mapSize[0]/2)

colCountry = {}
for i in range(len(countries)):
	colCountry[countries[i].color] = i

for x in range(mapSize[0]-1):
	for y in range(mapSize[1]-1):
		if pixC[x,y] != pixC[x,y+1] or pixC[x,y] != pixC[x+1,y]:
			#store the borders in a separate picture to be drawn on later
			pixB[x,y] = (255,255,255)
			#store the connection between countries
			if pixC[x,y] != (0,0,0) and pixC[x+1,y] != (0,0,0) and pixC[x,y+1] != (0,0,0):
				c1 = colCountry[pixC[x,y]]
				c2 = colCountry[pixC[x+1,y]]
				c3 = colCountry[pixC[x,y+1]]
				if c1 != c2:
					countries[c1].addNeighbour(c2)
					countries[c2].addNeighbour(c1)
				if c1 != c3 and c3 != c2:
					countries[c1].addNeighbour(c3)
					countries[c3].addNeighbour(c1)

continents = []
for i in range(numContinents):
	a = []
	for j in range(len(countries)):
		if countries[j].continent == i:
			a.append(j)
	continents.append(a)

for i in range(numContinents):
	for j in range(i+1, numContinents):
		connections = []
		for k in continents[i]:
			for l in countries[k].neighbours:
				if continents[j].count(l) != 0:
					connections.append((l,k))
		if len(connections) > 1:
			deletions = random.sample(connections, random.randint(0, len(connections)-1))
			for d in deletions:
				breakConnection(countries, d[0],d[1])

#draw on the white borders worked out earlier
for x in range(mapSize[0]):
	for y in range(mapSize[1]):
		if pixB[x,y] == (255,255,255):
			pixC[x,y] = (255,255,255)

#draw lines between connected countries
for country in countries:
	for i in country.neighbours:
		drawC.line([country.centre[0],country.centre[1], countries[i].centre[0],countries[i].centre[1]], fill=(0,0,0))

im.save("map.png")
imC.save("mapC.png")
