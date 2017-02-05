import maya.cmds as cmds
print 'UI active'

def rigArm(*args):
    import rig.rig_arm_kc3clean as rig_arm

mymenu=cmds.menu('RDojo_menu', label='RDojo Menu', tearOff=True, p='MayaWindow')
cmds.menuItem(label='rig_arm', p=mymenu, command=rigArm)
