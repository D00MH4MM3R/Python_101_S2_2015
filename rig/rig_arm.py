import maya.cmds as cmds

ikj_list = [['ik_shoulder_jnt', [2, 0, 3], 'ctrl_ikShoulder', 'ctrl_ikShoulder_grp'], ['ik_elbow_jnt', [0, 0, 0], 'ctrl_pv_arm'], ['ik_wrist_jnt', [1, 0, -3], 'ctrl_ikWrist', 'ctrl_ikWrist_grp'], ['ik_hand_jnt', [1, 0, -4]]]
fkj_list = [['fk_shoulder_jnt', [2, 0, 3], 'ctrl_fkShoulder', 'ctrl_fkShoulder_grp'], ['fk_elbow_jnt', [0, 0, 0], 'ctrl_fkElbow', 'ctrl_fkElbow_grp'], ['fk_wrist_jnt', [1, 0, -3], 'ctrl_fkWrist', 'ctrl_fkWrist_grp'], ['fk_hand_jnt', [1, 0, -4], 'ctrl_fkHand']]
bcj_list = [['rig_shoulder_jnt', [2, 0, 3]], ['rig_elbow_jnt', [0, 0, 0]], ['rig_wrist_jnt', [1, 0, -3]], ['rig_hand_jnt', [1, 0, -4]]]

for item in ikj_list:
    cmds.joint ( n=item[0], p=item[1])
cmds.select( d=True )
for item in fkj_list:
    cmds.joint ( n=item[0], p=item[1])
cmds.select( d=True )
for item in bcj_list:
    cmds.joint ( n=item[0], p=item[1])
cmds.select( d=True )

# Create IKHandle
cmds.ikHandle( n='ikHarm', sj=ikj_list[0][0], ee=ikj_list[2][0], sol='ikRPsolver', p=2, w=1 )

# Create IK controls
# Create wrist control
# Get the position of the wrist joint
pos_wrist = cmds.xform(ikj_list[2][0], q=True, t=True, ws=True)
# Create an empty group for the wrist control
cmds.group(em=True, name=ikj_list[2][3])
# Create the wrist control
cmds.circle(n=ikj_list[2][2], nr=(0, 0, 1), c=(0, 0, 0) )
# Parent the wrist control under the empty group
cmds.parent(ikj_list[2][2], ikj_list[2][3])
# Move the group in the wrist position
cmds.xform(ikj_list[2][3], t=pos_wrist, ws=True)
# Parent the Ik Handle under the wrist control
cmds.parent('ikHarm', ikj_list[2][2])
# Create shoulder control
pos_shoulder = cmds.xform(ikj_list[0][0], q=True, t=True, ws=True)
cmds.group(em=True, name=ikj_list[0][3])
cmds.circle(n=ikj_list[0][2], nr=(0, 0, 1), c=(0, 0, 0) )
cmds.parent(ikj_list[0][2], ikj_list[0][3])
cmds.xform(ikj_list[0][3], t=pos_shoulder, ws=True)
cmds.parentConstraint( ikj_list[0][2], ikj_list[0][0], mo=True )

# Create pv control
pv_shader = cmds.shadingNode('surfaceShader', asShader=True, n='PV_shader')
cmds.setAttr ( 'PV_shader.outColor', 1, 0, 0, type="double3" )
pos_elbow = cmds.xform(ikj_list[1][0], q=True, t=True, ws=True)
cmds.sphere(n=ikj_list[1][2])
cmds.xform(ikj_list[1][2], t=pos_elbow, ws=True)
cmds.move ( -3.5, 0, 0, ws=True )
cmds.scale( 0.5, 0.5, 0.5 )
cmds.makeIdentity( apply=True, t=1, r=1, s=1 )
cmds.setAttr ( 'ctrl_pv_armShape.castsShadows', 0 )
cmds.setAttr ( 'ctrl_pv_armShape.primaryVisibility', 0 )
cmds.setAttr ( 'ctrl_pv_armShape.receiveShadows', 0 )
cmds.setAttr ( 'ctrl_pv_armShape.visibleInReflections', 0 )
cmds.setAttr ( 'ctrl_pv_armShape.visibleInRefractions', 0 )
cmds.hyperShade( assign=pv_shader )
cmds.poleVectorConstraint( ikj_list[1][2], 'ikHarm' )

for i in range(len(fkj_list)-1):
    pos_fk = cmds.xform(fkj_list[i][0], q=True, t=True, ws=True)
    cmds.group(em=True, name=fkj_list[i][3])
    cmds.circle(n=fkj_list[i][2], nr=(0, 0, 1), c=(0, 0, 0) )
    cmds.parent(fkj_list[i][2], fkj_list[i][3])
    cmds.xform(fkj_list[i][3], t=pos_fk, ws=True)
    cmds.parentConstraint( fkj_list[i][2], fkj_list[i][0], mo=True )
    del pos_fk

# Parent ctrls
# Fk
cmds.parent( fkj_list[2][3], fkj_list[1][2])
cmds.parent( fkj_list[1][3], fkj_list[0][2])
# Ik
cmds.parent( ikj_list[2][3], ikj_list[0][2])

for i in range(len(fkj_list)):
    cmds.parentConstraint(fkj_list[i][0], ikj_list[i][0], bcj_list[i][0], mo=True )
