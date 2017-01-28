import maya.cmds as cmds


#----- CREATE ARM SKELETON -----#
# I eventually want this to be a function with one of its main inputs as how many fingers are on the hand.
# I do also want to be able to decide ahead of time where the joints are placed so
# I can have non-standard proportions- kind of like how the AS rig does it, I guess.

armjntList = (['shoulder', [0,0,0]], ['elbow', [-48,12,0]], ['wrist', [-96,0,0]], ['wristEnd', [-108,0,0]])
digitLocationList = ( [-113, -6, 0], [-110, -6, 0], [-110, -6, 0], [-110, -6, 0])
# these are the other joints I want to add in as well, but I want to make sure I can get the main bit working first.
    # 'digit1_1','digit1_2','digit1_3','digit1_end',
    # 'digit2_1','digit2_2','digit2_3','digit2_end', 'digit3_1','digit3_2','digit3_3','digit3_end',
    # 'cup', 'digit4_1','digit4_2','digit4_3','digit4_end', 'digit5_1','digit5_2','digit5_3','digit5_end']

#below gives me all the nest numbers I need for digit names :D
"""for i in range(5):
    j=1
    while j<=4:
        print 'makes joint ' + str(j) + ' of digit ' + str(i+1)
        j = j+1"""

#this gives me all the joints, properly named for digits. wrong place, though
"""for i in range(5):
    j=1
    while j<=4:
        cmds.joint(n='digit'+ str(i + 1) + '_' + str(j) + '_jnt', p = ((-2 * i)+2, (-4 * j) - 2, 0))
        j = j+1
cmds.select('digit*_1_jnt')
cmds.parent(w=True)
cmds.select(d=True)"""
#it does spit out a warning about digit 1-1 already being parented to worldspace, but it works for now.

#this is the one for a basehand!
for i in range(5):
    j=1
    while j<=4:
        cmds.joint(n='digit'+ str(i + 1) + '_' + str(j) + '_jnt', p = ((-4 * j) - 108, (3 * i) - 6 , 0))
        j = j+1
cmds.select('digit*_1_jnt')
cmds.parent(w=True)
cmds.select(d=True)

#for proper positions
cmds.setAttr('digit1_1_jnt.tx', -104)
cmds.setAttr('digit2_1_jnt.tx', -112)
cmds.setAttr('digit3_1_jnt.tx', -113)
cmds.setAttr('digit4_1_jnt.tx', -112)
cmds.setAttr('digit5_1_jnt.tx', -109)

#make cup jnt
cmds.joint(n='cup_jnt', p = (-106, 4 , 0))

#create hierarchy
cmds.select('digit4_1_jnt', 'digit5_1_jnt', 'cup_jnt')
cmds.parent()
cmds.select('digit1_1_jnt', 'digit2_1_jnt','digit3_1_jnt', 'cup_jnt', '*wrist_jnt')
cmds.parent()



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
#I do this one 'cause I find a double wrist IK allows for a smooth IK handle and freedom with actual hand rotation.
cmds.parentConstraint('ctl_ik_Arm','IK_wristEnd_jnt')

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
#at = attribute, cd = current driver
#set the weights to FK active
"""
#wrist
cmds.setAttr('rig_wrist_jnt_parentConstraint1.IK_wrist_jntW1', 0)
cmds.setDrivenKeyframe('rig_wrist_jnt_parentConstraint1.FK_wrist_jntW0' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')
cmds.setDrivenKeyframe('rig_wrist_jnt_parentConstraint1.IK_wrist_jntW1' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')
#elbow
cmds.setAttr('rig_elbow_jnt_parentConstraint1.IK_elbow_jntW1', 0)
cmds.setDrivenKeyframe('rig_elbow_jnt_parentConstraint1.FK_elbow_jntW0' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')
cmds.setDrivenKeyframe('rig_elbow_jnt_parentConstraint1.IK_elbow_jntW1' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')
#shoulder
cmds.setAttr('rig_shoulder_jnt_parentConstraint1.IK_shoulder_jntW1', 0)
cmds.setDrivenKeyframe('rig_shoulder_jnt_parentConstraint1.FK_shoulder_jntW0' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')
cmds.setDrivenKeyframe('rig_shoulder_jnt_parentConstraint1.IK_shoulder_jntW1' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')

#-set the weights to FK active-#
cmds.setAttr('ctl_IKFK_Switch.IK_to_FK_Switch', 0)
#wrist
cmds.setAttr('rig_wrist_jnt_parentConstraint1.FK_wrist_jntW0', 1)
cmds.setAttr('rig_wrist_jnt_parentConstraint1.IK_wrist_jntW1', 0)
cmds.setDrivenKeyframe('rig_wrist_jnt_parentConstraint1.FK_wrist_jntW0' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')
cmds.setDrivenKeyframe('rig_wrist_jnt_parentConstraint1.IK_wrist_jntW1' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')
#elbow
cmds.setAttr('rig_wrist_jnt_parentConstraint1.FK_elbow_jntW0', 1)
cmds.setAttr('rig_elbow_jnt_parentConstraint1.IK_elbow_jntW1', 0)
cmds.setDrivenKeyframe('rig_elbow_jnt_parentConstraint1.FK_elbow_jntW0' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')
cmds.setDrivenKeyframe('rig_elbow_jnt_parentConstraint1.IK_elbow_jntW1' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')
#shoulder
cmds.setAttr('rig_shoulder_jnt_parentConstraint1.FK_shoulder_jntW0', 1)
cmds.setAttr('rig_shoulder_jnt_parentConstraint1.IK_shoulder_jntW1', 0)
cmds.setDrivenKeyframe('rig_shoulder_jnt_parentConstraint1.FK_shoulder_jntW0' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')
cmds.setDrivenKeyframe('rig_shoulder_jnt_parentConstraint1.IK_shoulder_jntW1' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')

#-set the weights to IK active-#
cmds.setAttr('ctl_IKFK_Switch.IK_to_FK_Switch', 10)
#wrist
cmds.setAttr('rig_wrist_jnt_parentConstraint1.FK_wrist_jntW0', 0)
cmds.setAttr('rig_wrist_jnt_parentConstraint1.IK_wrist_jntW1', 1)
cmds.setDrivenKeyframe('rig_wrist_jnt_parentConstraint1.FK_wrist_jntW0' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')
cmds.setDrivenKeyframe('rig_wrist_jnt_parentConstraint1.IK_wrist_jntW1' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')
#elbow
cmds.setAttr('rig_elbow_jnt_parentConstraint1.FK_elbow_jntW0', 0)
cmds.setAttr('rig_elbow_jnt_parentConstraint1.IK_elbow_jntW1', 1)
cmds.setDrivenKeyframe('rig_elbow_jnt_parentConstraint1.FK_elbow_jntW0' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')
cmds.setDrivenKeyframe('rig_elbow_jnt_parentConstraint1.IK_elbow_jntW1' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')
#shoulder
cmds.setAttr('rig_shoulder_jnt_parentConstraint1.FK_shoulder_jntW0', 0)
cmds.setAttr('rig_shoulder_jnt_parentConstraint1.IK_shoulder_jntW1', 1)
cmds.setDrivenKeyframe('rig_shoulder_jnt_parentConstraint1.FK_shoulder_jntW0' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')
cmds.setDrivenKeyframe('rig_shoulder_jnt_parentConstraint1.IK_shoulder_jntW1' , cd = 'ctl_IKFK_Switch.IK_to_FK_Switch')
#YESSSSS IT WORKS!!!! now to see about simplifying.
"""

#FK first
cmds.setAttr('ctl_IKFK_Switch.IK_to_FK_Switch', 0)
for each in armjntList:
    cmds.setAttr('rig_' + each[0] +'_jnt_parentConstraint1.FK_' + each[0] +'_jntW0', 1)
    cmds.setAttr('rig_' + each[0] +'_jnt_parentConstraint1.IK_' + each[0] +'_jntW1', 0)
    cmds.setDrivenKeyframe('rig_' + each[0] +'_jnt_parentConstraint1.FK_' + each[0] +'_jntW0', cd='ctl_IKFK_Switch.IK_to_FK_Switch')
    cmds.setDrivenKeyframe('rig_' + each[0] +'_jnt_parentConstraint1.IK_' + each[0] +'_jntW1', cd='ctl_IKFK_Switch.IK_to_FK_Switch')

#now IK
cmds.setAttr('ctl_IKFK_Switch.IK_to_FK_Switch', 10)
for each in armjntList:
    cmds.setAttr('rig_' + each[0] +'_jnt_parentConstraint1.FK_' + each[0] +'_jntW0', 0)
    cmds.setAttr('rig_' + each[0] +'_jnt_parentConstraint1.IK_' + each[0] +'_jntW1', 1)
    cmds.setDrivenKeyframe('rig_' + each[0] +'_jnt_parentConstraint1.FK_' + each[0] +'_jntW0', cd='ctl_IKFK_Switch.IK_to_FK_Switch')
    cmds.setDrivenKeyframe('rig_' + each[0] +'_jnt_parentConstraint1.IK_' + each[0] +'_jntW1', cd='ctl_IKFK_Switch.IK_to_FK_Switch')
#yep! this works!

