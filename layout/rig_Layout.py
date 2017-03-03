import maya.cmds as cmds
import system.utils as utils
import os
from collections import OrderedDict
import json

class Layout:
	
	def __init__(self):
		self.rlayout = {}
		self.layoutLog = {}
		self.symmCheckbox = cmds.checkBox('symmBox', q = True, v = True)
		self.layoutPath = os.environ["RDOJO_DATA"] + '/layoutPositions.json'
		

	def importCoord(self, *args):
		importLayout = utils.readJson(self.layoutPath)
		self.rlayout = json.loads(importLayout, object_pairs_hook=OrderedDict)
		print 'Importing Coordinates'

	def createLayout(self):
		self.importCoord(self.layoutPath)
		symmTargets_L = []
		symmTargets_R = []
		keys = self.rlayout.keys()
		


		for k in keys:
			side = k.split('_')
			if side[1] == 'L': 
				symmTargets_L.append(k)
			elif side[1] == 'R':
				symmTargets_R.append(k)

		for key, value in self.rlayout.iteritems():
			for k, val in value.iteritems():
				cmds.joint(n = k, p = val)
			cmds.select(d=True)
		if 	self.symmCheckbox == True:
			counter = 0
			#variables for both keys to store their internal keys#
			for s in symmTargets_L:
				rBones = self.rlayout[symmTargets_R[counter]].keys()
				keyCounter = 0
				for key in self.rlayout[symmTargets_L[counter]].iteritems():
					utils.symmetryConstraint(key[0], rBones[keyCounter])
					keyCounter += 1
					cmds.select(d = True)
				counter += 1
				

		print 'Generating Layout'
