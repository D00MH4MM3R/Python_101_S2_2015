import maya.cmds as cmds

class RDojo_UI:

	def __init__(self, *args):
		activeMenus = cmds.window('MayaWindow', q = True, ma = True)
		for a in activeMenus:
			if a == 'RDojo_Menu':
				cmds.deleteUI('RDojo_Menu', m = True)

		myMenu = cmds.menu('RDojo_Menu', l = 'RDMenu', to = True, p = 'MayaWindow')
		cmds.menuItem(l = 'Rig Tool', p =  myMenu, command = self.ui)

		self.uiElements = {}
		self.uiInfo = {}
		
		print 'Rig_Arm'

	def ui(self, *args):
		windowName = 'ARWindow'
	 	if cmds.window(windowName, exists = True):
	 		cmds.deleteUI(windowName)

	 	
	 	windowHeight = 400
	 	windowWidth = 300
	 	buttonHeight = 200
	 	buttonWidth = 150

	 	self.uiElements['window'] = cmds.window(windowName, w = windowWidth, h = windowHeight, t = 'Auto Rig V 0.5', sizeable = True, mnb = True)

	 	self.uiElements['mainColLayout'] = cmds.columnLayout("mainColLayout", w = windowWidth, adj = True)
	 	self.uiElements['layoutFrameLayout'] = cmds.frameLayout ("layoutTab", w = windowWidth, label = "Layout", cll = True, p = self.uiElements['mainColLayout'])

	 	self.uiElements['layoutButton'] = cmds.button(l= 'Generate Layout', w = windowWidth, h = buttonHeight/2, c = self.riglayout)
	 	self.uiElements['symmArmLayout'] = cmds.rowColumnLayout("Symm", numberOfColumns = 3, columnWidth = [(1, windowWidth/4), (2, windowWidth/1.3)])
	 	self.uiElements['symmBox'] = cmds.checkBox( "symmBox", label = "Symmetry")
	 	cmds.text(l = '*Note: Activate before generating.')
	 	cmds.separator( width = windowWidth, style='none', h = 3,  p = self.uiElements['layoutFrameLayout'])
	 	

	 	
	 	self.uiElements['optionsFrameLayout'] = cmds.frameLayout ("optionsTab", w = windowWidth, label = "Options", cll = True, p = self.uiElements['mainColLayout']) 
	 	self.uiElements['optionsTabLayout'] = cmds.tabLayout('optionsTabs', w = windowWidth)
	 	self.uiElements['optionsArmLayout'] = cmds.rowColumnLayout("Arm", numberOfColumns = 2, columnWidth = [(1, windowWidth/2), (2, windowWidth/2)], p =self.uiElements['optionsTabLayout'])

	 	self.uiElements['stretchArmBox'] = cmds.checkBox( "stretchArmBox", label = "Stretch")
	 	self.uiElements['twistArmBox'] = cmds.checkBox( "twistArmBox", label = "Twist Joints")
	 	cmds.separator( width = windowWidth, style='none', h = 10,  p = self.uiElements['optionsArmLayout'])

	 	self.uiElements['optionsLegLayout'] = cmds.rowColumnLayout("Leg", numberOfColumns = 2, columnWidth = [(1, windowWidth/2), (2, windowWidth/2)], p =self.uiElements['optionsTabLayout'])

	 	self.uiElements['stretchLegBox'] = cmds.checkBox( "stretchLegBox", label = "Stretch")
	 	self.uiElements['twistLegBox'] = cmds.checkBox( "twistLegBox", label = "Twist Joints")
	 	cmds.separator( width = windowWidth, style='none', h = 10,  p = self.uiElements['optionsArmLayout'])

	 	self.uiElements['modFrameLayout'] = cmds.frameLayout ("ModuleTab", w = windowWidth, label = "Modules", cll = True, p = self.uiElements['mainColLayout'])
	 	self.uiElements['modFlowLayout'] = cmds.flowLayout("moduleFlowLayout", v = False, w = windowWidth, h = windowHeight/2, wr = True)

	 	self.uiElements['armButton'] = cmds.button(l= 'Arm', w = buttonWidth, h = buttonHeight/2, c = self.rig_arm)
	 	self.uiElements['legButton'] = cmds.button(l= 'Leg', w = buttonWidth, h = buttonHeight/2, c =  self.rig_leg)
	 	self.uiElements['spineButton'] = cmds.button(l= 'Spine', w = buttonWidth, h = buttonHeight/2, c =  self.filler)
	 	self.uiElements['footButton'] = cmds.button(l= 'Foot', w = buttonWidth, h = buttonHeight/2, c =  self.filler)

	


	 	cmds.showWindow(self.uiElements['window'])

	def rig_arm(self, *args):
		#import the module with an alias
		import rig.arm_rig as arm_rig
		reload(arm_rig)
		#store the class within a variable
		rig_arm = arm_rig.Rig_Arm()
		print 'Rigging Arm'
		#excecute the arm bulding function from within the variable that houses the class
		rig_arm.rig_arm()

	def rig_leg(self, *args):
		#import the module with an alias
		import rig.leg_rig as leg_rig
		reload(leg_rig)
		#store the class within a variable
		rig_leg = leg_rig.Rig_Leg()
		print 'Rigging Leg'
		#excecute the arm bulding function from within the variable that houses the class
		rig_leg.rig_leg()

	def riglayout(self, *args):
		import layout.rig_Layout as rig_Layout
		reload(rig_Layout)
		ly = rig_Layout.Layout()
		ly.importCoord()
		ly.createLayout()

	def filler(*args):
		print 'I do nothing yet'



