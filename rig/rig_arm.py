'''
rig_arm.py

littered str('lets' + build + 'strings!') everywhere,
just in case we get side swiped by some devious unicode

defined some functions that are pretty similar,
likely will get smashed together next iteration
'''
import maya.cmds as cmds

# declare a data structure, fill it with useful information
_jointData = {'prefix': ['ik', 'fk', 'rig'],
              'names': ['shoulder', 'elbow', 'wrist', 'wristEnd'],
              'positions': [[2.1, 0.0, 5.0], [-0.1, 0.0, 0.0], [1.0, 0, -5.0], [1.0, 0, -8.0]]}


def CreateIKController(handleName='', startJoint='', endJoint='', solverType='ikRPsolver'):
    # setup temp vars
    ikStartJoint = str('ik_' + startJoint + '_jnt')
    ikEndJoint = str('ik_' + endJoint + '_jnt')
    ikGroup = str('grp_ctrl_ik' + endJoint.capitalize())
    ikControl = str('ctrl_ik' + endJoint.capitalize())
    ikHandleName = str('ikh_' + handleName)

    cmds.ikHandle(n=ikHandleName, sj=ikStartJoint, ee=ikEndJoint, sol=solverType, p=2, w=1)
    # Create IK Control
    pos = cmds.xform(ikEndJoint, q=True, t=True, ws=True)
    cmds.group(em=True, name=ikGroup)

    cmds.circle(n=ikControl, nr=(0, 0, 1), c=(0, 0, 0), r=1.5)
    SetControllerColor(controlName=ikControl, rgb=[1.0, 1.0, 0.0])

    cmds.parent(ikControl, ikGroup)
    cmds.xform(ikGroup, t=pos, ws=True)
    cmds.parent(ikHandleName, ikControl)


def CreatePoleVector(handleName='', alignmentJoint=''):
    '''
    This one feels like a real mess as I'm not entirely sure if
    there should be an intermediate grouping / alignment step,
    or just left as a free floating object to be dragged around
    '''
    alignJointName = str("ik_" + alignmentJoint + "_jnt")
    #pvGroup = str('grp_ctrl_pv' + handleName.replace('ikh',''))
    pvControl = str('ctrl_pv_' + handleName)

    pos = cmds.xform(alignJointName, q=True, t=True, ws=True)
    #cmds.group(em=True, name=pvGroup)

    # make a shape, nudge it around, freeze transforms, deleteHistory
    cmds.circle(n=pvControl, nr=(0, 0, 1), c=(0, 0, 0), r=0.5)
    SetControllerColor(controlName=pvControl, rgb=[1.0, 1.0, 0.0])

    cmds.xform(pvControl, t=((pos[0]-3.0), 0, 0), roo='xyz', ro=(0, 90, 0))
    cmds.makeIdentity(pvControl, apply=True, t=1, r=1, s=1, n=0, pn=1)
    cmds.delete(ch=True)

    #cmds.parent(pvControl, pvGroup)
    #cmds.xform(pvGroup, t=pos, ws=True)

    # make a pole vector
    cmds.poleVectorConstraint(pvControl, handleName, w=1.0)


def CreateFKController(joints=None):
    # proceed if we have at least 1 joint to operate on
    if len(joints) > 0:
        for j in range(len(joints)-1):
            # setup temp vars
            fkJointName = str('fk_' + joints[j] + '_jnt')
            fkGroup = str('grp_ctrl_fk' + joints[j].capitalize())
            fkControl = str('ctrl_fk' + joints[j].capitalize())

            pos = cmds.xform(fkJointName, q=True, t=True, ws=True)
            cmds.group(em=True, name=fkGroup)

            cmds.circle(n=fkControl, nr=(0, 0, 1), c=(0, 0, 0))
            SetControllerColor(controlName=fkControl, rgb=[1.0, 0.0, 0.0])

            cmds.parent(fkControl, fkGroup)
            cmds.xform(fkGroup, t=pos, ws=True)

            # orient constrain joint to controller
            cmds.orientConstraint(fkControl, fkJointName, w=1.0)

            if j != 0:
                # parent currentGroup to previousControl ... if we're not the first one
                previousControl = str('ctrl_fk' + joints[j-1].capitalize())
                cmds.parent(fkGroup, previousControl)
    else:
        print "Joint List must contain at least ONE entry - are you sure you're passing in the right list?"

def AttachToBaseRig(joints=None):
    if len(joints) > 0:
        for j in range(len(joints)):
            # setup temp vars
            fkJointName = str('fk_' + joints[j] + '_jnt')
            ikJointName = str('ik_' + joints[j] + '_jnt')
            rigJointName = str('rig_' + joints[j] + '_jnt')

            # doCreateParentConstraintArgList 1 { "1","0","0","0","0","0","0","1","","1" }; <--- actually necessary?
            cmds.parentConstraint(fkJointName, ikJointName, rigJointName, mo=True, w=1)
    else:
        print "Joint List must contain at least ONE entry - are you sure you're passing in the right list?"

def SetControllerColor(controlName=None, rgb=None):
    if controlName != None:
        if rgb != None:
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]
            # override default display draw
            cmds.setAttr(controlName + ".overrideEnabled", True)
            cmds.setAttr(controlName + ".overrideRGBColors", True)
            # set RGB color
            cmds.setAttr(controlName + ".overrideColorRGB", r, g, b)
        else:
            print "Missing an RGB list - continue with defaults"
    else:
        print "Missing a control name to set color - moving on"

# all together now:
# create all the necessary joints
for pfx in _jointData['prefix']:
    # start a new chain
    cmds.select(cl=True)

    for i in range(len(_jointData['names'])):
        # set some temp variables
        jointName = str(pfx + '_' + _jointData['names'][i] + '_jnt')
        jointPos = _jointData['positions'][i]
        # create the current joint
        cmds.joint(n=jointName, p=jointPos)

    if pfx == 'ik':
        CreateIKController(handleName='arm', startJoint='shoulder', endJoint='wrist')
        CreatePoleVector(handleName='arm', alignmentJoint='elbow')
    elif pfx == 'fk':
        CreateFKController(_jointData['names'])
    else:
        AttachToBaseRig(_jointData['names'])
        # TODO :: BlendColors Node / IKFK Switch
