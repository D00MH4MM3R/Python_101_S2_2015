# TODO : Combine 'CreateIK', 'CreateFK', etc... into 'CreateController(ctrlType)'
import maya.cmds as cmds
import maya.OpenMaya as om
import os
import json


def writeJson(fileName, data, prtyIndent=None):
    with open(fileName, 'w') as outFile:
        json.dump(data, outFile, indent=prtyIndent, separators=(',', ': '), sort_keys=True)
    outFile.close()


def readJson(fileName):
    with open(fileName, 'r') as inFile:
        data = (open(inFile.name, 'r').read())
    return json.loads(data)


def SaveCustomShape(shapeName=None, debug=False):
    if shapeName == None:
        shapeName = cmds.ls(sl=True)[0]
    cvCount = cmds.getAttr(shapeName + '.cp', s=1)
    cvPos = []
    for i in range(0, cvCount):
        cp = cmds.select(shapeName + '.cv[' + str(i) + ']')
        p = cmds.xform(cp, q=True, t=True, ws=True)
        cvPos.append(p)

    # TODO : write to CustomShapes.json:
    # { "shapeName": [cvPos, cvPos, cvPos] }
    if debug:
        return cvPos


def CreateCustomShape(shapeName=None, cvPositions=[]):
    # load Resources/CustomShapes.json
    # check for shapeName in keys
    # if found:
    # shapesJson = {}
    if shapeName:  # and shapesJson:
        # Create Curve
        cmds.curve(n=shapeName, p=cvPositions)

        # Get Some Renaming Done
        cmds.select(shapeName, r=True)
        all = cmds.ls(sl=True, dag=True, shapes=True)
        for shape in all:
            cmds.rename(shape, "{0}Shape".format(cmds.listRelatives(shape, parent=True)[0]))
    else:
        print "FAILED TO CREATE CUSTOM SHAPE"
# del temp
# temp = None
# temp = SaveCustomShape()
# CreateCustomShape(shapeName="ctrl_control_name", cvPositions=temp)


def SetCustomColor(objectName=None, rgb=None, *args):
    for a in args:
        print a
    if objectName:
        if rgb:
            r, g, b = rgb[0], rgb[1], rgb[2]
            try:
                # override default display draw
                cmds.setAttr(objectName + ".overrideEnabled", True)
                cmds.setAttr(objectName + ".overrideRGBColors", True)
                # set RGB color
                cmds.setAttr(objectName + ".overrideColorRGB", r, g, b)
            except:
                print "Something has gone terribly wrong while attempting to override {0} colors with {1}".format(objectName, rgb)
        else:
            print "Missing an RGB list - continue with defaults"
    else:
        print "Missing a control name to set color - moving on"


def ConstructJointChain(prefix='', chain='', chainData=None, mirrorNaming=None):
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
        CreateIKController(handleName=ikhName, startJoint=chainJoints[0], endJoint=chainJoints[-1], alignment=chainData['ctrl_alignment'])
        CreatePoleVector(handleName=ikhName, alignmentJoints=chainJoints)

    if chainData['use_fk'] and prefix.lower() == 'fk':
        # print "BUILDING FK"
        CreateFKController(chainJoints, chainData['ctrl_alignment'])

    #if prefix.lower() == 'rig':
    #    self.AttachToBaseRig(chainJoints)
    return chainJoints


def CreateIKController(handleName='', startJoint='', endJoint='', solverType='ikRPsolver', alignment=(0, 0, 0)):
    # setup temp vars
    ikGroup = str('grp_ctrl_' + endJoint)
    ikControl = str('ctrl_' + endJoint)
    ikHandleName = str('ikh_' + handleName)

    cmds.ikHandle(n=ikHandleName, sj=startJoint, ee=endJoint, sol=solverType, p=2, w=1)
    # Create IK Control
    pos = cmds.xform(endJoint, q=True, t=True, ws=True)
    cmds.group(em=True, name=ikGroup)

    cmds.circle(n=ikControl, nr=alignment, c=(0, 0, 0), r=1.5)
    SetCustomColor(objectName=ikControl, rgb=[1.0, 1.0, 0.0])

    cmds.parent(ikControl, ikGroup)
    cmds.xform(ikGroup, t=pos, ws=True)
    cmds.parent(ikHandleName, ikControl)


def CreatePoleVector(handleName='', alignmentJoints=[]):
    pvControl = str('ctrl_pv_' + handleName)
    t_handleName = str('ikh_' + handleName)

    pos = CalculatePVPosition(alignmentJoints)
    # cmds.group(em=True, name=pvGroup)

    # make a shape, nudge it around, freeze transforms, deleteHistory
    cmds.cone(n=pvControl, r=0.5)
    #cmds.circle(n=pvControl, nr=(0, 0, 0), c=(0, 0, 0), r=0.5)
    SetCustomColor(objectName=pvControl, rgb=[0.0, 1.0, 0.0])

    cmds.xform(pvControl, t=pos, roo='xyz', ro=(0, 90, 0))
    cmds.makeIdentity(pvControl, apply=True, t=1, r=1, s=1, n=0, pn=1)
    cmds.delete(ch=True)

    # make a pole vector
    cmds.poleVectorConstraint(pvControl, t_handleName, w=1.0)


def CalculatePVPosition(joints):
    start = cmds.xform(joints[0], q=True, ws=True, t=True)
    mid = cmds.xform(joints[1], q=True, ws=True, t=True)
    end = cmds.xform(joints[2], q=True, ws=True, t=True)

    startV = om.MVector(start[0], start[1], start[2])
    midV = om.MVector(mid[0], mid[1], mid[2])
    endV = om.MVector(end[0], end[1], end[2])

    startEnd = endV - startV
    startMid = midV - startV

    dotP = startMid * startEnd

    proj = float(dotP)/float(startEnd.length())

    startEndN = startEnd.normal()

    projV = startEndN * proj
    arrowV = startMid - projV
    arrowV *= 2.5
    finalV = arrowV + midV

    return [finalV.x, finalV.y, finalV.z]


def CreateFKController(joints=None, alignment=(0, 0, 0)):
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
            SetCustomColor(objectName=fkControl, rgb=[1.0, 0.0, 0.0])

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


def AttachToBaseRig(jointsChain=None, useMirror=False):
    """

    :rtype: None, nothing, zilch, nada
    """
    if useMirror:
        zipChain = [x for x in list(zip(*jointsChain))]
        for zc in zipChain:
            tempL = []
            tempR = []
            for i in range(0, len(zc)):
                if i % 2 == 0:
                    tempR.append(zc[i])
                else:
                    tempL.append(zc[i])
            cmds.parentConstraint(tempL[:-1], tempL[-1], mo=True, w=1)
            cmds.parentConstraint(tempR[:-1], tempR[-1], mo=True, w=1)
    else:
        for i in range(0, len(jointsChain[0])):
            cmds.parentConstraint((zip(*jointsChain[:-1])[i]), jointsChain[-1][i], mo=True, w=1)
    # print "CONNECTING: ", fkJointName, ikJointName, rigJointName
    # doCreateParentConstraintArgList 1 { "1","0","0","0","0","0","0","1","","1" }; <--- actually necessary?
    # cmds.parentConstraint(fkJointName, ikJointName, rigJointName, mo=True, w=1)
