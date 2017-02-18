import maya.cmds as cmds
print 'UI active'

# def function(*args):
def rigArm(*args):
    #import folder.file as namespace
    import rig.rig_arm_kc4 as rig_arm
    #reload (namespace)
    reload(rig_arm)
    #variable = namespace.class()
    Rarm = rig_arm.Rig_Arm()
    #variable.classFunction()
    Rarm.rigArm()

#add dropdown menu to main toolbar
mymenu = cmds.menu('RDojo_menu', label='RDojo Menu', tearOff=True, p='MayaWindow')
#add item to dropdown menu
cmds.menuItem(label='Rig Arm', p = mymenu, command = rigArm)

