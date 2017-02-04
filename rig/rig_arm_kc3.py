import maya.cmds as cmds

#----- CREATE ARM SKELETON -----#
armjntList = (['shoulder', [0,0,0]], ['elbow', [-48,12,0]], ['wrist', [-96,0,0]], ['wristEnd', [-96.25,0,0]])

#define the base arm function
print "Use 'ik' or 'fk' as tags only, otherwise joint controls will not generate."
def armjoint(tag, jointlist):
    for item in jointlist:
        cmds.joint(n= tag + item[0] + '_jnt', p=item[1])
    cmds.select(d=True)

#build those arms
armjoint('rig_', armjntList)
armjoint('ik_', armjntList)
armjoint('fk_', armjntList)


#define the hand skeleton. I CAN CONTROL HOW MANY FINGERS AND JOINTS IT HAS!!!! MUAHAHAHAHAHAHAHA!
handjntList = []
def handjoint(fingers, joints):
    for i in range(fingers):
        j=1
        while j<=joints:
            djname = cmds.joint(n='digit'+ str(i + 1) + '_' + str(j), p = ((-4 * j) - 108, (3 * i) - 6 , 0))
            j = j+1
            djXform = cmds.xform(djname, q=True, t=True, ws=True)
            handjntList.append([djname, djXform])
            cmds.rename('rig_' + djname + '_jnt')
    cmds.select('rig_digit*_1_jnt')
    cmds.parent(w=True)
    cmds.select(d=True)

#build a hand
handjoint(5,4)

#--for proper positions (up to 5 fingers)
#this moves the base joints to a more sensible location and updates handjntList with the new locations of
#the joint chains for adding controls later. I only built fingers for the rig skele, so I'm only running this once.
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


#-----BUILD ARM CONTROL SETS-----#

# this function is large.
# I really wish I had 2016 colors to choose from. Later, I'll have the colors based on what side the limb is on.
def armControls(tag, jointList):
    if tag == 'fk':
        for item in jointList:
            if item[0] != '*End':
                cmds.circle(n='ctl_' + tag + '_' + item[0], r=(10), nr=(1, 0, 0), c=(0, 0, 0))
                cmds.group(n='grp_ctl_' + tag + '_' + item[0])
                cmds.xform('grp_ctl_' + tag + '_' + item[0], t=item[1], ws=True)
                cmds.orientConstraint(tag + '_' + item[0] + '_jnt', 'grp_ctl_' + tag + '_' + item[0])
                cmds.delete('grp_ctl_' + tag + '_' + item[0] + '_orientConstraint1')
        cmds.select(d=True)
        cmds.parent('grp_ctl_' + tag + '_wrist', 'ctl_' + tag + '_elbow')
        cmds.parent('grp_ctl_' + tag + '_elbow', 'ctl_' + tag + '_shoulder')
        # constrain joints to controls
        cmds.parentConstraint('ctl_fk_shoulder', 'fk_shoulder_jnt')
        cmds.parentConstraint('ctl_fk_elbow', 'fk_elbow_jnt')
        cmds.parentConstraint('ctl_fk_wrist', 'fk_wrist_jnt')
        # make it blue
        cmds.color('*ctl_fk*', ud=6)
    elif tag == 'ik':
        for item in jointList:
            if item[0] == 'wrist':
                #create grouped control
                cmds.circle(n='ctl_' + tag + '_' + item[0], r=(10), nr=(1, 0, 0), c=(0, 0, 0))
                cmds.group(n='grp_ctl_' + tag + '_' + item[0])
                #move and orient at location
                cmds.xform('grp_ctl_' + tag + '_' + item[0], t=item[1], ws=True)
                cmds.orientConstraint(tag + '_' + item[0] + '_jnt', 'grp_ctl_' + tag + '_' + item[0])
                cmds.delete('grp_ctl_' + tag + '_' + item[0] + '_orientConstraint1')
            elif item[0] == 'elbow':
                cmds.spaceLocator(n= 'ctl_' + tag + '_' + item[0] +'Aim', p=(0, 0, 0))
                cmds.select('ctl_ik_elbowAim')
                cmds.scale(15, 15, 15)
                cmds.group('ctl_' + tag + '_' + item[0] + 'Aim', n='grp_ctl_' + tag + '_' + item[0] + 'Aim')
        #move to locations and orient, delete orientConstraint
        cmds.xform('grp_ctl_ik_wrist', t=item[1], ws=True)
        cmds.xform('grp_ctl_ik_elbowAim', t=(-50, 100, 0), ws=True)
        OC_ikwrist = cmds.orientConstraint('ik_wrist_jnt', 'grp_ctl_ik_wrist')
        cmds.delete(OC_ikwrist)
        # create IK handle, pole vector, then parent
        cmds.ikHandle(n='ikh_arm', sj='ik_shoulder_jnt', ee='ik_wrist_jnt', w=1, sol='ikRPsolver')
        cmds.poleVectorConstraint('ctl_ik_elbowAim', 'ikh_arm')
        cmds.parent('ikh_arm', 'ctl_ik_wrist')
        cmds.parentConstraint('ctl_ik_wrist', 'ik_wristEnd_jnt')
        # make it red
        cmds.color('*ctl_ik*', ud=8)
    cmds.select(d=True)

# this actually builds the arm contols
armControls('fk', armjntList)
armControls('ik', armjntList)












#----- ARM IKFK SWITCH -----#
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





#---- DIGIT CONTROL SET ----#
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




