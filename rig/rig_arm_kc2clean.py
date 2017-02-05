import maya.cmds as cmds

#----- CREATE ARM SKELETON -----#
armjntList = (['shoulder', [0,0,0]], ['elbow', [-48,12,0]], ['wrist', [-96,0,0]], ['wristEnd', [-96.25,0,0]])

#make the base joint chain
for item in armjntList:
    cmds.joint(n= 'rig_' + item[0] + '_jnt', p= item[1])
cmds.select(d=True)

#base hand, 5 fingers, makes a var list similar to armjntList for use later
handjntList = []
for i in range(5):
    j=1
    while j<=4:
        djname = cmds.joint(n='digit'+ str(i + 1) + '_' + str(j), p = ((-4 * j) - 108, (3 * i) - 6 , 0))
        j = j+1
        djXform = cmds.xform(djname, q=True, t=True, ws=True)
        handjntList.append([djname, djXform])
        cmds.rename('rig_' + djname + '_jnt')
cmds.select('rig_digit*_1_jnt')
cmds.parent(w=True)
cmds.select(d=True)

#--for proper positions
for i in range(len(handjntList)):
    if handjntList[i][0] == 'digit1_1':
        cmds.setAttr('rig_digit1_1_jnt.tx', -104)
        handjntList[i][1] = cmds.xform('rig_digit1_1_jnt', q=True, t=True, ws=True)
    elif handjntList[i][0] == 'digit2_1':
        cmds.setAttr('rig_digit2_1_jnt.tx', -112)
        handjntList[i][1] = cmds.xform('rig_digit2_1_jnt', q=True, t=True, ws=True)
    elif handjntList[i][0] == 'digit3_1':
        cmds.setAttr('rig_digit3_1_jnt.tx', -113)
        handjntList[i][1] = cmds.xform('rig_digit3_1_jnt', q=True, t=True, ws=True)
    elif handjntList[i][0] == 'digit4_1':
        cmds.setAttr('rig_digit4_1_jnt.tx', -112)
        handjntList[i][1] = cmds.xform('rig_digit4_1_jnt', q=True, t=True, ws=True)
    elif handjntList[i][0] == 'digit5_1':
        cmds.setAttr('rig_digit5_1_jnt.tx', -109)
        handjntList[i][1] = cmds.xform('rig_digit5_1_jnt', q=True, t=True, ws=True)
    elif handjntList[i][0] != 'digit*_1':
        handjntList[i][1] = cmds.xform('rig_' + handjntList[i][0] + '_jnt', q=True, t=True, ws=True)

# --make cup jnt and add to handList
cjname = cmds.joint(n='cup', p = (-106, 4 , 0))
cjXform = cmds.xform(cjname, q=True, t=True, ws=True)
handjntList.append([cjname, cjXform])
cmds.rename('rig_' + cjname + '_jnt')

#--create hierarchy
cmds.select('rig_digit4_1_jnt', 'rig_digit5_1_jnt', 'rig_cup_jnt')
cmds.parent()
cmds.select('rig_digit1_1_jnt', 'rig_digit2_1_jnt','rig_digit3_1_jnt', 'rig_cup_jnt', 'rig_wristEnd_jnt')
cmds.parent()
cmds.select(d=True)

#make the IK joint chain
for item in armjntList:
    cmds.joint(n= 'IK_' + item[0] + '_jnt', p= item[1])
cmds.select(d=True)

#make the FK joint chain
for item in armjntList:
    cmds.joint(n= 'FK_' + item[0] + '_jnt', p= item[1])
cmds.select(d=True)

#parent joint chains
for item in armjntList:
    cmds.select('*' + item[0] + '_jnt')
    cmds.parentConstraint()
    cmds.select(d=True)

#----- IK CONTROL SET -----# gonna leave this alone for now.
#create IK controllers
cmds.circle( n='ctl_ik_ElbowAim', r=(10), nr=(0, 1, 0), c=(0, 0, 0) )
cmds.group( 'ctl_ik_ElbowAim', n='grp_ctl_ik_ElbowAim' )
cmds.circle(n='ctl_ik_Arm', r=(10), nr=(0, 1, 0), c=(0, 0, 0) )
cmds.group('ctl_ik_Arm', n='grp_ctl_ik_Arm')

#move controls to locations
ikWristPos=cmds.xform('IK_wrist_jnt', q=True, t=True, ws=True)
cmds.xform('grp_ctl_ik_Arm', t=ikWristPos, ws=True)
cmds.xform('grp_ctl_ik_ElbowAim', t=(-50,100,0), ws=True)

#orient wrist control
OC_ikwrist = cmds.orientConstraint( 'IK_wrist_jnt', 'grp_ctl_ik_Arm')
cmds.delete(OC_ikwrist)

#create IK handle, pole vector
cmds.ikHandle( n='ikh_arm', sj='IK_shoulder_jnt', ee='IK_wrist_jnt', w=1, sol='ikRPsolver')
cmds.poleVectorConstraint( 'ctl_ik_ElbowAim', 'ikh_arm' )
cmds.parent( 'ikh_arm', 'ctl_ik_Arm' )
#I use a double IK wrist- one for the end effector and one to transfer actual wrist rotations.
#Does anyone else do this or am I on my own? How do others tackle that?
cmds.parentConstraint('ctl_ik_Arm','IK_wristEnd_jnt')


#----- FK CONTROL SET -----#
#create FK controllers and move to location

for item in armjntList:
    if item[0] != 'wristEnd':
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
cmds.circle( n='ctl_IKFK_Switch', r=(20), nr=(0, 1, 0), c=(0, 0, 0) )
cmds.group( 'ctl_IKFK_Switch', n='grp_ctl_IKFK_Switch' )
cmds.xform('grp_ctl_IKFK_Switch', t=(-50,0,50), ws=True)

#add attribute for switching
cmds.select('ctl_IKFK_Switch')
cmds.addAttr(longName='IK_to_FK_Switch', attributeType='double', min= 0, max= 10, defaultValue= 0 )
cmds.setAttr('|grp_ctl_IKFK_Switch|ctl_IKFK_Switch.IK_to_FK_Switch', keyable = True)

#key parent weights to switch
#key IK
cmds.setAttr('ctl_IKFK_Switch.IK_to_FK_Switch', 10)
for each in armjntList:
    cmds.setAttr('rig_' + each[0] +'_jnt_parentConstraint1.FK_' + each[0] +'_jntW0', 0)
    cmds.setAttr('rig_' + each[0] +'_jnt_parentConstraint1.IK_' + each[0] +'_jntW1', 1)
    cmds.setDrivenKeyframe('rig_' + each[0] +'_jnt_parentConstraint1.FK_' + each[0] +'_jntW0', cd='ctl_IKFK_Switch.IK_to_FK_Switch')
    cmds.setDrivenKeyframe('rig_' + each[0] +'_jnt_parentConstraint1.IK_' + each[0] +'_jntW1', cd='ctl_IKFK_Switch.IK_to_FK_Switch')

#key FK
cmds.setAttr('ctl_IKFK_Switch.IK_to_FK_Switch', 0)
for each in armjntList:
    cmds.setAttr('rig_' + each[0] +'_jnt_parentConstraint1.FK_' + each[0] +'_jntW0', 1)
    cmds.setAttr('rig_' + each[0] +'_jnt_parentConstraint1.IK_' + each[0] +'_jntW1', 0)
    cmds.setDrivenKeyframe('rig_' + each[0] +'_jnt_parentConstraint1.FK_' + each[0] +'_jntW0', cd='ctl_IKFK_Switch.IK_to_FK_Switch')
    cmds.setDrivenKeyframe('rig_' + each[0] +'_jnt_parentConstraint1.IK_' + each[0] +'_jntW1', cd='ctl_IKFK_Switch.IK_to_FK_Switch')


#----DIGIT CONTROL SET----#
#make curves for all joints in hand
for item in handjntList:
    cmds.circle(n= 'ctl_' + item[0], r=(2), nr=(1, 0, 0), c=(0, 0, 0))
    cmds.group(n='SDK_grp_ctl_' + item[0])
    cmds.group(n='grp_ctl_' + item[0])
    cmds.xform('grp_ctl_' + item[0], t=item[1], ws=True)
    cmds.orientConstraint('rig_' + item[0] + '_jnt', 'grp_ctl_' + item [0])
    cmds.delete('grp_ctl_' + item[0] + '_orientConstraint1')
cmds.select(d=True)

# this builds the hierarchy of the fingers
for i in range(5):
    j = 2
    while j <= 4:
        call = 'grp_ctl_digit' + str(i + 1) + '_' + str(j)
        if call != '*5':
            cmds.select('ctl_digit' + str(i + 1) + '_' + str(j - 1))
            cmds.parent('grp_ctl_digit' + str(i + 1) + '_' + str(j))
            j = j + 1
        elif call != '5':
            j = j + 1
cmds.select(d=True)

# cup hierarchy
cmds.parent('grp_ctl_digit4_1', 'grp_ctl_digit5_1', 'grp_ctl_cup')
cmds.select(d=True)

# create the pin group
cmds.group(n='grp_ctl_hand', em=True)
xfer = cmds.xform('rig_wrist_jnt', q=True, t=True, ws=True)
cmds.xform('grp_ctl_hand', t=xfer, ws=True)
cmds.select(d=True)
# fill pin group, bind to rig hand
cmds.parent('grp_ctl_digit1_1', 'grp_ctl_digit2_1', 'grp_ctl_digit3_1', 'grp_ctl_cup', 'grp_ctl_hand')
cmds.select(d=True)
cmds.parentConstraint('rig_wristEnd_jnt', 'grp_ctl_hand', mo=True)

# this parents joints to controls
for item in handjntList:
    cmds.parentConstraint('ctl_' + item[0], 'rig_' + item[0] + '_jnt', mo=True)
    cmds.select(d=True)

# get rid of end controls (can't get it to skip over them right now without breaking the hierarchy builder)
cmds.select('grp_ctl_digit*_4')
cmds.delete()
