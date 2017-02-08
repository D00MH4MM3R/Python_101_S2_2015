import maya.cmds as cmds
import os

print "UI"

def rigarm(*args):
    print "Rig_Arm"
    import rig.rig_arm
    import system.utils as utils
    jsonFilePath = os.path.join(os.environ['RIGGING_TOOL'], 'layout', 'layout.json')
    _jsonRigData = utils.readJson(jsonFilePath)
    arm = rig.rig_arm.RigArm()
    arm.rig_arm(_jsonRigData)

myMenu = cmds.menu('RDojo_Menu', l='RDMenu', to=True, p='MayaWindow')
cmds.menuItem(l='Rig_Arm', p=myMenu, command=rigarm)
