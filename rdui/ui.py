import maya.cmds as cmds

print "UI"

def rigarm(*args):
	print "Rig_Arm"
	import rig.rig_arm as rig_arm
	reload(rig_arm)
	rig_arm = rig_arm.Rig_Arm()
	rig_arm.rig_arm

menuarray = cmds.window('MayaWindow', q = True, ma = True)
if 'Rdojo_Menu' not in menuarray:
	mymenu = cmds.menu('Rdojo_Menu', label = 'RDMenu', to = True, p = 'MayaWindow')
	cmds.menuItem(label = 'Rig_Arm', p = mymenu, command = rigarm)
