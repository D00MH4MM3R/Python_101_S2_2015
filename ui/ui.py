import pymel.core as pm 
import system.data_prep as dp
reload(dp)
import system.utils as utils
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
		windowWidth = 400
		windowHeight = 125
		listWidth = 125
		listHeight = 30
		buttonWidth = 100
		buttonHeight = 30

		self.uiElements['window'] = pm.window(windowName, width=windowWidth, height=windowHeight, title='RDojo_UI', sizeable=True)

		# create ui layouts
		self.uiElements['mainColLayout'] = pm.columnLayout(adjustableColumn=True)
		self.uiElements['guiFrameLayout'] = pm.frameLayout(label='Layout', borderStyle='in', parent=self.uiElements['mainColLayout'])
		self.uiElements['guiFlowLayout'] = pm.flowLayout(vertical=False, width=windowWidth, height=windowHeight/2, wrap=True, backgroundColor=[.2, .2, .2], parent=self.uiElements['guiFrameLayout'])

		# create buttons
		self.uiElements['comboRowLayout'] = pm.rowColumnLayout(numberOfColumns=3, columnWidth=[(1,listWidth), (2,listWidth), (3,listWidth)], columnOffset=[(2, "both", 2)], parent=self.uiElements['guiFlowLayout'])
		self.createComboBox(listWidth, listHeight)

		pm.separator(width=10, horizontal=True, style='none', parent=self.uiElements['guiFlowLayout'])
		self.uiElements['buttonRowLayout'] = pm.rowLayout(numberOfColumns=1, columnWidth=[(1,buttonWidth)], columnAlign=[1, 'center'], parent=self.uiElements['guiFlowLayout'])
		self.uiElements['rigButton'] = pm.button(label='Create Rig', width=buttonWidth, height=buttonHeight, backgroundColor=[.2, .3, .2], parent=self.uiElements['guiFlowLayout'], command=self.rigarm)

		# show window
		pm.showWindow(windowName)
		

	def createComboBox(self, lWidth, lHeight):
		# load the menu file to create comboboxes
		fileName = os.environ['DATA_PATH'] + 'menuData.json'
		menuInfo = json.loads(utils.readJson(fileName))	 

		for dictItem in menuInfo:
			# get appropriate label
			items = menuInfo.get(dictItem)
			pos = [ndx for ndx, char in enumerate(dictItem) if char.isupper()]
			labelName = dictItem[0:pos[0]].capitalize()+" "+dictItem[pos[0]:len(dictItem)]

			self.cmd = dictItem+'_changed'

			self.uiElements[dictItem] = pm.optionMenu(label=labelName, width=lWidth, height=lHeight, parent=self.uiElements['guiFlowLayout'], changeCommand=self.cmd)
			for di in items:
				pm.menuItem(label=di, parent=self.uiElements[dictItem])

			
	def bodyPart_changed():
		print 'change command'


	def rigarm(*args):
		import rig.rig_arm as ra
		reload(ra)

		arm = ra.RigArm()
		arm.createRig(self.uiElements)

