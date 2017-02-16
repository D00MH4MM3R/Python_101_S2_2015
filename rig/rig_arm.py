# rig_arm.py
# @author: TOMG
# @reason: RiggingDojo
# @modified: 2/12/2017
# TODO : general refactoring and cleanup
# TODO : Mathify PoleVector Placements; set PV root position via config; Fix IK setup in general <see legs>
# TODO : Get the IKFK switch / BlendColor Node hooked up one of these days
# TODO : Find elegant solution for mirror axis
# TODO : Setup RvL control colours for each type, e.g. 'ctrl_colors': { 'fk_right': [0,1,0], 'fk_left': [1,0,0] }, etc.
# TODO : Final Cleanup Phase of parenting full groups; RIGHT_ARM -> SPINE <- LEFT_ARM, etc.

#from PySide import QtCore
#from PySide import QtGui
#from shiboken import wrapInstance
#import maya.OpenMayaUI as omui
import maya.cmds as cmds
import system.utils as utils
#import os

print "We Have Imported RIG_ARM"

class RigArm(object):
    def __init__(self):
        print "Initializing RigArm:", self


    def rig_arm(self, jsonRigData):
        print "commencing rig... ", self
        for pfx in jsonRigData['prefix']:
            for chain in jsonRigData['chains']:
                chainData = jsonRigData['chains'][chain]

                if chainData['use_mirror'] == True:
                    for mName in jsonRigData['mirrorName']:
                        self.ConstructJointChain(pfx, chain, chainData, mName)
                else:
                    self.ConstructJointChain(pfx, chain, chainData)


    def ConstructJointChain(self, prefix='', chain='', chainData=None, mirrorNaming=None):
        # start a new chain
        chainJoints = []

        cmds.select(cl=True)
        for jnt in chainData['joints']:
            ikhName = ''
            newJointName = ''
            # newJointPos = []
            newJointPos = jnt['position']

            if mirrorNaming:
                ikhName = '{0}_{1}'.format(mirrorNaming, chain)
                newJointName = '{0}_{1}_{2}_{3}'.format(prefix, mirrorNaming, jnt['name'], 'jnt')
                if 'r' in mirrorNaming.lower():
                    newJointPos = [(jnt['position'][0] * -1.0), jnt['position'][1], jnt['position'][2]]  # mirroring in X only for now, assuming that Left values are provided first
            else:
                ikhName = chain
                newJointName = '{0}_{1}_{2}'.format(prefix, jnt['name'], 'jnt')
                # newJointPos = jnt['position']

            # print newJointName, newJointPos
            newJoint = cmds.joint(n=newJointName, p=newJointPos)
            chainJoints.append(newJoint)

        # chain completed - build controllers, IK Handles, Switches, etc...
        if chainData['use_ik'] and prefix.lower() == 'ik':
            # print "BUILDING IK"
            self.CreateIKController(handleName=ikhName, startJoint=chainJoints[0], endJoint=chainJoints[-1], alignment=chainData['ctrl_alignment'])
            self.CreatePoleVector(handleName=ikhName, alignmentJoint=chainJoints[1], offset=chainData['offset_value'])

        if chainData['use_fk'] and prefix.lower() == 'fk':
            # print "BUILDING FK"
            self.CreateFKController(chainJoints, chainData['ctrl_alignment'])

        if prefix.lower() == 'rig':
            self.AttachToBaseRig(chainJoints)


    def CreateIKController(self, handleName='', startJoint='', endJoint='', solverType='ikRPsolver', alignment=(0, 0, 0)):
        # setup temp vars
        # ikStartJoint = str('ik_' + startJoint + '_jnt')
        # ikEndJoint = str('ik_' + endJoint + '_jnt')
        ikGroup = str('grp_ctrl_' + endJoint)
        ikControl = str('ctrl_' + endJoint)
        ikHandleName = str('ikh_' + handleName)

        cmds.ikHandle(n=ikHandleName, sj=startJoint, ee=endJoint, sol=solverType, p=2, w=1)
        # Create IK Control
        pos = cmds.xform(endJoint, q=True, t=True, ws=True)
        cmds.group(em=True, name=ikGroup)

        cmds.circle(n=ikControl, nr=alignment, c=(0, 0, 0), r=1.5)
        utils.SetCustomColor(objectName=ikControl, rgb=[1.0, 1.0, 0.0])

        cmds.parent(ikControl, ikGroup)
        cmds.xform(ikGroup, t=pos, ws=True)
        cmds.parent(ikHandleName, ikControl)


    def CreatePoleVector(self, handleName='', alignmentJoint='', offset=3.0):
        # TODO :: Math it up a little more in here
        pvControl = str('ctrl_pv_' + handleName)
        t_handleName = str('ikh_' + handleName)

        pos = cmds.xform(alignmentJoint, q=True, t=True, ws=True)
        # cmds.group(em=True, name=pvGroup)

        # make a shape, nudge it around, freeze transforms, deleteHistory
        cmds.circle(n=pvControl, nr=(0, 0, 0), c=(0, 0, 0), r=0.5)
        utils.SetCustomColor(objectName=pvControl, rgb=[1.0, 1.0, 0.0])

        cmds.xform(pvControl, t=(pos[0], pos[1], pos[2] - offset), roo='xyz', ro=(0, 90, 0))
        cmds.makeIdentity(pvControl, apply=True, t=1, r=1, s=1, n=0, pn=1)
        cmds.delete(ch=True)

        # make a pole vector
        cmds.poleVectorConstraint(pvControl, t_handleName, w=1.0)


    def CreateFKController(self, joints=None, alignment=(0, 0, 0)):
        # proceed if we have at least 1 joint to operate on
        if len(joints) > 0:
            for j in range(len(joints) - 1):
                # setup temp vars
                fkJointName = joints[j]  # str('fk_' + joints[j] + '_jnt')
                fkGroup = str('grp_ctrl_' + joints[j])
                fkControl = str('ctrl_' + joints[j])

                pos = cmds.xform(fkJointName, q=True, t=True, ws=True)
                cmds.group(em=True, name=fkGroup)

                cmds.circle(n=fkControl, nr=alignment, c=(0, 0, 0))
                utils.SetCustomColor(objectName=fkControl, rgb=[1.0, 0.0, 0.0])

                cmds.parent(fkControl, fkGroup)
                cmds.xform(fkGroup, t=pos, ws=True)

                # orient constrain joint to controller
                cmds.orientConstraint(fkControl, fkJointName, w=1.0)

                if j != 0:
                    # parent currentGroup to previousControl ... if we're not the first one
                    previousControl = str('ctrl_' + joints[j - 1])
                    cmds.parent(fkGroup, previousControl)
        else:
            print "Joint List must contain at least ONE entry - are you sure you're passing in the right list?"


    def AttachToBaseRig(self, joints=None):
        if joints:
            jointCount = len(joints)
            for i in range(0, jointCount):
                # setup temp vars
                fkJointName = joints[i].replace('rig', 'fk')
                ikJointName = joints[i].replace('rig', 'ik')
                rigJointName = joints[i]

                print "CONNECTING: ", fkJointName, ikJointName, rigJointName
                # doCreateParentConstraintArgList 1 { "1","0","0","0","0","0","0","1","","1" }; <--- actually necessary?
                cmds.parentConstraint(fkJointName, ikJointName, rigJointName, mo=True, w=1)
        else:
            print "Joint List must contain at least ONE entry - are you sure you're passing in the right list?"


    def DebugPrint(self):
        print "Hello: ", self


# jsonFilePath = os.path.join( os.environ['RIGGING_TOOL'], 'layout', 'layout.json' )
# _jsonRigData = utils.readJson(jsonFilePath)
# myClass = RigArm()
# myClass.rig_arm(_jsonRigData)

'''
# declare a data structure, fill it with useful information
_jointData = {
    'default': {
        'prefix': ['IK', 'FK', 'RIG'],
        'postfix': '',
        'mirrorName': ['Right', 'Left'],
        'mirrorAxis': 'x',
        'chains': {
            'arm': {
                'use_mirror': True,
                'use_ik': True,
                'use_fk': True,
                'ctrl_alignment': (1, 0, 0),
                'offset_value': 3.0,
                'joints': [
                    {'name': 'shoulder', 'position': [4.0, 13.0, 0.0]},
                    {'name': 'elbow', 'position': [7.0, 13.0, -1.5]},
                    {'name': 'wrist', 'position': [10.0, 13.0, 0.0]},
                    {'name': 'wristEnd', 'position': [10.5, 13.0, 0.0]}
                ]
            },
            'leg': {
                'use_mirror': True,
                'use_ik': True,
                'use_fk': True,
                'offset_value': -3.0,
                'ctrl_alignment': (0, 1, 0),
                'joints': [
                    {'name': 'hip', 'position': [1.5, 7.5, 0.0]},
                    {'name': 'upper', 'position': [2.5, 6.0, 0.0]},
                    {'name': 'lower', 'position': [2.5, 3.0, 1.5]},
                    {'name': 'foot', 'position': [2.5, 0.0, 0.0]}
                ]
            }
        }
    },
    'RiggingDojo': {
        'prefix': ['ik', 'fk', 'rig'],
        'postfix': 'jnt',
        'mirrorName': ['R', 'L'],
        'mirrorAxis': 'x',
        'chains': {
            'arm': {
                'use_mirror': True,
                'use_ik': True,
                'use_fk': True,
                'ctrl_alignment': (1, 0, 0),
                'offset_value': 3.0,
                'joints': [
                    {'name': 'shoulder', 'position': [4.0, 13.0, 0.0]},
                    {'name': 'elbow', 'position': [7.0, 13.0, -1.5]},
                    {'name': 'wrist', 'position': [10.0, 13.0, 0.0]},
                    {'name': 'wristEnd', 'position': [10.5, 13.0, 0.0]}
                ]
            },
            'leg': {
                'use_mirror': True,
                'use_ik': True,
                'use_fk': True,
                'offset_value': -3.0,
                'ctrl_alignment': (0, 1, 0),
                'joints': [
                    {'name': 'hip', 'position': [1.5, 7.5, 0.0]},
                    {'name': 'upper', 'position': [2.5, 6.0, 0.0]},
                    {'name': 'lower', 'position': [2.5, 3.0, 1.5]},
                    {'name': 'foot', 'position': [2.5, 0.0, 0.0]}
                ]
            },
            'spine': {
                'use_mirror': False,
                'use_ik': False,
                'use_fk': True,
                'offset_value': -3.0,
                'ctrl_alignment': (0, 1, 0),
                'joints': [
                    {'name': 'pelvis', 'position': [0.0, 7.5, 0.0]},
                    {'name': 'spine', 'position': [0.0, 8.5, 0.0]},
                    {'name': 'spine1', 'position': [0.0, 10.0, -1.0]},
                    {'name': 'spine2', 'position': [0.0, 13.5, 0.0]}
                    {'name': 'neck', 'position': [0.0, 14.0, 0.0]}
                ]
            }
        }
    }
}
jsonFilePath = os.path.join( os.environ['RIGGING_TOOL'], 'layout', 'layout.json' )
utils.writeJson(jsonFilePath, _jointData)
'''
