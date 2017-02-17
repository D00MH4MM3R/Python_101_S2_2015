import maya.cmds as cmds
import system.utils as utils
import json

class Layout:
	
	def __init__(self):
		self.rlayout = {}
		self.layoutPath = 'C:/Users/Mauricio Pachon/Documents/GitHub/Python_101_S2_2015/layout/layoutPositions.json'
		

	def importCoord(self, *args):
		importLayout = utils.readJson(self.layoutPath)
		self.rlayout = json.loads(importLayout)
		print 'Importing Coordinates'

	def createLayout(self):
		self.importCoord(self.layoutPath)

		for key, value in self.rlayout.iteritems():
			currentLoc = cmds.spaceLocator(n = key)
			cmds.xform(currentLoc, t = value)

		print 'Generating Layout'
