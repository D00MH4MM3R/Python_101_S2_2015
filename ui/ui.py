import pymel.core as pm 
import system.data_prep as dp
reload(dp)
import system.utils as utils
from functools import partial
import json
import os

class RDojo_UI:

	def __init__(self, *args):
		print 'In RDojo_UI...'

		mwin = pm.window('MayaWindow', menuArray=True, query=True)
		for m in mwin:
			if m == 'RDojo_Menu':
				pm.deleteUI('RDojo_Menu', menu=True)

		mymenu = pm.menu('RDojo_Menu', label='RDMenu', tearOff=True, parent='MayaWindow')
		pm.menuItem(label='Rig Tool', parent=mymenu, command=self.ui)

		# dictionary to hold UI elements
		self.uiElements = {}

		# variables for error message
		self.windowName = "Window"
		self.msg = ''
		self.view = False

		# dictionary for combo boxes
		self.dictCombo = {'bodyPart':'', 'bodySide':'', 'rigType':''}

		dp.loadData()


	def ui(self, *args):
		# check if UI already exists
		if pm.window(self.windowName, exists=True):
			pm.deleteUI(self.windowName)

		# set up window and button size
		windowWidth = 245
		windowHeight = 135
		listWidth = 75
		listHeight = 25
		buttonWidth = 100
		buttonHeight = 30

		self.uiElements['window'] = pm.window(self.windowName, width=windowWidth, height=windowHeight, title='RDojo_UI', sizeable=False)

		# create ui layouts
		#self.uiElements['mainColLayout'] = pm.columnLayout(width=windowWidth, backgroundColor=(.5, .5, .5))
		#self.uiElements['guiFrameLayout'] = pm.frameLayout(label='Layout', borderStyle='in', backgroundColor=(.5, .5, .5), parent=self.uiElements['mainColLayout'])
		self.uiElements['guiFrameLayout'] = pm.frameLayout(label='Layout', borderStyle='in', backgroundColor=(.5, .5, .5), width=windowWidth)
		self.uiElements['guiLabelLayout'] = pm.rowLayout(numberOfColumns=3, columnWidth3=(80, 75, 80), columnAlign=[(1, 'center'), (2, 'center'), (3, 'center')], 
			columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)], height=listHeight, parent=self.uiElements['guiFrameLayout'])
		self.uiElements['guiComboLayout'] = pm.rowLayout(numberOfColumns=3, columnWidth3=(listWidth, listWidth, listWidth), columnAttach=[(1, 'both', 2), (2, 'both', 2), (3, 'both', 2)], 
			parent=self.uiElements['guiFrameLayout'])
		self.uiElements['guiButtonLayout'] = pm.rowLayout(numberOfColumns=1, width=windowWidth, parent=self.uiElements['guiFrameLayout'])

		# create comboboxes and button
		self.createComboBox(listWidth, listHeight)

		self.uiElements['rigButton'] = pm.button(label='Create Rig', width=windowWidth, height=buttonHeight, backgroundColor=(.1, .2, .1), parent=self.uiElements['guiButtonLayout'], 
			command=self.rigarm)

		# show window
		pm.showWindow(self.windowName)
		

	def createComboBox(self, lWidth, lHeight):
		# load the menu file to create comboboxes
		fileName = os.environ['DATA_PATH'] + 'menuData.json'
		menuInfo = json.loads(utils.readJson(fileName))	 
		print 'starting combo box'
		print 'menu info = ', menuInfo

		for dictItem in menuInfo:
			print 'dict item = ', dictItem
			# itemValues is the values for the key specified in dictItem
			itemValues = menuInfo.get(dictItem)

			#for i in itemValues:
			pos = [ndx for ndx, char in enumerate(dictItem) if char.isupper()]
			labelName = dictItem[0:pos[0]].capitalize()+" "+dictItem[pos[0]:len(dictItem)]
	
			self.uiElements['comboLabel'] = pm.text(label=labelName, font='boldLabelFont', width=lWidth, height=lHeight, parent=self.uiElements['guiLabelLayout'])
			self.uiElements[dictItem] = pm.optionMenu(width=lWidth, height=lHeight, backgroundColor=(.5, .5, .5), parent=self.uiElements['guiComboLayout'], 
				changeCommand=partial(self.item_changed, dictItem))

			print itemValues
			iv = type(itemValues)
			print 'iv type = ', iv
			print 'len = ', len(itemValues)
			print ''
			#for di in itemValues:
			for di in range(len(itemValues)):
				print 'di for loop = ', di
				print ''
				if isinstance(itemValues[di], dict):
					print 'this should be a dictionary'
					print 'dict di = ', itemValues[di]
					print ''
					key = itemValues[di].keys()[0]
					pm.menuItem(label=key, parent=self.uiElements[dictItem])
           		else:
           			print 'this is something else'
           			t = type(di)
           			print 'other di = ', itemValues[di]
           			print 'type = ', t
           			print ''
           			if isinstance(itemValues[di], dict):
           				print 'ignore'
           			else:
           				pm.menuItem(label=itemValues[di], parent=self.uiElements[dictItem])
				
	
	def item_changed(self, itemName, *args):
		val = pm.optionMenu(self.uiElements[itemName], query=True, value=True)
		if val == ' ':
			self.displayErrMsg(itemName)
		else:
			self.dictCombo[itemName] = val


	def rigarm(self, *args):
		import rig.rig_arm as ra
		reload(ra)	

		emptyDictValues = bool([item for item in self.dictCombo.itervalues() if item == ''])
		if emptyDictValues:
			self.displayErrMsg('empty')
		else:
			arm = ra.RigArm()
			arm.initializeEverything(self.dictCombo)


	def displayErrMsg(self, itemName):
		# this generates a dialog box with the appropriate error message
		if itemName == 'empty':
			msg = 'Please make sure all items have been selected.'
		else:
			msg = itemName + ' cannot be blank.'

		pm.confirmDialog(title='Error Message', message=msg, messageAlign='left', button=['OK'], defaultButton='OK')







