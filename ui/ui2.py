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

		dp.loadData()


	def ui(self, *args):
		# check if UI already exists
		windowName = "Window"
		if pm.window(windowName, exists=True):
			pm.deleteUI(windowName)

		# set up window and button size
		windowWidth = 375
		windowHeight = 75
		listWidth = 125
		listHeight = 30
		buttonWidth = 100
		buttonHeight = 30

		self.uiElements['window'] = pm.window(windowName, width=windowWidth, height=windowHeight, title='RDojo_UI', sizeable=True)

		# create ui layouts
		#self.uiElements['mainColLayout'] = pm.columnLayout(adjustableColumn=True)
		self.uiElements['guiMainFlowLayout']=pm.flowLayout(v=True)
		self.uiElements['guiFrameLayout'] = pm.frameLayout(label='Layout', borderStyle='in', p=self.uiElements['guiMainFlowLayout'])
		self.uiElements['guiFlowLayout'] = pm.rowLayout(numberOfColumns=3, columnWidth3=(80, 80, 80),
														columnAlign=(1, 'center'),
														columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)],
														parent=self.uiElements['guiFrameLayout'])
		self.uiElements['guiFlowLayoutB'] = pm.rowLayout(numberOfColumns=4, columnWidth3=(80, 80, 80),
														columnAlign=(1, 'center'),
														columnAttach=[(1, 'left', 20), (2, 'left', 10), (3, 'left', 10),  (4, 'left', 10)],
														 columnWidth4=[listWidth, listWidth, listWidth, listWidth],
														 adjustableColumn4=4, parent=self.uiElements['guiFrameLayout'])


		# create comboboxes and button
		#self.uiElements['comboRowLayout'] = pm.rowColumnLayout(numberOfRows=2, parent=self.uiElements['guiFlowLayout'])
		#self.uiElements['comboRowLayout'] = pm.rowColumnLayout(numberOfColumns=3, columnWidth=[(1,listWidth), (2,listWidth), (3,listWidth)], columnOffset=[(2, "both", 2)], parent=self.uiElements['guiFlowLayout'])
		self.createComboBox(listWidth, listHeight)

		#pm.separator(width=10, horizontal=True, style='none', parent=self.uiElements['guiFlowLayout'])
		#self.uiElements['buttonRowLayout'] = pm.rowColumnLayout(numberOfColumns=3, columnAlign=[2, 'center'], parent=self.uiElements['guiFlowLayout'])
		self.uiElements['rigButton'] = pm.button(label='Create Rig', width=buttonWidth, height=buttonHeight, backgroundColor=[.2, .3, .2], parent=self.uiElements['guiFlowLayoutB'], command=self.rigarm)

		# show window
		pm.showWindow(windowName)
		

	def createComboBox(self, lWidth, lHeight):
		# load the menu file to create comboboxes
		fileName = os.environ['DATA_PATH'] + 'menuData.json'
		menuInfo = json.loads(utils.readJson(fileName))	 

		for dictItem in menuInfo:
			# get appropriate label
			items = menuInfo.get(dictItem)
			print 'items = ', items
			pos = [ndx for ndx, char in enumerate(dictItem) if char.isupper()]
			labelName = dictItem[0:pos[0]].capitalize()+" "+dictItem[pos[0]:len(dictItem)]
			print 'label name = ', labelName
	
			self.uiElements['comboLabel'] = pm.text(label=labelName, font="boldLabelFont", width=lWidth, height=lHeight, parent=self.uiElements['guiFlowLayout'])

			self.uiElements[dictItem] = pm.optionMenu(width=lWidth, height=lHeight, parent=self.uiElements['guiFlowLayoutB'], changeCommand=partial(self.item_changed, dictItem))
			for di in items:
				print 'di = ', di
				pm.menuItem(label=di, parent=self.uiElements[dictItem])

	
	def item_changed(self, itemName, *args):
		print 'change command item = ', itemName
		val = pm.optionMenu(self.uiElements[itemName], query=True, value=True)
		print 'value = ', val

 


	def rigarm(self, *args):
		import rig.rig_arm as ra
		reload(ra)

		arm = ra.RigArm()
		arm.createRig(self.uiElements)

