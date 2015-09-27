import maya.cmds as cmds

#Create Bind Joints
cmds.joint(n = 'shoulderBind_jnt', p = [0, 0, 0], o = [180, 0, 0])
cmds.joint(n = 'elbowBind_jnt', p = [3, 0, 0])
cmds.joint(n = 'wristBind_jnt', p = [6, 0, 0])
cmds.select(d = True)

#Create IK Joints
cmds.joint(n = 'shoulderIK_jnt', p = [0, 0, 0], o = [180, 0, 0])
cmds.joint(n = 'elbowIK_jnt', p = [3, 0, 0])
cmds.joint(n = 'wristIK_jnt', p = [6, 0, 0])
cmds.select(d = True)

#Create FK Joints
cmds.joint(n = 'shoulderFK_jnt', p = [0, 0, 0], o = [180, 0, 0])
cmds.joint(n = 'elbowFK_jnt', p = [3, 0, 0])
cmds.joint(n = 'wristFK_jnt', p = [6, 0, 0])
cmds.select(d = True)

#
#IK Setup
#

#Create IK Handle
cmds.ikHandle(n = 'armIK_HDL', sj = 'shoulderIK_jnt', ee = 'wristIK_jnt', sol = 'ikRPsolver')

#Create IK Control
ikCtrlPos = cmds.xform('wristIK_jnt', q = True, t = True, ws = True)
cmds.circle(n ='armIK_ctrl', nr = (0, 1, 0), c = (0, 0, 0))
cmds.xform('armIK_ctrl', t = ikCtrlPos, ws = True)
cmds.setAttr('armIK_ctrl.rotateZ', 90)
cmds.makeIdentity(a = True, t = 1, r = 1, s = 1, n = 0, pn = 1)
cmds.delete('armIK_ctrl', ch = True)
cmds.parent('armIK_HDL', 'armIK_ctrl')

#Create Pole Vector
pvCtrlPos = cmds.xform('elbowIK_jnt', q = True, t = True, ws = True)
pvCtrlx = pvCtrlPos[0]
pvCtrly = pvCtrlPos[1]
pvCtrlz = pvCtrlPos[2]
cmds.circle(n ='armPV_ctrl', nr = (0, 1, 0), c = (0, 0, 0))
cmds.xform('armPV_ctrl', t = (pvCtrlx, pvCtrly, pvCtrlz - 5), ws = True)
cmds.setAttr('armPV_ctrl.rotateZ', 90)
cmds.setAttr('armPV_ctrl.rotateX', 90)
cmds.makeIdentity(a = True, t = 1, r = 1, s = 1, n = 0, pn = 1)
cmds.delete('armPV_ctrl', ch = True)
cmds.poleVectorConstraint('armPV_ctrl', 'armIK_HDL')


#
#FK Setup
#

#Create FK Controls
cmds.circle(n ='shoulderFK_ctrl', nr = (0, 1, 0), c = (0, 0, 0))
cmds.circle(n ='elbowFK_ctrl', nr = (0, 1, 0), c = (0, 0, 0))
cmds.circle(n ='wristFK_ctrl', nr = (0, 1, 0), c = (0, 0, 0))

#Parent FK Controls to FK joints
#Shoulder
cmds.parent('shoulderFK_ctrl', 'shoulderFK_jnt')
cmds.setAttr('shoulderFK_ctrl.translateX', 0)
cmds.setAttr('shoulderFK_ctrl.translateY', 0)
cmds.setAttr('shoulderFK_ctrl.translateZ', 0)
cmds.setAttr('shoulderFK_ctrl.rotateZ', 90)
cmds.makeIdentity(a = True, t = 1, r = 1, s = 1, n = 0, pn = 1)
cmds.parent('shoulderFK_ctrl', w = True)
cmds.delete('shoulderFK_ctrl', ch = True)
cmds.parent('shoulderFK_ctrlShape', 'shoulderFK_jnt', r = True, s = True)
cmds.delete('shoulderFK_ctrl')

#Elbow
cmds.parent('elbowFK_ctrl', 'elbowFK_jnt')
cmds.setAttr('elbowFK_ctrl.translateX', 0)
cmds.setAttr('elbowFK_ctrl.translateY', 0)
cmds.setAttr('elbowFK_ctrl.translateZ', 0)
cmds.setAttr('elbowFK_ctrl.rotateZ', 90)
cmds.makeIdentity(a = True, t = 1, r = 1, s = 1, n = 0, pn = 1)
cmds.parent('elbowFK_ctrl', w = True)
cmds.delete('elbowFK_ctrl', ch = True)
cmds.parent('elbowFK_ctrlShape', 'elbowFK_jnt', r = True, s = True)
cmds.delete('elbowFK_ctrl')

#Wrist
cmds.parent('wristFK_ctrl', 'wristFK_jnt')
cmds.setAttr('wristFK_ctrl.translateX', 0)
cmds.setAttr('wristFK_ctrl.translateY', 0)
cmds.setAttr('wristFK_ctrl.translateZ', 0)
cmds.setAttr('wristFK_ctrl.rotateZ', 90)
cmds.makeIdentity(a = True, t = 1, r = 1, s = 1, n = 0, pn = 1)
cmds.parent('wristFK_ctrl', w = True)
cmds.delete('wristFK_ctrl', ch = True)
cmds.parent('wristFK_ctrlShape', 'wristFK_jnt', r = True, s = True)
cmds.delete('wristFK_ctrl')

#
#Connect IK and FK joints to Bind
#
armpart = ['shoulder', 'elbow', 'wrist']

for x in range(0, len(armpart)):
    #Connect rotates from IK FK to blend to result on the arm
    cmds.createNode('blendColors', n = 'left_' + armpart[x] + '_rot_IkFkChoice')
    cmds.setAttr('left_' + armpart[x] + '_rot_IkFkChoice.blender', 1)
    cmds.connectAttr(armpart[x] + 'IK_jnt.rotate', 'left_' + armpart[x] + '_rot_IkFkChoice.color1')
    cmds.connectAttr(armpart[x] + 'FK_jnt.rotate', 'left_' + armpart[x] + '_rot_IkFkChoice.color2')
    cmds.connectAttr('left_' + armpart[x] + '_rot_IkFkChoice.output', armpart[x] + 'Bind_jnt.rotate')

    #Connect translates from IK FK to blend to result on the arm
    cmds.createNode('blendColors', n = 'left_' + armpart[x] + '_trans_IkFkChoice')
    cmds.setAttr('left_' + armpart[x] + '_trans_IkFkChoice.blender', 1)
    cmds.connectAttr(armpart[x] + 'IK_jnt.translate', 'left_' + armpart[x] + '_trans_IkFkChoice.color1')
    cmds.connectAttr(armpart[x] + 'FK_jnt.translate', 'left_' + armpart[x] + '_trans_IkFkChoice.color2')
    cmds.connectAttr('left_' + armpart[x] + '_trans_IkFkChoice.output', armpart[x] + 'Bind_jnt.translate')

#Make settings control for IK FK Switch
settingsCtrlPos = cmds.xform('wristBind_jnt', q = True, t = True, ws = True)
setctrlx = settingsCtrlPos[0]
setctrly = settingsCtrlPos[1]
setctrlz = settingsCtrlPos[2]
cmds.circle(n ='settings_ctrl', nr = (0, 1, 0), c = (0, 0, 0))
cmds.xform('settings_ctrl', t = (setctrlx + 5, setctrly, setctrlz), ws = True)
cmds.setAttr('settings_ctrl.rotateZ', 90)
cmds.makeIdentity(a = True, t = 1, r = 1, s = 1, n = 0, pn = 1)
cmds.delete('settings_ctrl', ch = True)
cmds.parentConstraint('wristBind_jnt', 'settings_ctrl', mo = True)
cmds.addAttr(ln = 'ikfkswitch', nn = 'IK FK Switch', at = 'double', min = 0, max = 1, dv = 0, k = True)
for y in range(0, len(armpart)):
    #Connect switch attribute to blendcolor nodes
    cmds.connectAttr('settings_ctrl.ikfkswitch', 'left_' + armpart[y] + '_rot_IkFkChoice.blender')