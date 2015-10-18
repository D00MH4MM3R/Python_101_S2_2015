
# Create IK joints
cmds.joint( n='ik_shoulder_jnt', p=[2, 0, 3] )
cmds.joint( n='ik_elbow_jnt', p=[0, 0, 0] )
cmds.joint( n='ik_wrist_jnt', p=[1, 0, -3] )
cmds.joint( n='ik_hand_jnt', p=[1, 0, -4] )
cmds.select( d=True )

# Create FK joints
cmds.joint( n='fk_shoulder_jnt', p=[2, 0, 3] )
cmds.joint( n='fk_elbow_jnt', p=[0, 0, 0] )
cmds.joint( n='fk_wrist_jnt', p=[1, 0, -3] )
cmds.joint( n='fk_hand_jnt', p=[1, 0, -4] )
cmds.select( d=True )

# Create blend chain joints
cmds.joint( n='rig_shoulder_jnt', p=[2, 0, 3] )
cmds.joint( n='rig_elbow_jnt', p=[0, 0, 0] )
cmds.joint( n='rig_wrist_jnt', p=[1, 0, -3] )
cmds.joint( n='rig_hand_jnt', p=[1, 0, -4] )
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


# Create FK controls
# Shoulder ctrl
pos_shoulderfk = cmds.xform('fk_shoulder_jnt', q=True, t=True, ws=True)
cmds.group(em=True, name='ctrl_fkShoulder_grp')
cmds.circle(n='ctrl_fkShoulder', nr=(0, 0, 1), c=(0, 0, 0) )
cmds.parent('ctrl_fkShoulder', 'ctrl_fkShoulder_grp')
cmds.xform('ctrl_fkShoulder_grp', t=pos_shoulderfk, ws=True)
cmds.parentConstraint( 'ctrl_fkShoulder', 'fk_shoulder_jnt', mo=True )

# Elbow ctrl
pos_elbowfk = cmds.xform('fk_elbow_jnt', q=True, t=True, ws=True)
cmds.group(em=True, name='ctrl_fkElbow_grp')
cmds.circle(n='ctrl_fkElbow', nr=(0, 0, 1), c=(0, 0, 0) )
cmds.parent('ctrl_fkElbow', 'ctrl_fkElbow_grp')
cmds.xform('ctrl_fkElbow_grp', t=pos_elbowfk, ws=True)
cmds.parentConstraint( 'ctrl_fkElbow', 'fk_elbow_jnt', mo=True )

# Wrist ctrl
pos_wristfk = cmds.xform('fk_wrist_jnt', q=True, t=True, ws=True)
cmds.group(em=True, name='ctrl_fkWrist_grp')
cmds.circle(n='ctrl_fkWrist', nr=(0, 0, 1), c=(0, 0, 0) )
cmds.parent('ctrl_fkWrist', 'ctrl_fkWrist_grp')
cmds.xform('ctrl_fkWrist_grp', t=pos_wristfk, ws=True)
cmds.parentConstraint( 'ctrl_fkWrist', 'fk_wrist_jnt', mo=True )

# Parent ctrls
# Fk
cmds.parent( 'ctrl_fkWrist_grp', 'ctrl_fkElbow')
cmds.parent( 'ctrl_fkElbow_grp', 'ctrl_fkShoulder')
# Ik
cmds.parent( 'ctrl_ikWrist_grp', 'ctrl_ikShoulder')


# Create constraint between joint chains
cmds.parentConstraint( 'fk_shoulder_jnt', 'ik_shoulder_jnt', 'rig_shoulder_jnt', mo=True )
cmds.parentConstraint( 'fk_elbow_jnt', 'ik_elbow_jnt', 'rig_elbow_jnt', mo=True )
cmds.parentConstraint( 'fk_wrist_jnt', 'ik_wrist_jnt', 'rig_wrist_jnt', mo=True )
cmds.parentConstraint( 'fk_hand_jnt', 'ik_hand_jnt', 'rig_hand_jnt', mo=True )
