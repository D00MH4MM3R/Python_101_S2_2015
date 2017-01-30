import maya.cmds as cmds

print "UI"

def rigarm(*args):
    print "Rig_Arm"
    import rig.rig_arm

myMenu = cmds.menu('RDojo_Menu', l='RDMenu', to=True, p='MayaWindow')
cmds.menuItem(l='Rig_Arm', p=myMenu, command=rigarm)
