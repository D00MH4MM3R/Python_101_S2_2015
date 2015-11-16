ikj_list = [['ik_shoulder_jnt', [2, 0, 3]], ['ik_elbow_jnt', [0, 0, 0]], ['ik_wrist_jnt', [1, 0, -3]], ['ik_hand_jnt', [1, 0, -4]]]
fkj_list = [['fk_shoulder_jnt', [2, 0, 3], 'ctrl_fkShoulder'], ['fk_elbow_jnt', [0, 0, 0], 'ctrl_fkElbow'], ['fk_wrist_jnt', [1, 0, -3], 'ctrl_fkWrist'], ['fk_hand_jnt', [1, 0, -4], 'ctrl_fkHand']]
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
cmds.ikHandle( n='ikHarm', sj='ik_shoulder_jnt', ee='ik_wrist_jnt', sol='ikRPsolver', p=2, w=1 )

# Create IK controls
# Create wrist control
# Get the position of the wrist joint
pos_wrist = cmds.xform('ik_wrist_jnt', q=True, t=True, ws=True)
# Create an empty group for the wrist control
cmds.group(em=True, name='ctrl_ikWrist_grp')
# Create the wrist control
cmds.circle(n='ctrl_ikWrist', nr=(0, 0, 1), c=(0, 0, 0) )
# Parent the wrist control under the empty group
cmds.parent('ctrl_ikWrist', 'ctrl_ikWrist_grp')
# Move the group in the wrist position
cmds.xform('ctrl_ikWrist_grp', t=pos_wrist, ws=True)
# Parent the Ik Handle under the wrist control
cmds.parent('ikHarm', 'ctrl_ikWrist')

# Create shoulder control
pos_shoulder = cmds.xform('ik_shoulder_jnt', q=True, t=True, ws=True)
cmds.group(em=True, name='ctrl_ikShoulder_grp')
cmds.circle(n='ctrl_ikShoulder', nr=(0, 0, 1), c=(0, 0, 0) )
cmds.parent('ctrl_ikShoulder', 'ctrl_ikShoulder_grp')
cmds.xform('ctrl_ikShoulder_grp', t=pos_shoulder, ws=True)
cmds.parentConstraint( 'ctrl_ikShoulder', 'ik_shoulder_jnt', mo=True )

# Create pv control
pv_shader = cmds.shadingNode('surfaceShader', asShader=True, n='PV_shader')
cmds.setAttr ( 'PV_shader.outColor', 1, 0, 0, type="double3" )
pos_elbow = cmds.xform('ik_elbow_jnt', q=True, t=True, ws=True)
cmds.sphere(n='ctrl_pv_arm')
cmds.xform('ctrl_pv_arm', t=pos_elbow, ws=True)
cmds.move ( -3.5, 0, 0, ws=True )
cmds.scale( 0.5, 0.5, 0.5 )
cmds.makeIdentity( apply=True, t=1, r=1, s=1 )
cmds.setAttr ( 'ctrl_pv_armShape.castsShadows', 0 )
cmds.setAttr ( 'ctrl_pv_armShape.primaryVisibility', 0 )
cmds.setAttr ( 'ctrl_pv_armShape.receiveShadows', 0 )
cmds.setAttr ( 'ctrl_pv_armShape.visibleInReflections', 0 )
cmds.setAttr ( 'ctrl_pv_armShape.visibleInRefractions', 0 )
cmds.hyperShade( assign=pv_shader )
cmds.poleVectorConstraint( 'ctrl_pv_arm', 'ikHarm' )

for i in range(len(fkj_list)-1):
    pos_fk = cmds.xform(fkj_list[i][0], q=True, t=True, ws=True)
    cmds.group(em=True, name=str(fkj_list[i][2])+'_grp')
    cmds.circle(n=fkj_list[i][2], nr=(0, 0, 1), c=(0, 0, 0) )
    cmds.parent(fkj_list[i][2], str(fkj_list[i][2])+'_grp')
    cmds.xform(str(fkj_list[i][2])+'_grp', t=pos_fk, ws=True)
    cmds.parentConstraint( fkj_list[i][2], fkj_list[i][0], mo=True )
    del pos_fk

# Parent ctrls
# Fk
cmds.parent( 'ctrl_fkWrist_grp', 'ctrl_fkElbow')
cmds.parent( 'ctrl_fkElbow_grp', 'ctrl_fkShoulder')
# Ik
cmds.parent( 'ctrl_ikWrist_grp', 'ctrl_ikShoulder')

for i in range(len(fkj_list)):
    cmds.parentConstraint(fkj_list[i][0], ikj_list[i][0], bcj_list[i][0], mo=True )
