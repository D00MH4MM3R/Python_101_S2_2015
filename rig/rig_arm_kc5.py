import maya.cmds as cmds
import system.utils as utils
import os
import json


rig_data = {}

rig_data['armjnt'] = ['shoulder', 'elbow', 'wrist', 'wristEnd']
rig_data['handjnt'] = []
rig_data['pos_arm'] = [[0, 0, 0], [-48, 12, 0], [-96, 0, 0], [-96.001, 0, 0]]
rig_data['pos_digit'] = []


filename = os.environ['RIGGING_TOOL'] + '/layout/test.json'
if not os.path.exists(filename):
    print "False"
else:
    utils.writeJson(filename, rig_data)

newdata = utils.readJson(filename)
print newdata


#info = json.loads( newdata )
#for key, value in info.iteritems(newdata):
#    print key
#    print value


class Rig_Arm:
    def rigArm(self):
        # build those arms
        self.armjoint('rig', rig_data['armjnt'])
        self.armjoint('ik', rig_data['armjnt'])
        self.armjoint('fk', rig_data['armjnt'])

        # parent joint chains
        for item in rig_data['armjnt']:
            cmds.select('*' + item + '_jnt')
            cmds.parentConstraint()
            cmds.select(d=True)

        # build a hand
        self.handjoint(5, 4)

        # And this builds the arm contols
        self.armControls('fk', rig_data['armjnt'])
        self.armControls('ik', rig_data['armjnt'])

        # ----- ARM IKFK SWITCH -----#
        # create controller switch
        cmds.circle(n='ctl_IKFK_Switch', r=(20), nr=(0, 1, 0), c=(0, 0, 0))
        cmds.group('ctl_IKFK_Switch', n='grp_ctl_IKFK_Switch')
        cmds.xform('grp_ctl_IKFK_Switch', t=(-50, 0, 50), ws=True)
        # make it yellow(ish)
        cmds.color('*ctl_IKFK*', ud=2)
        # add attribute for switching
        cmds.select('ctl_IKFK_Switch')
        cmds.addAttr(longName='IK_to_FK_Switch', attributeType='double', min=0, max=10, defaultValue=0)
        cmds.setAttr('|grp_ctl_IKFK_Switch|ctl_IKFK_Switch.IK_to_FK_Switch', keyable=True)

        # key IK
        cmds.setAttr('ctl_IKFK_Switch.IK_to_FK_Switch', 10)
        self.setkeyIKFK(rig_data['armjnt'], 0, 1)
        # key FK
        cmds.setAttr('ctl_IKFK_Switch.IK_to_FK_Switch', 0)
        self.setkeyIKFK(rig_data['armjnt'], 1, 0)

    #----- CREATE ARM SKELETON -----#

    #define the base arm function
    #print "Use 'ik' or 'fk' as tags only, otherwise joint controls will not generate."
    def armjoint(self, tag, jointlist):
        if tag not in ('rig', 'ik', 'fk'):
                print "You must use 'rig', 'ik', or 'fk' as your tag."
        elif tag in ('rig', 'ik', 'fk'):
            for i in range(len(jointlist)):
                cmds.joint(n= tag + '_' + str(jointlist[i]) + '_jnt', p=rig_data['pos_arm'][i])
        cmds.select('rig_' + rig_data['armjnt'][3] + '_jnt')
        cmds.xform('rig_' + rig_data['armjnt'][3] + '_jnt', t= rig_data['pos_arm'][2], ws=True)
        cmds.select(d=True)


    #----- CREATE HAND SKELETON AND CONTROLS -----#
    #define the hand skeleton. I CAN CONTROL HOW MANY FINGERS AND JOINTS IT HAS!!!! MUAHAHAHAHAHAHAHA!

    def handjoint(self, fingers, joints):
        #determine what digits are part of the cup hierarchy
        cupped = (float(fingers) + 2) / 2.0

        #builds the fingers to specs
        #handjntList = []
        for i in range(fingers):
            j=1
            while j<=joints:
                djname = cmds.joint(n='digit'+ str(i + 1) + '_' + str(j), p = ((-4 * j) - 108, (3 * i) - 6 , 0))
                j = j+1
                djXform = cmds.xform(djname, q=True, t=True, ws=True)
                rig_data['handjnt'].append(djname)
                utils.writeJson(filename, rig_data['handjnt'])
                rig_data['pos_digit'].append(djXform)
                utils.writeJson(filename, rig_data['pos_digit'])
                cmds.rename('rig_' + djname + '_jnt')
        cmds.select('rig_digit*_1_jnt')
        cmds.parent(w=True)
        cmds.select(d=True)
        respond = utils.readJson(filename)
        print respond


        # --make cup jnt and add to handList
        cjname = cmds.joint(n='cup', p=(-106, 4, 0))
        cjXform = cmds.xform(cjname, q=True, t=True, ws=True)
        rig_data['handjnt'].append(cjname)
        utils.writeJson(filename, rig_data['handjnt'])
        rig_data['pos_digit'].append(cjXform)
        utils.writeJson(filename, rig_data['pos_digit'])
        #handjntList.append([cjname, cjXform])
        cmds.rename('rig_' + cjname + '_jnt')

        # create the handpin group
        cmds.group(n='grp_ctl_hand', em=True)
        xfer = cmds.xform('rig_' + rig_data['armjnt'][2] + '_jnt', q=True, t=True, ws=True)
        cmds.xform('grp_ctl_hand', t=xfer, ws=True)
        cmds.select(d=True)
        # fill pin group, bind to rig hand
        #cmds.parent('grp_ctl_digit1_1', 'grp_ctl_digit2_1', 'grp_ctl_digit3_1', 'grp_ctl_cup', 'grp_ctl_hand')
        #cmds.select(d=True)
        cmds.parentConstraint('rig_' + rig_data['armjnt'][3] +'_jnt', 'grp_ctl_hand', mo=True)

        #this builds the controls
        for i in range(len(rig_data['handjnt'])):
            cmds.circle(n='ctl_' + rig_data['handjnt'][i], r=(2), nr=(1, 0, 0), c=(0, 0, 0))
            cmds.group(n='SDK_grp_ctl_' + rig_data['handjnt'][i])
            cmds.group(n='grp_ctl_' + rig_data['handjnt'][i])
            cmds.xform('grp_ctl_' + rig_data['handjnt'][i], t=rig_data['pos_digit'][i], ws=True)
            cmds.orientConstraint('rig_' + rig_data['handjnt'][i] + '_jnt', 'grp_ctl_' + rig_data['handjnt'][i])
            cmds.delete('grp_ctl_' + rig_data['handjnt'][i] + '_orientConstraint1')
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
        for i in range(len(rig_data['handjnt'])):
            f = n + 1
            if f >= cupped and rig_data['handjnt'][n] == '*digit' + str(f) + '_1':
                print rig_data['handjnt'][n] + 'ring or pinky'
                # joints first
                cmds.parent('rig_digit' + str(f) + '_1_jnt', 'rig_cup_jnt')
                cmds.select(d=True)
                # controls next
                cmds.parent('grp_ctl_digit' + str(f) + '_1', 'ctl_cup')
                cmds.select(d=True)
                n = n + 1
            elif f < cupped and rig_data['handjnt'][n] == '*digit' + str(f) + '_1':
                print rig_data['handjnt'][n] + 'thumb to middle'
                # joints
                cmds.parent('rig_digit' + str(f) + '_1_jnt', 'rig_' + rig_data['armjnt'][3] + '_jnt')
                cmds.select(d=True)
                # controls
                cmds.parent('grp_ctl_digit' + str(f) + '_1', 'grp_ctl_hand')
                cmds.select(d=True)
                n = n + 1
            elif rig_data['handjnt'][n] == 'cup':
                print rig_data['handjnt'][n] + 'cup'
                cmds.parent('rig_cup_jnt', 'rig_' + rig_data['armjnt'][3] + '_jnt')
                cmds.select(d=True)
                cmds.parent('grp_ctl_cup', 'grp_ctl_hand')
                cmds.select(d=True)
                n = n + 1

        print len(rig_data['handjnt'])  # --- this is proof that 5 finger/4 jnt has 21 entries. WHY DON'T THEY WRITE TO JSON?!?!
        print rig_data['handjnt'] # --- here are all their names. i don't see where the problem's happening
        utils.writeJson(filename, rig_data['handjnt']

        # parent joints to controls
        for i in range(len(rig_data['handjnt'])):
            cmds.parentConstraint('ctl_' + rig_data['handjnt'][i], 'rig_' + rig_data['handjnt'][i] + '_jnt', mo=True)
            cmds.select(d=True)

        # get rid of end controls (can't get it to skip over them right now without breaking the hierarchy builder)
        cmds.select('grp_ctl_digit' + str(fingers) + '_' + str(joints))
        cmds.delete()

#rig_data['armjnt'] = ['shoulder', 'elbow', 'wrist', 'wristEnd']

    #-----BUILD ARM CONTROL SETS-----#
    # This function is absurdly large, but it'll do my FK and IK.
    # I really wish I had 2016 colors to choose from. Later, I'll have the colors based on what side the limb is on.
    def armControls(self, tag, jointList):
        if tag == 'fk':
            for i in range(len(jointList)):
                if jointList[i] != jointList[3]:
                    cmds.circle(n='ctl_' + tag + '_' + jointList[i], r=(10), nr=(1, 0, 0), c=(0, 0, 0))
                    cmds.group(n='grp_ctl_' + tag + '_' + jointList[i])
                    cmds.xform('grp_ctl_' + tag + '_' + jointList[i], t=rig_data['pos_arm'][i], ws=True)
                    cmds.orientConstraint(tag + '_' + jointList[i] + '_jnt', 'grp_ctl_' + tag + '_' + jointList[i])
                    cmds.delete('grp_ctl_' + tag + '_' + jointList[i] + '_orientConstraint1')
            cmds.select(d=True)
            cmds.parent('grp_ctl_' + tag + '_' + jointList[2], 'ctl_' + tag + '_' + jointList[1])
            cmds.parent('grp_ctl_' + tag + '_' + jointList[1], 'ctl_' + tag + '_' + jointList[0])
            # constrain joints to controls
            cmds.parentConstraint('ctl_fk_' + jointList[0], 'fk_' + jointList[0] + '_jnt')
            cmds.parentConstraint('ctl_fk_' + jointList[1], 'fk_' + jointList[1] + '_jnt')
            cmds.parentConstraint('ctl_fk_' + jointList[2], 'fk_' + jointList[2] + '_jnt')
            # make it blue
            cmds.color('*ctl_fk*', ud=6)
            #it won't listen and keeps making the end group, so I'm just going to kill it here for now
            #cmds.delete('grp_ctl_fk_' + jointList[3])
        elif tag == 'ik':
            for i in range(len(jointList)):
                #wrist
                if jointList[i] == jointList[2]:
                    #create grouped control
                    cmds.circle(n='ctl_' + tag + '_' + jointList[i], r=(10), nr=(1, 0, 0), c=(0, 0, 0), d=1, s=4)
                    cmds.group(n='grp_ctl_' + tag + '_' + jointList[i])
                    #move and orient at location
                    cmds.xform('grp_ctl_' + tag + '_' + jointList[i], t=rig_data['pos_arm'][2], ws=True)
                    cmds.orientConstraint(tag + '_' + jointList[i] + '_jnt', 'grp_ctl_' + tag + '_' + jointList[i])
                    cmds.delete('grp_ctl_' + tag + '_' + jointList[i] + '_orientConstraint1')
                #elbow
                elif jointList[i] == jointList[1]:
                    cmds.spaceLocator(n= 'ctl_' + tag + '_' + jointList[i] +'Aim', p=(0, 0, 0))
                    cmds.select('ctl_ik_elbowAim')
                    cmds.scale(15, 15, 15)
                    cmds.group('ctl_' + tag + '_' + jointList[i] + 'Aim', n='grp_ctl_' + tag + '_' + jointList[i] + 'Aim')
            #move to locations and orient, delete orientConstraint
            cmds.xform('grp_ctl_ik_' + rig_data['armjnt'][2] , t=rig_data['pos_arm'][2], ws=True)
            cmds.xform('grp_ctl_ik_elbowAim', t=(-50, 100, 0), ws=True)
            OC_ikwrist = cmds.orientConstraint('ik_' + rig_data['armjnt'][2] + '_jnt', 'grp_ctl_ik_' + rig_data['armjnt'][2])
            cmds.delete(OC_ikwrist)
            # create IK handle, pole vector, then parent
            cmds.ikHandle(n='ikh_arm', sj='ik_' + rig_data['armjnt'][0] + '_jnt', ee= 'ik_' + rig_data['armjnt'][2] + '_jnt', w=1, sol='ikRPsolver')
            cmds.poleVectorConstraint('ctl_ik_elbowAim', 'ikh_arm')
            cmds.parent('ikh_arm', 'ctl_ik_' + rig_data['armjnt'][2])
            cmds.parentConstraint('ctl_ik_' + rig_data['armjnt'][2], 'ik_' + rig_data['armjnt'][3] + '_jnt')
            # make it red
            cmds.color('*ctl_ik*', ud=8)
        elif tag not in ('ik', 'fk'):
            print "You must use 'ik' or 'fk' as your tag."
        cmds.select(d=True)


    #----- ARM IKFK SWITCH -----#

    #def to key parent weights
    def setkeyIKFK(self, jointlist, fkval, ikval):
        for each in jointlist:
            cmds.setAttr('rig_' + each + '_jnt_parentConstraint1.fk_' + each + '_jntW0', fkval)
            cmds.setAttr('rig_' + each + '_jnt_parentConstraint1.ik_' + each + '_jntW1', ikval)
            cmds.setDrivenKeyframe('rig_' + each + '_jnt_parentConstraint1.fk_' + each + '_jntW0',
                                   cd='ctl_IKFK_Switch.IK_to_FK_Switch')
            cmds.setDrivenKeyframe('rig_' + each + '_jnt_parentConstraint1.ik_' + each + '_jntW1',
                                   cd='ctl_IKFK_Switch.IK_to_FK_Switch')
