import maya.cmds as cmds


#----- CREATE ARM SKELETON -----#
#make the main joint chain
cmds.joint(n='rig_shoulder_jnt', p= (0,-48,0) )
cmds.joint(n='rig_elbow_jnt', p= (-12,0,0) )
cmds.joint(n='rig_wrist_jnt', p= (0,48,0) )
cmds.joint(n='rig_wristEnd_jnt', p= (0,60,0) )
cmds.select(d=True)

#make the IK joint chain
cmds.joint(n='ik_shoulder_jnt', p= (0,-48,0) )
cmds.joint(n='ik_elbow_jnt', p= (-12,0,0) )
cmds.joint(n='ik_wrist_jnt', p= (0,48,0) )
cmds.joint(n='ik_wristEnd_jnt', p= (0,60,0) )
cmds.select(d=True)

#make the FK joint chain
cmds.joint(n='fk_shoulder_jnt', p= (0,-48,0) )
cmds.joint(n='fk_elbow_jnt', p= (-12,0,0) )
cmds.joint(n='fk_wrist_jnt', p= (0,48,0) )
cmds.joint(n='fk_wristEnd_jnt', p= (0,60,0) )
cmds.select(d=True)

#parent joint chains
cmds.parentConstraint('fk_shoulder_jnt','ik_shoulder_jnt', 'rig_shoulder_jnt')
cmds.parentConstraint('fk_elbow_jnt','ik_elbow_jnt', 'rig_elbow_jnt')
cmds.parentConstraint('fk_wrist_jnt','ik_wrist_jnt', 'rig_wrist_jnt')
cmds.parentConstraint('fk_wristEnd_jnt','ik_wristEnd_jnt', 'rig_wristEnd_jnt')


#----- IK CONTROL SET -----#
#create IK controllers
cmds.circle( n='ctl_ik_ElbowAim', r=(10), nr=(1, 0, 0), c=(0, 0, 0) )
cmds.group( 'ctl_ik_ElbowAim', n='grp_ctl_ik_ElbowAim' )
cmds.circle(n='ctl_ik_Arm', r=(10), nr=(0, 1, 0), c=(0, 0, 0) )
cmds.group('ctl_ik_Arm', n='grp_ctl_ik_Arm')

#move controls to locations
ikWristPos=cmds.xform('ik_wrist_jnt', q=True, t=True, ws=True)
cmds.xform('grp_ctl_ik_Arm', t=ikWristPos, ws=True)
cmds.xform('grp_ctl_ik_ElbowAim', t=(-100,0,0), ws=True)

#orient wrist control
OC_ikwrist = cmds.orientConstraint( 'ik_wrist_jnt', 'grp_ctl_ik_Arm')
cmds.delete(OC_ikwrist)

#create IK handle, pole vector
cmds.ikHandle( n='ikh_arm', sj='ik_shoulder_jnt', ee='ik_wrist_jnt', w=1, sol='ikRPsolver')
cmds.poleVectorConstraint( 'ctl_ik_ElbowAim', 'ikh_arm' )
cmds.parent( 'ikh_arm', 'ctl_ik_Arm' )


#----- FK CONTROL SET -----#
#create FK controllers
cmds.circle( n='ctl_fk_Shoulder', r=(10), nr=(0, 1, 0), c=(0, 0, 0) )
cmds.group( 'ctl_fk_Shoulder', n='grp_ctl_fk_Shoulder' )
cmds.circle( n='ctl_fk_Elbow', r=(10), nr=(0, 1, 0), c=(0, 0, 0) )
cmds.group( 'ctl_fk_Elbow', n='grp_ctl_fk_Elbow' )
cmds.circle( n='ctl_fk_Wrist', r=(10), nr=(0, 1, 0), c=(0, 0, 0) )
cmds.group( 'ctl_fk_Wrist', n='grp_ctl_fk_Wrist' )

#move controls to locations
fkShoulderPos=cmds.xform('fk_shoulder_jnt', q=True, t=True, ws=True)
cmds.xform('grp_ctl_fk_Shoulder', t=fkShoulderPos, ws=True)
fkElbowPos=cmds.xform('fk_elbow_jnt', q=True, t=True, ws=True)
cmds.xform('grp_ctl_fk_Elbow', t=fkElbowPos, ws=True)
fkWristPos=cmds.xform('fk_wrist_jnt', q=True, t=True, ws=True)
cmds.xform('grp_ctl_fk_Wrist', t=fkWristPos, ws=True)

#orient controls
OC_fkshoulder = cmds.orientConstraint( 'fk_shoulder_jnt', 'grp_ctl_fk_Shoulder')
cmds.delete(OC_fkshoulder)
OC_fkelbow = cmds.orientConstraint( 'fk_elbow_jnt', 'grp_ctl_fk_Elbow')
cmds.delete(OC_fkelbow)
OC_fkwrist = cmds.orientConstraint( 'fk_wrist_jnt', 'grp_ctl_fk_Wrist')
cmds.delete(OC_fkwrist)

#create fk control hierarchy
cmds.parent('grp_ctl_fk_Wrist','ctl_fk_Elbow')
cmds.parent('grp_ctl_fk_Elbow','ctl_fk_Shoulder')

#constrain joints to controls
cmds.parentConstraint('ctl_fk_Shoulder', 'fk_shoulder_jnt')
cmds.parentConstraint('ctl_fk_Elbow', 'fk_elbow_jnt')
cmds.parentConstraint('ctl_fk_Wrist', 'fk_wrist_jnt')


#----- IKFK SWITCH -----#
# create controller switch
cmds.circle( n='ctl_IKFK_Switch', r=(20), nr=(1, 0, 0), c=(0, 0, 0) )
cmds.group( 'ctl_IKFK_Switch', n='grp_ctl_IKFK_Switch' )
cmds.xform('grp_ctl_IKFK_Switch', t=(0,100,0), ws=True)

#add attribute for switching
cmds.select('ctl_IKFK_Switch')
cmds.addAttr(longName='IK_to_FK_Switch', attributeType='double', min= 0, max= 10, defaultValue= 0 )
cmds.setAttr('|grp_ctl_IKFK_Switch|ctl_IKFK_Switch.IK_to_FK_Switch', keyable = True)


#key parent weights to switch
#set fk keys
cmds.setAttr('rig_wristEnd_jnt_parentConstraint1.ik_wristEnd_jntW1', [0])

# Set an entire list of multi-attribute values in one command
cmds.setAttr( 'rig_wristEnd_jnt_parentConstraint1.ik_wristEnd_jntW1', 0)

#there's something wrong with this next bit. not sure how I need to enter the data... both versions have the same error.
#   --> Error: line 1: TypeError: file <maya console> line 1: Flag 'driven' must be passed a boolean argument
#cmds.setDrivenKeyframe(currentDriver = 'ctl_IKFK_Switch.IK_to_FK_Switch', driven = 'rig_wristEnd_jnt_parentConstraint1.fk_wristEnd_jntW0')
#cmds.setDrivenKeyframe(currentDriver = 'ctl_IKFK_Switch.IK_to_FK_Switch', 'rig_wristEnd_jnt_parentConstraint1.ik_wristEnd_jntW1')

#grabbed from MEL output
#setDrivenKeyframe -currentDriver ctl_IKFK_Switch.IK_to_FK_Switch rig_wristEnd_jnt_parentConstraint1.fk_wristEnd_jntW0;
#setDrivenKeyframe -currentDriver ctl_IKFK_Switch.IK_to_FK_Switch rig_wristEnd_jnt_parentConstraint1.ik_wristEnd_jntW1;
