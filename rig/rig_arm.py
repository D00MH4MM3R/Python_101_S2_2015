'''
Rhonda Ray

Description:
   Creating IK/FK arm rig

'''

import pymel.core as pm

print 'Starting IK-FK Arm Rig...'

# creating joint position based on manual creation values
# create IK joints
pm.joint(name="ik_shoulder_jnt", position=[-7, 0, 2], radius=.5)
pm.joint(name="ik_elbow_jnt", position=[-1, 0, 0], radius=.5)
pm.joint(name="ik_wrist_jnt", position=[4, 0, 2], radius=.5)
pm.joint(name="ik_wristEND_jnt", position=[7, 0, 3], radius=.5)

# clear selection after each chain to create new hierarchy
pm.select(deselect=True)

# create FK joints
pm.joint(name="fk_shoulder_jnt", position=[-7, 0, 2], radius=.5)
pm.joint(name="fk_elbow_jnt", position=[-1, 0, 0], radius=.5)
pm.joint(name="fk_wrist_jnt", position=[4, 0, 2], radius=.5)
pm.joint(name="fk_wristEND_jnt", position=[7, 0, 3], radius=.5)

pm.select(deselect=True)

# create rig joints
pm.joint(name="rig_shoulder_jnt", position=[-7, 0, 2], radius=.5)
pm.joint(name="rig_elbow_jnt", position=[-1, 0, 0], radius=.5)
pm.joint(name="rig_wrist_jnt", position=[4, 0, 2], radius=.5)
pm.joint(name="rig_wristEND_jnt", position=[7, 0, 3], radius=.5)

pm.select(deselect=True)

# create IK rig
# create IK handle
pm.ikHandle(name='ikh_arm', startJoint='ik_shoulder_jnt', endEffector='ik_wrist_jnt', solver='ikRPsolver', priority=2, weight=1)

# get world space position of wrist joint
pos = pm.xform('ik_wrist_jnt', query=True, translation=True, worldSpace=True)

# create an empty group
pm.group(empty=True, name='grp_ctrl_ikWrist')

# create circle control
pm.circle(name='ctrl_ikWrist', normal=(1,0,0), center=(0,0,0), radius=1)

# parent control to group
pm.parent('ctrl_ikWrist', 'grp_ctrl_ikWrist')

# move the group to the joint
pm.xform('grp_ctrl_ikWrist', translation=pos, worldSpace=True)

# parent ik handle to wrist control
pm.parent('ikh_arm', 'ctrl_ikWrist')

# create FK rig
# get list of selected objects minus the end joint
pm.select('fk_shoulder_jnt')
selJoints = pm.ls(selection=True, dag=True)
selJoints.pop(-1)

# loop thru the selected joints
for jnt in selJoints:
	# get world space position of the joint
	pos = pm.xform(jnt, query=True, translation=True, worldSpace=True)

	# pull out the joint name, upper case the first letter and concatenate to fk
	jntName = 'fk' + jnt.split('_')[1].title()

	# create group from joint name
	grp = pm.group(name='grp_ctrl_' + jntName, empty=True)

	# create square control from joint name
	ctrl = pm.circle(name='ctrl_' + jntName, normal=(1,0,0), center=(0,0,0), radius=1.5)
	
	# parent control to grp
	# Warning: Cannot parent components or objects in the underworld
	pm.parent(ctrl, grp)

	# move group to joint
	pm.xform(grp, translation=pos, worldSpace=True)

	# constrain joint to control
	pm.parentConstraint(ctrl, jnt, maintainOffset=True)

# connect IK and FK to rig joints
# select all three joint chains and group together
pm.select('rig_shoulder_jnt', replace=True)
pm.select('fk_shoulder_jnt', add=True)
pm.select('ik_shoulder_jnt', add=True)
pm.group(name='grp_arm')

# select same joint from each arm and add orient constraint
pm.orientConstraint('fk_shoulder_jnt', 'rig_shoulder_jnt')
pm.orientConstraint('ik_shoulder_jnt', 'rig_shoulder_jnt')

pm.orientConstraint('fk_elbow_jnt', 'rig_elbow_jnt')
pm.orientConstraint('ik_elbow_jnt', 'rig_elbow_jnt')

pm.orientConstraint('fk_wrist_jnt', 'rig_wrist_jnt')
pm.orientConstraint('ik_wrist_jnt', 'rig_wrist_jnt')

# create control hierarchy
pm.parent('grp_ctrl_fkWrist', 'ctrl_fkElbow')
pm.parent('grp_ctrl_fkElbow', 'ctrl_fkShoulder')

print 'end of script'
