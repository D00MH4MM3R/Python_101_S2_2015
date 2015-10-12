import maya.cmds as cmds
bindjnt_list = [['shoulderBind_jnt', [0, 0, 0], [180, 0, 0]], ['elbowBind_jnt', [3, 0, 0], [0, 0, 0]], ['wristBind_jnt', [6, 0, 0], [0, 0, 0]]]
ikjnt_list = [['shoulderIK_jnt', [0, 0, 0], [180, 0, 0], [0, 0, 0]], ['elbowIK_jnt', [3, 0, 0], [0, 0, 0]], ['wristIK_jnt', [6, 0, 0], [0, 0, 0]]]
fkjnt_list = [['shoulderFK_jnt', [0, 0, 0], [180, 0, 0]], ['elbowFK_jnt', [3, 0, 0], [0, 0, 0]], ['wristFK_jnt', [6, 0, 0], [0, 0, 0]]]

def createJoint(jntinfo):
    for i in range(len(jntinfo)):
        if i == 0:
            cmds.joint(n = jntinfo[i][0], p = jntinfo[i][1], o = jntinfo[i][2])
        else:
            cmds.joint(n = jntinfo[i][0], p = jntinfo[i][1])

#Create Bind Joints
createJoint(bindjnt_list)
cmds.select(d = True)

#Create IK Joints
createJoint(ikjnt_list)
cmds.select(d = True)

#Create FK Joints
createJoint(fkjnt_list)
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

fkctrl_list = [['shoulderFK_ctrl', [0, 1, 0], [0, 0, 0]], ['elbowFK_ctrl', [0, 1, 0], [0, 0, 0]], ['wristFK_ctrl', [0, 1, 0], [0, 0, 0]]]
def createfkCtrls(ctrlinfo):
    for item in ctrlinfo:
        cmds.circle(n = item[0], nr = item[1], c = item[2])
#Create FK Controls
createfkCtrls(fkctrl_list)

#Parent FK Controls to FK joints
def parentfkCtrls(ctrlinfo, jntinfo):
    for i in range(len(ctrlinfo)):
        for u in range(len(jntinfo)):
            if i == u:
                cmds.parent(ctrlinfo[i][0], jntinfo[u][0])
                cmds.setAttr(ctrlinfo[i][0] + '.translateX', 0)
                cmds.setAttr(ctrlinfo[i][0] + '.translateY', 0)
                cmds.setAttr(ctrlinfo[i][0] + '.translateZ', 0)
                cmds.setAttr(ctrlinfo[i][0] + '.rotateZ', 90)
                cmds.makeIdentity(a = True, t = 1, r = 1, s = 1, n = 0, pn = 1)
                cmds.parent(ctrlinfo[i][0], w = True)
                cmds.delete(ctrlinfo[i][0], ch = True)
                cmds.parent(ctrlinfo[i][0] + 'Shape', jntinfo[u][0], r = True, s = True)
                cmds.delete(ctrlinfo[i][0])

parentfkCtrls(fkctrl_list, fkjnt_list)


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