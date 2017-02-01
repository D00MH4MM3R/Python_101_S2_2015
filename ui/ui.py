import maya.cmds as cmds

def rigarm(*args):
	print 'Rig_Arm'
	import rig.arm_rig as arm_rig



myMenu = cmds.menu('RDojo_Menu', l = 'RDMenu', to = True, p = 'MayaWindow')
cmds.menuItem(l = 'Rig Arm', p =  myMenu, command = rigarm)

