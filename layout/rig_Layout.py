import maya.cmds as cmds
import system.utils as utils
import os
from collections import OrderedDict
import json

class Layout:
	
	def __init__(self):
		self.rlayout = {}
		self.layoutPath = os.environ["RDOJO_DATA"] + 'layout/layoutPositions.json'
		

	def importCoord(self, *args):
		importLayout = utils.readJson(self.layoutPath)
		self.rlayout = json.loads(importLayout, object_pairs_hook=OrderedDict)
		print 'Importing Coordinates'

	def createLayout(self):
		self.importCoord(self.layoutPath)
		for key, value in self.rlayout.iteritems():
			currentJnt = cmds.joint(n = key, p = value)
		cmds.select(d=True)


		print 'Generating Layout'
	
