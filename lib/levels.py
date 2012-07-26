from xml.sax import *
from xml.sax import handler
from xml.sax import saxutils
from xml.sax import make_parser
from xml.sax.handler import feature_namespaces
import pygame
import data

#levels.py - class for opening the map file and parsing the xml into a list of map data

class LevelHandler(ContentHandler):
	def __init__(self, levelname):
		#init handler blah blah wtf
		self.level_name = levelname
		self.level_width = None
		self.level_height = None
		self.level_maxy = None
		self.level_bgimg = None
		self.level_map = None
		self.level_data = False
		self.map_list = []
	def startElement(self,name,attrs):
		#check element blah bleh
		if name == "map":
			levelname = attrs.get('title',"")
			print "Found map object. looking for: "+self.level_name+" . found: "+levelname
			if self.level_name == levelname:
				self.level_maxy = attrs.get('maxy',"")
				self.level_bgimg = attrs.get('background',"")
				self.level_data = True
				self.level_map = Level(levelname, self.level_bgimg, attrs.get('width',""), attrs.get('height',""), attrs.get('maxy',""))
			if self.level_name == "list maps":
				self.map_list.append(levelname)
		if self.level_data != True:
			return;
		if name == "ground":
			print "Ground object found.. adding: "+attrs.get('x',"")+", "+attrs.get('y',"")
			if attrs.get('color',"") != "image":
				self.level_map.addground(attrs.get('x',""),attrs.get('y',""),attrs.get('w',""),attrs.get('h',""),attrs.get('color',""))
			else:
				self.level_map.addground(attrs.get('x',""),attrs.get('y',""),attrs.get('w',""),attrs.get('h',""),attrs.get('color',""),attrs.get('image',""))
		if name == "object":
			self.level_map.addobject(attrs.get('x'),attrs.get('y'),attrs.get('type'))
		
		
	def endElement(self,name):
		if name == "map" and self.level_data == True:
			self.level_data = False
			


class MapLoader:
	def __init__(self,filename):
		self.filename = filename
		self.maps = []
		
	def parseMap(self,mapname):
		parser = make_parser()
		parser.setFeature(feature_namespaces,0)
		lhandle = LevelHandler(mapname)
		parser.setContentHandler(lhandle)
		parser.parse(self.filename)
		if mapname == "list maps":
			return lhandle.map_list
		print lhandle.level_map
		return lhandle.level_map
	
	def parseFile(self):
		parser = make_parser()
		parser.setFeature(feature_namespaces,0)
		lhandle = LevelHandler("list maps")
		parser.setContentHandler(lhandle)
		parser.parse(self.filename)
		print lhandle.map_list
		return lhandle.map_list
		
	def setFile(self, filename):
		self.filename = filename
		
	def newMap(self):
		self.level_map = Level("newlevel1", "bigbackground.jpg", "2008", "771", "770")
		return self.level_map
			
		


class Level:
	def __init__(self,name,bg,w,h,maxy):
		self.bg = data.load_image(bg)
		self.bg_name = bg
		self.w = w
		self.h = h
		self.levelname = name
		self.maxy = maxy
		self.ground = []
		self.groundattr = []
		self.objects = []
		
	def addground(self,x,y,w,h,color,image=None):
		temprect = pygame.Rect(int(x),int(y),int(w),int(h))
		#color="000,000,000"
		if color != "image":
			color1 = int(color[:3])
			color2 = int(color[4:7])
			color3 = int(color[8:11])
			tempattr = [(color1,color2,color3)]
		else:
			if image == None:
				image = "samplebuild.png"
			tempimg = data.load_image(image)
			tempattr = ["image",tempimg,image]
		self.groundattr.append(tempattr)
		self.ground.append(temprect)
		
	def addobject(self,x,y,type):
		tempobj = [x,y,int(type)]
		self.objects.append(tempobj)

	def setBG(self,bg):
		self.bg = data.load_image(bg)
		self.bg_name = bg
		self.bg = self.bg.convert()
		self.w = self.bg.get_width()
		self.h = self.bg.get_height()
		
	def setName(self,name):
		self.levelname = name
		
	def removeLastGround(self):
		#delete last entry in the ground list
		if(len(self.ground) < 1 or len(self.groundattr) < 1):
			return
		self.ground.pop()
		self.groundattr.pop()