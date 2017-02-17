import maya.cmds as cmds
print 'UI active'

def rigArm(*args):
    import rig.rig_arm_kc4 as rig_arm
    reload(rig_arm)
    #this makes an instance of the class... I think. The tutorial video was very confusing
    # because everything had the same name. So my understanding is that R_arm is my instance, rig_arm calls
    # the file, and Rig_Arm is the actual function that's being called..? Goodness I hope this works...
    Rarm = rig_arm.Rig_Arm()
    rig_arm.Rarm

mymenu=cmds.menu('RDojo_menu', label='RDojo Menu', tearOff=True, p='MayaWindow')
cmds.menuItem(label='rig_arm', p=mymenu, command=rigArm)

