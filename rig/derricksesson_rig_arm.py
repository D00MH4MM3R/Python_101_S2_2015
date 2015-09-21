import maya.cmds as cmds

#Create Ik joints
cmds.joint( n='ik_shoulder_jnt', p=[0.973979, 0, 6.451274])
cmds.joint( n='ik_elbow_jnt', p=[-0.552349, 0,-0.109641])
cmds.joint( n='ik_wrist_jnt', p=[1.178011, 0, -5.309904])
cmds.joint( n='ik_wristEnd_jnt', p=[1.178011, 0, -6.722549])
cmds.select(d=True)

#Create Fk joints
cmds.joint( n='fk_shoulder_jnt', p=[0.973979, 0, 6.451274])
cmds.joint( n='fk_elbow_jnt', p=[-0.552349, 0,-0.109641])
cmds.joint( n='fk_wrist_jnt', p=[1.178011, 0, -5.309904])
cmds.joint( n='fk_wristEnd_jnt', p=[1.178011, 0, -6.722549])
cmds.select(d=True)

#Create rig joints
cmds.joint( n='rig_shoulder_jnt', p=[0.973979, 0, 6.451274])
cmds.joint( n='rig_elbow_jnt', p=[-0.552349, 0,-0.109641])
cmds.joint( n='rig_wrist_jnt', p=[1.178011, 0, -5.309904])
cmds.joint( n='rig_wristEnd_jnt', p=[1.178011, 0, -6.722549])
cmds.select(d=True)

#Create Ik Rig
# Ik handle
cmds.ikHandle(n='ikh_arm', sj='ik_shoulder_jnt', ee='ik_wrist_jnt', sol="ikRPsolver", p=2, w=1 )

#Create Ik control
# Get ws position of wrist joint
pos = cmds.xform('ik_wrist_jnt', q=True, t=True, ws=True)
#Create an empty group
cmds.group(em=True, n='grp_ctrl_ikWrist')
#Create circle control
cmds.circle(n='ctrl_ikWrist', nr=(0,0,1), c=(0,0,0))
#Parent the control to group
cmds.parent('ctrl_ikWrist','grp_ctrl_ikWrist')
#move the group to the joint
cmds.xform('grp_ctrl_ikWrist', t=pos, ws=True)
#parent ikh to ctrl
cmds.parent('ikh_arm','ctrl_ikWrist')

#Create pole vector
cmds.spaceLocator(name='ik_PV')
cmds.group(em=True, n='grp_ik_PV')
cmds.parent('ik_PV','grp_ik_PV')
PVconstraint = cmds.parentConstraint('ik_elbow_jnt','grp_ik_PV', mo=False)
cmds.delete(PVconstraint)
cmds.move(-5,0,0,'grp_ik_PV', r=True)
cmds.poleVectorConstraint('ik_PV','ikh_arm')

#Create Fk Rig
#Get positon of FK joints
fkShoulderTrans = cmds.xform('fk_shoulder_jnt', q=True, t=True, ws=True)
fkElbowTrans = cmds.xform('fk_elbow_jnt', q=True, t=True, ws=True)
fkWristTrans = cmds.xform('fk_wrist_jnt', q=True, t=True, ws=True)
#Create Fk Control Curves
#Create an empty group
cmds.group(em=True, n='grp_ctrl_fkShoulder')
cmds.group(em=True, n='grp_ctrl_fkElbow')
cmds.group(em=True, n='grp_ctrl_fkWrist')
#Create circle control
cmds.circle(n='ctrl_fkShoulder', nr=(0,0,1), c=(0,0,0))
cmds.circle(n='ctrl_fkElbow', nr=(0,0,1), c=(0,0,0))
cmds.circle(n='ctrl_fkWrist', nr=(0,0,1), c=(0,0,0))
#Parent the control to group
cmds.parent('ctrl_fkShoulder','grp_ctrl_fkShoulder')
cmds.parent('ctrl_fkElbow','grp_ctrl_fkElbow')
cmds.parent('ctrl_fkWrist','grp_ctrl_fkWrist')
#move the group to the joint
cmds.xform('grp_ctrl_fkShoulder', t=fkShoulderTrans, ws=True)
cmds.xform('grp_ctrl_fkElbow', t=fkElbowTrans, ws=True)
cmds.xform('grp_ctrl_fkWrist', t=fkWristTrans, ws=True)
#parent group under hierarchy
cmds.parent('grp_ctrl_fkElbow','ctrl_fkShoulder')
cmds.parent('grp_ctrl_fkWrist','ctrl_fkElbow')
#parent constrain fk controls to fk joints
cmds.parentConstraint('ctrl_fkShoulder','fk_shoulder_jnt',mo=True)
cmds.parentConstraint('ctrl_fkElbow','fk_elbow_jnt',mo=True)
cmds.parentConstraint('ctrl_fkWrist','fk_wrist_jnt',mo=True)

#Connect Ik and Fk to Rig  joints
cmds.parentConstraint('ik_shoulder_jnt','fk_shoulder_jnt','rig_shoulder_jnt',mo=True)
cmds.parentConstraint('ik_elbow_jnt','fk_elbow_jnt','rig_elbow_jnt',mo=True)
cmds.parentConstraint('ik_wrist_jnt','fk_wrist_jnt','rig_wrist_jnt',mo=True)