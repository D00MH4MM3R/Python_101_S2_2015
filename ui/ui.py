import pymel.core as pm 

print 'UI'

def rigarm(*args):
	import rig.rig_arm as ra
	reload(ra)

	arm = ra.RigArm()
	arm.createRig()


mymenu = pm.menu('RDojo_Menu', label='RDMenu', tearOff=True, parent='MayaWindow')
pm.menuItem(label='Rig_Arm', parent=mymenu, command=rigarm)

