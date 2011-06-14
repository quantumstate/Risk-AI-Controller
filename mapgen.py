import sys
import Image, ImageFilter, ImageDraw, ImageChops
import math, random
import json
pi = math.pi

mapSize = (600,400)
numContinents = 7
contCols = [(255,0,0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255),(188,188,188)]
numCountries = 50

#object to hold the data for a country
class country:
	def __init__(self, centre, color, continent = -1, neighbours = []):
		self.centre = centre
		self.continent = continent
		self.neighbours = []
		self.color = color
		
	def addNeighbour(self, n):
		if self.neighbours.count(n) == 0:
			self.neighbours.append(n)

#break the connection between two countries by removing the numbers from the neighbours list
def breakConnection(countries, i, j):
	countries[i].neighbours.remove(j)
	countries[j].neighbours.remove(i)

#make a list of pixels centred around 0 ina  circle
def circle(radius):
	if radius == 0:
		return [[0,0]]
	points = []
	for i in range(int(2*pi*radius)+1):
		points.append([int(radius * math.cos(i/float(radius))),int(radius * math.sin(i/float(radius)))])
		
	return points

#expand from each point with the corresponding color, drawing the result onto pix.
#each point has a growing circle around it which grows up to the radius.
def expand(points, colors, pix, imSize, radius):
	for i in range(0,radius):
		circ = circle(i/3.0)
		for p in circ:
			for i in range(len(points)):
				q = (points[i][0]+p[0], points[i][1]+p[1])
				if 0 <= q[0] < imSize[0] and 0 <= q[1] < imSize[1]:
					if pix[q[0],q[1]] == (0,0,0):
						pix[q[0],q[1]] = colors[i]

#has the continents drawn on
im = Image.new("RGB", mapSize, "black")
pix = im.load()
#has the countries drawn on
imC = Image.new("RGB", mapSize, "black")
pixC = imC.load()
drawC = ImageDraw.Draw(imC)
#has the borders between countries temporarily stored here
borders = Image.new("RGB", mapSize, "black")
pixB = borders.load()


#pick random continent centres
continentPoints = []
for i in range(numContinents):
	continentPoints.append([random.randint(0,mapSize[0]-1), random.randint(0,mapSize[1]-1)])

expand(continentPoints, contCols, pix, mapSize, mapSize[0])


#randomly pick the country centres
countries = []
countryPoints = []
countryColors = []

for i in range(numCountries):
	p = [random.randint(0,mapSize[0]-1), random.randint(0,mapSize[1]-1)]
	#check the point lies within a continent
	if pix[p[0],p[1]] != (0,0,0):
		countryPoints.append(p)
		#pick a unique color (a deviation from the continent color)
		while True:
			r1 = random.random()*0.7 + 0.3
			col = (int(255-r1*(255-pix[p[0],p[1]][0])),int(255-r1*(255-pix[p[0],p[1]][1])),int(255-r1*(255-pix[p[0],p[1]][2])))
			if countryColors.count(col) == 0:
				break

		countryColors.append(col)
		countries.append(country(p, col, contCols.index(pix[p[0],p[1]])))

expand(countryPoints, countryColors, pixC, mapSize, mapSize[0]/2)

#make a dictionary which can convert a color to a country efficiently
colCountry = {}
for i in range(len(countries)):
	colCountry[countries[i].color] = i

#scan the picture lookat at borders between different colors (countries)
for x in range(mapSize[0]-1):
	for y in range(mapSize[1]-1):
		#check if adjacent pixels have different colors
		if pixC[x,y] != pixC[x,y+1] or pixC[x,y] != pixC[x+1,y]:
			#store the borders in a separate picture to be drawn on later
			pixB[x,y] = (255,255,255)
			#store the connections between countries
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

#list the countries in each continent
continents = []
for i in range(numContinents):
	a = []
	for j in range(len(countries)):
		if countries[j].continent == i:
			a.append(j)
	continents.append(a)

#remove links between continents
for i in range(numContinents):
	for j in range(i+1, numContinents):
		connections = [] # list of connections between continent i and continent j
		#generate the list of connections
		for k in continents[i]: 
			for l in countries[k].neighbours:
				if continents[j].count(l) != 0:
					connections.append((l,k))
		
		if len(connections) > 1:
			#randomly pick some connections to remove (always leaving at least 1)
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

#im.save("map.png")
imC.save("map.png")

countriesJson = []
for country in countries:
	countriesJson.append({'centre':country.centre,
	                      'continent':country.continent,
	                      'neighbours':country.neighbours,
	                      'color':country.color})

mapObj = {"image":"map.png",
          "countries":countriesJson}
#print json.dumps(mapObj)
f = open('map.json', 'w')
json.dump(mapObj, f)
