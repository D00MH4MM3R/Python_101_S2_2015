import maya.cmds as cmds

def rigarm(*args):
	print 'Rig_Arm'
	import rig.arm_rig as arm_rig
	reload(arm_rig)
	rig_arm = arm_rig.Rig_Arm()
	print arm_rig
	rig_info = rig_arm.rig_arm()



activeMenus = cmds.window('MayaWindow', q = True, ma = True)
if 'RDojo_Menu' not in activeMenus:
	myMenu = cmds.menu('RDojo_Menu', l = 'RDMenu', to = True, p = 'MayaWindow')
	cmds.menuItem(l = 'Rig Arm', p =  myMenu, command = rigarm)

