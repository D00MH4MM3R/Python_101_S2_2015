import maya.cmds as cmds


#----- CREATE ARM SKELETON -----#
# I eventually want this to be a function with one of its main inputs as how many fingers are on the hand.
# I do also want to be able to decide ahead of time where the joints are placed so
# I can have non-standard proportions- kind of like how the AS rig does it, I guess.

armjntList = (['shoulder', [0,0,0]], ['elbow', [-48,12,0]], ['wrist', [-96,0,0]], ['wristEnd', [-108,0,0]])
# these are the other joints I want to add in as well, but I want to make sure I can get the main bit working first.
    # 'digit1_1','digit1_2','digit1_3','digit1_end',
    # 'digit2_1','digit2_2','digit2_3','digit2_end', 'digit3_1','digit3_2','digit3_3','digit3_end',
    # 'cup', 'digit4_1','digit4_2','digit4_3','digit4_end', 'digit5_1','digit5_2','digit5_3','digit5_end']
print armjntList
armXlist = ([])
#make the base joint chain
for item in armjntList:
    #print item[0]
    #print item[1]
    cmds.joint(n= 'rig_' + item[0] + '_jnt', p= item[1])
    #this will store the xform data for making the control joints
    armXform = cmds.xform('rig_' + item[0] + '_jnt', q=True, t=True, ws=True)
    list.append(armXlist, armXform)
cmds.select(d=True)
print armXlist

#make the IK joint chain
for item in armjntList:
    #print item[0]
    #print item[1]
    cmds.joint(n= 'IK_' + item[0] + '_jnt', p= item[1])
cmds.select(d=True)

#make the FK joint chain
for item in armjntList:
    #print item[0]
    #print item[1]
    cmds.joint(n= 'FK_' + item[0] + '_jnt', p= item[1])

#parent joint chains (wow, it actually works as expected! yeah!!)
"""
cmds.select('*shoulder_jnt')
cmds.parentConstraint()
cmds.select(d=True)

cmds.select('*elbow_jnt')
cmds.parentConstraint()
cmds.select(d=True)

cmds.select('*wrist_jnt')
cmds.parentConstraint()
cmds.select(d=True)

cmds.select('*wristEnd_jnt')
cmds.parentConstraint()
cmds.select(d=True)
"""
#gonna try another version to see if I can shorten it a bit more

for item in armjntList:
    cmds.select(item[0] + '_jnt')
    cmds.parentConstraint()
    cmds.select(d=True)
#:D it works even better!!!!

#----

#----- IK CONTROL SET -----# gonna leave this alone for now.
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
#create FK controllers and move to location

for item in armjntList:
    #print item[0]
    #print item[1]
    cmds.circle(n= 'ctl_fk_' + item[0], r=(10), nr=(0, 1, 0), c=(0, 0, 0))
    cmds.group(n='grp_ctl_fk_' + item[0])
    cmds.xform('grp_ctl_fk_' + item[0], t=item[1], ws=True)
    cmds.orientConstraint('fk_' + item[0] + '_jnt', 'grp_ctl_fk_' + item [0])
cmds.select(d=True)


#create FK controllers
#cmds.circle( n='ctl_fk_Shoulder', r=(10), nr=(0, 1, 0), c=(0, 0, 0) )
#cmds.group( 'ctl_fk_Shoulder', n='grp_ctl_fk_Shoulder' )
#cmds.circle( n='ctl_fk_Elbow', r=(10), nr=(0, 1, 0), c=(0, 0, 0) )
#cmds.group( 'ctl_fk_Elbow', n='grp_ctl_fk_Elbow' )
#cmds.circle( n='ctl_fk_Wrist', r=(10), nr=(0, 1, 0), c=(0, 0, 0) )
#cmds.group( 'ctl_fk_Wrist', n='grp_ctl_fk_Wrist' )

#move controls to locations
for item in armjntList:
    print item[0]
    print item[1]
    cmds.circle(n= 'ctl_fk_' + item[0], r=(10), nr=(1, 0, 0), c=(0, 0, 0))
    cmds.group(n='grp_ctl_fk_' + item[0])
    cmds.xform('grp_ctl_fk_' + item[0], t=item[1], ws=True)
    cmds.orientConstraint('FK_' + item[0] + '_jnt', 'grp_ctl_fk_' + item [0])
    cmds.delete('grp_ctl_fk_' +item[0] +'_orientConstraint1')
cmds.select(d=True)


#create fk control hierarchy.
cmds.parent('grp_ctl_fk_wrist','ctl_fk_elbow')
cmds.parent('grp_ctl_fk_elbow','ctl_fk_shoulder')

#constrain joints to controls
cmds.parentConstraint('ctl_fk_shoulder', 'FK_shoulder_jnt')
cmds.parentConstraint('ctl_fk_elbow', 'FK_elbow_jnt')
cmds.parentConstraint('ctl_fk_wrist', 'FK_wrist_jnt')


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
