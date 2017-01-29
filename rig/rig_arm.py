'''
rig_arm.py

littered str('lets' + build + 'strings!') everywhere,
just in case we get side swiped by some devious unicode
'''
import maya.cmds as cmds

# declare our data structure, fill it with useful information
_jointData = {'prefix': ['ik', 'fk', 'rig'],
              'names': ['shoulder', 'elbow', 'wrist', 'wristEnd'],
              'positions': [[2.1, 0.0, 5.0], [-0.1, 0.0, 0.0], [1.0, 0, -5.0], [1.0, 0, -8.0]]
              }

# define some funcitons that are pretty similar, that may likely get smashed together next iteration
def CreateIKController(handleName='', startJoint='', endJoint='', solverType='ikRPsolver'):
    # setup temp vars
    ikStartJoint = str('ik_' + startJoint + '_jnt')
    ikEndJoint = str('ik_' + endJoint + '_jnt')
    ikGroup = str('grp_ctrl_ik' + endJoint.capitalize())
    ikControl = str('ctrl_ik' + endJoint.capitalize())

    cmds.ikHandle(n=handleName, sj=ikStartJoint, ee=ikEndJoint, sol=solverType, p=2, w=1)
    # Create IK Control
    pos = cmds.xform(ikEndJoint, q=True, t=True, ws=True)
    cmds.group(em=True, name=ikGroup)
    cmds.circle(n=ikControl, nr=(0, 0, 1), c=(0, 0, 0), r=1.5)
    cmds.parent(ikControl, ikGroup)
    cmds.xform(ikGroup, t=pos, ws=True)
    cmds.parent(handleName, ikControl)

# Create "FK Rig" ... i think
def CreateFKController(joints=[]):
    if len(joints) > 0:
        for j in range(len(joints)-1):
            # setup temp vars
            fkJointName = str('fk_' + joints[j] + '_jnt')
            fkGroup = str('grp_ctrl_fk' + joints[j].capitalize())
            fkControl = str('ctrl_fk' + joints[j].capitalize())

            pos = cmds.xform(fkJointName, q=True, t=True, ws=True)
            cmds.group(em=True, name=fkGroup)
            cmds.circle(n=fkControl, nr=(0, 0, 1), c=(0, 0, 0))
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

# create all the necessary joints
for pfx in _jointData['prefix']:
    # start a new chain
    cmds.select(cl=True)

    for i in range(len(_jointData['names'])):
        # set some temp variables
        jointName = str(pfx + '_' + _jointData['names'][i] +'_jnt')
        jointPos = _jointData['positions'][i]
        # create the current joint
        cmds.joint(n=jointName, p=jointPos)

    if pfx == 'ik':
        CreateIKController(handleName='ikh_arm', startJoint='shoulder', endJoint='wrist')

    elif pfx == 'fk':
        CreateFKController(_jointData['names'])

    else:
        # TODO :: Connect IK and FK to Rig joints
        # TODO :: sort out Pole-Vector
        # TODO :: sort out hooking these up...
        print "HOOK 'EM UP!"
