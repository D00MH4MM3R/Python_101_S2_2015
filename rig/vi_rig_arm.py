
import maya.cmds as cmds
#create IK joints
cmds.joint(n = 'ik_shoulder_jnt', p = [6.803994, 0, -1.223752] )
cmds.joint(n = 'ik_elbow_jnt', p = [1.607027, 0, 1.79003] )
cmds.joint(n = 'ik_wrist_jnt', p = [-5.564512, 0, -0.937867] )
cmds.joint(n = 'ik_wristEnd_jnt', p = [-8.702907, 0, -1.082102] )

cmds.select(d = True)

#create FK joints
cmds.joint(n = 'fk_shoulder_jnt', p = [6.803994, 0, -1.223752] )
cmds.joint(n = 'fk_elbow_jnt', p = [1.607027, 0, 1.79003] )
cmds.joint(n = 'fk_wrist_jnt', p = [-5.564512, 0, -0.937867] )
cmds.joint(n = 'fk_wristEnd_jnt', p = [-8.702907, 0, -1.082102] )

cmds.select(d = True)

#create rig joints
cmds.joint(n = 'rig_shoulder_jnt', p = [6.803994, 0, -1.223752] )
cmds.joint(n = 'rig_elbow_jnt', p = [1.607027, 0, 1.79003] )
cmds.joint(n = 'rig_wrist_jnt', p = [-5.564512, 0, -0.937867] )
cmds.joint(n = 'rig_wristEnd_jnt', p = [-8.702907, 0, -1.082102] )

cmds.select(d = True)

cmds.ikHandle(n = 'ikh_arm', sj = 'ik_shoulder_jnt', ee = 'ik_wrist_jnt', sol = 'ikRPsolver', p = 2, w = 0.5)

#get ws position of wrist joint
pos = cmds.xform('ik_wrist_jnt', q = True, t = True, ws = True)

#create circle control object 
cmds.circle(n = 'ctrl_ikWrist', ch = True, o = True, nr = (1,0,0), r = 1, c = (0,0,0))

#Group circle and move to ik_wrist_jnt pos
cmds.group(em = True, n = 'ctrl_grp_ikWrist')
cmds.parent('ctrl_ikWrist', 'ctrl_grp_ikWrist')
cmds.xform('ctrl_grp_ikWrist', t = pos, ws = True)

#parent ik to ctrl
cmds.parent('ikh_arm', 'ctrl_ikWrist')

#create locator for pole vector
cmds.spaceLocator(n = 'pole_vector', p=(0, 0, 0) )

#get xform of ik_elbow_jnt
elbowPos = cmds.xform('ik_elbow_jnt', q = True, t = True, ws = True)
cmds.xform('pole_vector', t = elbowPos, ws = True)

#create poly vector
cmds.select('pole_vector', r = True)
cmds.select('ikh_arm', add = True)

cmds.poleVectorConstraint(weight = 1)

cmds.select(deselect = True)


#create fk rig-----------------------------------------------------------------------------------------------------


#create circle control object 
cmds.circle(n = 'ctrl_fkElbow', ch = True, o = True, nr = (1,0,0), r = 1, c = (0,0,0))

#Group circle and move to ik_wrist_jnt pos
cmds.group(em = True, n = 'ctrl_grp_fkWrist')
cmds.parent('ctrl_fkElbow', 'ctrl_grp_fkWrist')
cmds.xform('ctrl_grp_fkWrist', t = elbowPos, ws = True)


#create orient constraint between ctrl_fkElbow and fk_elbow_jnt
cmds.orientConstraint('ctrl_fkElbow', 'fk_elbow_jnt')




#parent constrain ik_elbow_jnt to rig_elbow_jnt
cmds.parentConstraint('ik_elbow_jnt', 'rig_elbow_jnt', mo = True, weight = 1)

#parent constrain fk_elbow_jnt to rig_elbow_jnt
cmds.parentConstraint('fk_elbow_jnt', 'rig_elbow_jnt', mo = True, weight = 1)





#add IKFK blend attribute to rig_elbow_int--------------------------------------------------------
cmds.select('rig_elbow_jnt', r = True)

#add blend attribute to rig_elbow_jnt
cmds.addAttr(longName = 'IKFK_Blend', attributeType = 'float', min = 0, max = 10, dv = 0, w = True, k = True)

#set set driven keys for blend attribute

cmds.setAttr('rig_e lbow_jnt.IKFK_Blend', 0)
cmds.setAttr('rig_elbow_jnt_parentConstraint1.ik_elbow_jntW0', 0)
cmds.setAttr('rig_elbow_jnt_parentConstraint1.fk_elbow_jntW1', 1)

cmds.setDrivenKeyframe('rig_elbow_jnt_parentConstraint1.ik_elbow_jntW0', cd ='rig_e lbow_jnt.IKFK_Blend')
cmds.setDrivenKeyframe('rig_elbow_jnt_parentConstraint1.fk_elbow_jntW1', cd ='rig_e lbow_jnt.IKFK_Blend')

cmds.setAttr('rig_e lbow_jnt.IKFK_Blend', 10)
cmds.setAttr('rig_elbow_jnt_parentConstraint1.ik_elbow_jntW0', 1)
cmds.setAttr('rig_elbow_jnt_parentConstraint1.fk_elbow_jntW1', 0)

cmds.setDrivenKeyframe('rig_elbow_jnt_parentConstraint1.ik_elbow_jntW0', cd ='rig_e lbow_jnt.IKFK_Blend')
cmds.setDrivenKeyframe('rig_elbow_jnt_parentConstraint1.fk_elbow_jntW1', cd ='rig_e lbow_jnt.IKFK_Blend')

cmds.setAttr('rig_e lbow_jnt.IKFK_Blend', 0)

