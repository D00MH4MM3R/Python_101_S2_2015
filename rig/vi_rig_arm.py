"""
MEL Code:

joint -p 6.803994 0 -1.223752 ;
joint -p 1.607027 0 1.79003 ;
joint -p -5.564512 0 -0.937867 ;
joint -p -8.702907 0 -1.082102 ;

ikHandle -sol ikRPsolver;

circle -ch on -o on -nr 0 1 0 -r 1.362392 ;
move -rpr -5.564512 0 -0.937867 ;
move -5.564512 0 -0.937867 group2.scalePivot group2.rotatePivot ;
orientConstraint -offset 0 0 0 -weight 1;
select -r group2_orientConstraint1 ;
delete



"""


#create IK joints
cmds.joint(n = 'ik_shoulder_jnt', p = [6.803994, 0, -1.223752] )
cmds.joint(n = 'ik_elbow_jnt', p = [1.607027, 0, 1.79003] )
cmds.joint(n = 'ik_wrist_jnt', p = [-5.564512, 0, -0.937867] )
cmds.joint(n = 'ik_wristEnd_jnt', p = [-8.702907, 0, -1.082102] )

cmds.select(d = True)

#create FK joints
cmds.joint(n = 'fk_shoulder_jnt', p = [6.803994, 0, -1.223752] )
cmds.joint(n = 'fk_elbow_jnt', p = [1.607027, 0, 1.79003] )
cmds.joint(n = 'fk_wrist_jnt', p = [-5.564512, 0, -0.937867] )
cmds.joint(n = 'fk_wristEnd_jnt', p = [-8.702907, 0, -1.082102] )

cmds.select(d = True)

#create rig joints
cmds.joint(n = 'rig_shoulder_jnt', p = [6.803994, 0, -1.223752] )
cmds.joint(n = 'rig_elbow_jnt', p = [1.607027, 0, 1.79003] )
cmds.joint(n = 'rig_wrist_jnt', p = [-5.564512, 0, -0.937867] )
cmds.joint(n = 'rig_wristEnd_jnt', p = [-8.702907, 0, -1.082102] )

cmds.select(d = True)

cmds.ikHandle(n = 'ikh_arm', sj = 'ik_shoulder_jnt', ee = 'ik_wrist_jnt', sol = 'ikRPsolver', p = 2, w = 0.5)

#get ws position of wrist joint
pos = cmds.xform('ik_wrist_jnt', q = True, t = True, ws = True)

#create circle control object 
cmds.circle(n = 'ctrl_ikWrist', ch = True, o = True, nr = (1,0,0), r = 1, c = (0,0,0))

#Group circle and move to ik_wrist_jnt pos
cmds.group(em = True, n = 'ctrl_grp_ikWrist')
cmds.parent('ctrl_ikWrist', 'ctrl_grp_ikWrist')
cmds.xform('ctrl_grp_ikWrist', t = pos, ws = True)

#parent ik to ctrl
cmds.parent('ikh_arm', 'ctrl_ikWrist')


#create fk rig

#parent constrain ik and fk to rig





