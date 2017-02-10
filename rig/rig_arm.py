# rig_arm.py
# @author: TOMG
# @reason: RiggingDojo
# @modified: 2/7/2017
# TODO : general refactoring and cleanup
# TODO : Mathify PoleVector Placements; set PV root position via config; Fix IK setup in general <see legs>
# TODO : Get the IKFK switch / BlendColor Node hooked up one of these days
# TODO : Find elegant solution for mirror axis
# TODO : Setup RvL control colours for each type, e.g. 'ctrl_colors': { 'fk_right': [0,1,0], 'fk_left': [1,0,0] }, etc.
# TODO : Final Cleanup Phase of parenting full groups; RIGHT_ARM -> SPINE <- LEFT_ARM, etc.

from PySide import QtCore
from PySide import QtGui
from shiboken import wrapInstance
import maya.OpenMayaUI as omui
import maya.cmds as cmds
import system.utils as utils
import os

print "We Have Imported RIG_ARM"

'''
# declare a data structure, fill it with useful information
_jointData = {
    'default': {
        'prefix': ['ik', 'fk', 'rig'],
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
            }
        }
    }
}
jsonFilePath = os.path.join( os.environ['RIGGING_TOOL'], 'layout', 'layout.json' )
utils.writeJson(jsonFilePath, _jointData)
'''

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
                if mirrorNaming == 'R':
                    newJointPos = [(jnt['position'][0] * -1.0), jnt['position'][1],
                                   jnt['position'][2]]  # mirroring in X only for now
            else:
                ikhName = chain
                newJointName = '{0}_{1}_{2}'.format(prefix, jnt['name'], 'jnt')
                # newJointPos = jnt['position']

            # print newJointName, newJointPos
            newJoint = cmds.joint(n=newJointName, p=newJointPos)
            chainJoints.append(newJoint)

        # chain completed - build controllers, IK Handles, Switches, etc...
        if chainData['use_ik'] and prefix == 'ik':
            # print "BUILDING IK"
            self.CreateIKController(handleName=ikhName, startJoint=chainJoints[0], endJoint=chainJoints[-1],
                                    alignment=chainData['ctrl_alignment'])
            self.CreatePoleVector(handleName=ikhName, alignmentJoint=chainJoints[1], offset=chainData['offset_value'])

        if chainData['use_fk'] and prefix == 'fk':
            # print "BUILDING FK"
            self.CreateFKController(chainJoints, chainData['ctrl_alignment'])

        if prefix == 'rig':
            self.AttachToBaseRig(chainJoints)

    def CreateIKController(self, handleName='', startJoint='', endJoint='', solverType='ikRPsolver',
                           alignment=(0, 0, 0)):
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
        self.SetControllerColor(controlName=ikControl, rgb=[1.0, 1.0, 0.0])

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
        self.SetControllerColor(controlName=pvControl, rgb=[1.0, 1.0, 0.0])

        cmds.xform(pvControl, t=(pos[0], pos[1], pos[2] - offset), roo='xyz', ro=(0, 90, 0))
        cmds.makeIdentity(pvControl, apply=True, t=1, r=1, s=1, n=0, pn=1)
        cmds.delete(ch=True)

        # make a pole vector
        cmds.poleVectorConstraint(pvControl, t_handleName, w=1.0)

    def CreateFKController(self, joints=None, alignment=(0, 0, 0)):
        # proceed if we have at least 1 joint to operate on
        if len(joints) > 0:
            for j in range(len(joints) - 1):
                print "J = ", j
                # setup temp vars
                fkJointName = joints[j]  # str('fk_' + joints[j] + '_jnt')
                fkGroup = str('grp_ctrl_' + joints[j])
                fkControl = str('ctrl_' + joints[j])

                pos = cmds.xform(fkJointName, q=True, t=True, ws=True)
                cmds.group(em=True, name=fkGroup)

                cmds.circle(n=fkControl, nr=alignment, c=(0, 0, 0))
                self.SetControllerColor(controlName=fkControl, rgb=[1.0, 0.0, 0.0])

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

    def SetControllerColor(self, controlName=None, rgb=None):
        if controlName:
            if rgb:
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

    def DebugPrint(self):
        print "Hello: ", self


# jsonFilePath = os.path.join( os.environ['RIGGING_TOOL'], 'layout', 'layout.json' )
# _jsonRigData = utils.readJson(jsonFilePath)
# myClass = RigArm()
# myClass.rig_arm(_jsonRigData)

# *********************** #
# UI - PySide Experiments #
# *********************** #

def maya_main_window():
    # get 'pointer' for main Maya from omui
    main_window_ptr = omui.MQtUtil.mainWindow()
    if main_window_ptr is not None:
        return wrapInstance(long(main_window_ptr), QtGui.QWidget)
    else:
        print "ERROR OBTAINING POINTER"


class RiggingToolUi(QtGui.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(RiggingToolUi, self).__init__(parent)

        self.setWindowTitle("Rigging Tool")
        self.setWindowFlags(QtCore.Qt.Tool)

        # Delete UI on close to avoid winEvent error
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        jsonFilePath = os.path.join(os.environ['RIGGING_TOOL'], 'layout', 'layout.json')
        self.jsonData = utils.readJson(jsonFilePath)
        self.projectRigData = self.jsonData['default']

        self.create_layout()
        self.create_connections()

        self.classyArm = RigArm()


    def create_layout(self):
        self.btn_rigFromJson = QtGui.QPushButton("Rig From JSON")
        self.btn_rigFromLocators = QtGui.QPushButton("Rig from LOCATORS")
        self.btn_saveLocatorsAsJson = QtGui.QPushButton("Save LOCATORS as JSON")
        self.btn_thisDoesNothing = QtGui.QPushButton("This Button Does Nothing")

        self.lbl_projectsDrop = QtGui.QLabel("Project")
        self.dropDown_projects = QtGui.QComboBox()
        for k, v in self.jsonData.iteritems():
            self.dropDown_projects.addItem(k)
            #print k, v

        self.lbl_rigsDrop = QtGui.QLabel("Rigs")
        self.dropDown_rigs = QtGui.QComboBox()
        for k, v in self.jsonData.iteritems():
            self.dropDown_rigs.addItem(k)
            #print v

        main_layout = QtGui.QVBoxLayout()

        project_dropDown_layout = QtGui.QHBoxLayout()
        project_dropDown_layout.addWidget(self.lbl_projectsDrop)
        project_dropDown_layout.addWidget(self.dropDown_projects)
        project_dropDown_layout.setStretch(0, 1)
        project_dropDown_layout.setStretch(1, 2)

        rigs_dropDown_layout = QtGui.QHBoxLayout()
        rigs_dropDown_layout.addWidget(self.lbl_rigsDrop)
        rigs_dropDown_layout.addWidget(self.dropDown_rigs)
        rigs_dropDown_layout.setStretch(0, 1)
        rigs_dropDown_layout.setStretch(1, 2)

        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(5)
        main_layout.addLayout(project_dropDown_layout)
        main_layout.addLayout(rigs_dropDown_layout)
        main_layout.addWidget(self.btn_rigFromJson)
        main_layout.addWidget(self.btn_rigFromLocators)
        main_layout.addWidget(self.btn_saveLocatorsAsJson)
        main_layout.addWidget(self.btn_thisDoesNothing)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def create_connections(self):
        self.btn_rigFromJson.clicked.connect(self.RigFromJson)
        self.btn_rigFromLocators.clicked.connect(self.RigFromLocators)
        self.btn_saveLocatorsAsJson.clicked.connect(self.SaveLocatorsAsJson)
        self.btn_thisDoesNothing.clicked.connect(self.ThisDoesNothing)


    def RigFromJson(self):
        print "Rig From JSON"
        self.classyArm.DebugPrint()
        self.classyArm.rig_arm(self.projectRigData)


    def RigFromLocators(self):
        print "RIG FROM LOCATORS!"


    def SaveLocatorsAsJson(self):
        print "SAVE LOCATORS TO JSON!"


    def ThisDoesNothing(self):
        print "Ze Goggles..."

def LaunchUI():
    print "Attempting To Launch..."
    print "...we live in: ", __name__
    # Development workaround for winEvent error when running
    # the script multiple times
    try:
        ui.close()
        ui.deleteLater()
    except:
        pass
    ui = RiggingToolUi()
    ui.show()
