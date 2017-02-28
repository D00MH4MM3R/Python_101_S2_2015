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
		self.msg = ''
		self.view = False

		dp.loadData()


	def ui(self, *args):
		# check if UI already exists
		windowName = "Window"
		if pm.window(windowName, exists=True):
			pm.deleteUI(windowName)

		# set up window and button size
		windowWidth = 245
		windowHeight = 145
		listWidth = 75
		listHeight = 30
		buttonWidth = 100
		buttonHeight = 30

		self.uiElements['window'] = pm.window(windowName, width=windowWidth, height=windowHeight, title='RDojo_UI', sizeable=True)

		# create ui layouts
		self.uiElements['mainColLayout'] = pm.columnLayout(width=windowWidth, backgroundColor=(.5, .5, .5))
		self.uiElements['guiFrameLayout'] = pm.frameLayout(label='Layout', borderStyle='in', backgroundColor=(.5, .5, .5), parent=self.uiElements['mainColLayout'])
		self.uiElements['guiLabelLayout'] = pm.rowLayout(numberOfColumns=3, columnWidth3=(80, 75, 80), columnAlign=[(1, 'center'), (2, 'center'), (3, 'center')], 
			columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)], parent=self.uiElements['guiFrameLayout'])
		self.uiElements['guiComboLayout'] = pm.rowLayout(numberOfColumns=3, columnWidth3=(listWidth, listWidth, listWidth), columnAttach=[(1, 'both', 2), (2, 'both', 2), (3, 'both', 2)], 
			parent=self.uiElements['guiFrameLayout'])
		self.uiElements['guiMsgLayout'] = pm.rowLayout(numberOfColumns=1, width=windowWidth, parent=self.uiElements['guiFrameLayout'])
		self.uiElements['guiButtonLayout'] = pm.rowLayout(numberOfColumns=1, width=windowWidth, parent=self.uiElements['guiFrameLayout'])

		# create comboboxes and button
		self.createComboBox(listWidth, listHeight)

		self.uiElements['errorMsg'] = pm.text(label=self.msg, width=windowWidth, height=buttonHeight, align='center', font='boldLabelFont', visible=self.view, parent=self.uiElements['guiMsgLayout']) 
		self.uiElements['rigButton'] = pm.button(label='Create Rig', width=windowWidth, height=buttonHeight, backgroundColor=(.1, .2, .2), parent=self.uiElements['guiButtonLayout'], 
			command=self.rigarm)

		# show window
		pm.showWindow(windowName)
		

	def createComboBox(self, lWidth, lHeight):
		print 'creating combo boxes'
		# load the menu file to create comboboxes
		fileName = os.environ['DATA_PATH'] + 'menuData.json'
		menuInfo = json.loads(utils.readJson(fileName))	 

		for dictItem in menuInfo:
			# get appropriate label
			items = menuInfo.get(dictItem)
			pos = [ndx for ndx, char in enumerate(dictItem) if char.isupper()]
			labelName = dictItem[0:pos[0]].capitalize()+" "+dictItem[pos[0]:len(dictItem)]
	
			self.uiElements['comboLabel'] = pm.text(label=labelName, font="boldLabelFont", width=lWidth, height=lHeight, parent=self.uiElements['guiLabelLayout'])
			self.uiElements[dictItem] = pm.optionMenu(width=lWidth, height=lHeight, backgroundColor=(.5, .5, .5), parent=self.uiElements['guiComboLayout'], 
				changeCommand=partial(self.item_changed, dictItem))
			for di in items:
				pm.menuItem(label=di, parent=self.uiElements[dictItem])
			
	
	def item_changed(self, itemName, *args):
		print 'running change function'
		val = pm.optionMenu(self.uiElements[itemName], query=True, value=True)
		if val == ' ':
			self.msg = itemName + ' cannot be blank.'
			self.view = True
			print itemName + ' cannot be blank.'
 		return val


	def rigarm(self, *args):
		import rig.rig_arm as ra
		reload(ra)

		arm = ra.RigArm()
		arm.createRig(self.uiElements)

