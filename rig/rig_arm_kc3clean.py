import maya.cmds as cmds

#----- CREATE ARM SKELETON -----#
armjntList = (['shoulder', [0,0,0]], ['elbow', [-48,12,0]], ['wrist', [-96,0,0]], ['wristEnd', [-96.001,0,0]])

#define the base arm function
print "Use 'ik' or 'fk' as tags only, otherwise joint controls will not generate."
def armjoint(tag, jointlist):
    if tag not in ('rig', 'ik', 'fk'):
        print "You must use 'rig', 'ik', or 'fk' as your tag."
    elif tag in ('rig', 'ik', 'fk'):
        for item in jointlist:
          cmds.joint(n= tag + '_' + item[0] + '_jnt', p=item[1])
    cmds.select('*wristEnd*')
    cmds.xform('*wristEnd*', t=jointlist[3][1], ws=True)
    cmds.select(d=True)

#build those arms
armjoint('rig', armjntList)
armjoint('ik', armjntList)
armjoint('fk', armjntList)

#parent joint chains
for item in armjntList:
    cmds.select('*' + item[0] + '_jnt')
    cmds.parentConstraint()
    cmds.select(d=True)

#----- CREATE HAND SKELETON AND CONTROLS -----#
#define the hand skeleton. I CAN CONTROL HOW MANY FINGERS AND JOINTS IT HAS!!!! MUAHAHAHAHAHAHAHA!
handjntList = []
def handjoint(fingers, joints):
    #determine what digits are part of the cup hierarchy
    cupped = (float(fingers) + 2) / 2.0

    #builds the fingers to specs
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

    # --make cup jnt and add to handList
    cjname = cmds.joint(n='cup', p=(-106, 4, 0))
    cjXform = cmds.xform(cjname, q=True, t=True, ws=True)
    handjntList.append([cjname, cjXform])
    cmds.rename('rig_' + cjname + '_jnt')

    # create the handpin group
    cmds.group(n='grp_ctl_hand', em=True)
    xfer = cmds.xform('rig_wrist_jnt', q=True, t=True, ws=True)
    cmds.xform('grp_ctl_hand', t=xfer, ws=True)
    cmds.select(d=True)
    # fill pin group, bind to rig hand
    #cmds.parent('grp_ctl_digit1_1', 'grp_ctl_digit2_1', 'grp_ctl_digit3_1', 'grp_ctl_cup', 'grp_ctl_hand')
    #cmds.select(d=True)
    cmds.parentConstraint('rig_wristEnd_jnt', 'grp_ctl_hand', mo=True)

    #this builds the controls
    for item in handjntList:
        cmds.circle(n='ctl_' + item[0], r=(2), nr=(1, 0, 0), c=(0, 0, 0))
        cmds.group(n='SDK_grp_ctl_' + item[0])
        cmds.group(n='grp_ctl_' + item[0])
        cmds.xform('grp_ctl_' + item[0], t=item[1], ws=True)
        cmds.orientConstraint('rig_' + item[0] + '_jnt', 'grp_ctl_' + item[0])
        cmds.delete('grp_ctl_' + item[0] + '_orientConstraint1')
    cmds.select(d=True)
    # this builds the hierarchy of the fingers
    for i in range(fingers):
        j = 2
        while j <= joints:
            call = 'grp_ctl_digit' + str(i + 1) + '_' + str(j)
            if call != '*' + str(joints):
                cmds.select('ctl_digit' + str(i + 1) + '_' + str(j - 1))
                cmds.parent('grp_ctl_digit' + str(i + 1) + '_' + str(j))
                j = j + 1
            elif call != joints:
                j = j + 1
    cmds.select(d=True)

    # cup hierarchy for joints and controls
    n=0
    for item in handjntList:
        f = n + 1
        if f >= cupped and item[0] == 'digit' + str(f) + '_1':
            # joints first
            cmds.parent('rig_digit' + str(f) + '_1_jnt', 'rig_cup_jnt')
            cmds.select(d=True)
            # controls next
            cmds.parent('grp_ctl_digit' + str(f) + '_1', 'ctl_cup')
            cmds.select(d=True)
            n = n + 1
        elif f < cupped and item[0] == 'digit' + str(f) + '_1':
            # joints
            cmds.parent('rig_digit' + str(f) + '_1_jnt', 'rig_wristEnd_jnt')
            cmds.select(d=True)
            # controls
            cmds.parent('grp_ctl_digit' + str(f) + '_1', 'grp_ctl_hand')
            cmds.select(d=True)
            n = n + 1
        elif item[0] == 'cup':
            cmds.parent('rig_cup_jnt', 'rig_wristEnd_jnt')
            cmds.select(d=True)
            cmds.parent('grp_ctl_cup', 'grp_ctl_hand')
            cmds.select(d=True)
            n = n + 1
    # parent joints to controls
    for item in handjntList:
        cmds.parentConstraint('ctl_' + item[0], 'rig_' + item[0] + '_jnt', mo=True)
        cmds.select(d=True)

    # get rid of end controls (can't get it to skip over them right now without breaking the hierarchy builder)
    cmds.select('grp_ctl_digit' + str(fingers) + '_' + str(joints))
    cmds.delete()

#build a hand
handjoint(5,4)

#-----BUILD ARM CONTROL SETS-----#
# This function is absurdly large, but it'll do my FK and IK.
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
        #it won't listen and keeps making the end group, so I'm just going to kill it here for now
        cmds.delete('grp_ctl_fk_wristEnd')
    elif tag == 'ik':
        for item in jointList:
            if item[0] == 'wrist':
                #create grouped control
                cmds.circle(n='ctl_' + tag + '_' + item[0], r=(10), nr=(1, 0, 0), c=(0, 0, 0), d=1, s=4)
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
    elif tag not in ('ik', 'fk'):
        print "You must use 'ik' or 'fk' as your tag."
    cmds.select(d=True)

# And this actually builds the arm contols
armControls('fk', armjntList)
armControls('ik', armjntList)

#----- ARM IKFK SWITCH -----#
# create controller switch
cmds.circle( n='ctl_IKFK_Switch', r=(20), nr=(0, 1, 0), c=(0, 0, 0) )
cmds.group( 'ctl_IKFK_Switch', n='grp_ctl_IKFK_Switch' )
cmds.xform('grp_ctl_IKFK_Switch', t=(-50,0,50), ws=True)
# make it yellow(ish)
cmds.color('*ctl_IKFK*', ud=2)
#add attribute for switching
cmds.select('ctl_IKFK_Switch')
cmds.addAttr(longName='IK_to_FK_Switch', attributeType='double', min= 0, max= 10, defaultValue= 0 )
cmds.setAttr('|grp_ctl_IKFK_Switch|ctl_IKFK_Switch.IK_to_FK_Switch', keyable = True)

#def to key parent weights
def setkeyIKFK(jointlist, fkval, ikval):
    for each in jointlist:
        cmds.setAttr('rig_' + each[0] + '_jnt_parentConstraint1.fk_' + each[0] + '_jntW0', fkval)
        cmds.setAttr('rig_' + each[0] + '_jnt_parentConstraint1.ik_' + each[0] + '_jntW1', ikval)
        cmds.setDrivenKeyframe('rig_' + each[0] + '_jnt_parentConstraint1.fk_' + each[0] + '_jntW0',
                               cd='ctl_IKFK_Switch.IK_to_FK_Switch')
        cmds.setDrivenKeyframe('rig_' + each[0] + '_jnt_parentConstraint1.ik_' + each[0] + '_jntW1',
                               cd='ctl_IKFK_Switch.IK_to_FK_Switch')
# key IK
cmds.setAttr('ctl_IKFK_Switch.IK_to_FK_Switch', 10)
setkeyIKFK(armjntList, 0, 1)
#key FK
cmds.setAttr('ctl_IKFK_Switch.IK_to_FK_Switch', 0)
setkeyIKFK(armjntList, 1, 0)
