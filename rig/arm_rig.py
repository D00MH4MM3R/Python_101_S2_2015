import maya.cmds as cmds

## Creating the 3 joint chains ##
def jointCreation(prefix, chainTypes, name, position):
    # Takes the chainType argument and uses it to create the amount of chains we want #
    for c in chainTypes:
        counter = 0
        for n in name:
            #For each chain created, it then creates each joint specified in the name argument #            
            cmds.joint(n = prefix + '_' + c + '_' + n + '_jnt', p = position[counter])
            counter += 1
            if counter >= 1:
                # If the joint isnt the first one, it will orient it's parent #
                cmds.joint(prefix + '_' + c + '_' + name[counter - 1] + '_jnt', e = True, zso = True, oj = 'xyz', sao = 'yup')
        cmds.select(d=True)


jointCreation('c', ['IK', 'FK', 'TG'], ['shoulder', 'elbow', 'wrist', 'endWrist'], [[0, 0, 0], [7, 0, -1], [14, 0, 0], [15, 0, 0]])


## Creating the IK Arm ##
def ikSystemCreation(startJoint, endJoint, extremity):
    # Creating the IK handle
    
    ikH = cmds.ikHandle( sj=startJoint, ee=endJoint, p=2, w=.5, n = extremity + '_ikHandle')[0]
    
    # Creating the IK Arm Control
    
    ikControl = cmds.circle(n = 'ctrl_IK_' + extremity, nr = (1,0,0))
    ikGroup = cmds.group(ikControl, n = str(ikControl[0]) + '_grp')
    # Query wrist location and rotation
    pos = cmds.xform(endJoint, ws = True, q=True, t=True)
    rot = cmds.xform(endJoint, ws = True, q=True, ro=True)
    
    # Snap the group to the wrist joint
    cmds.xform(ikGroup, t=pos, ws=True)
    cmds.xform(ikGroup, ro=rot, ws=True)
    
    # Constrain the handle to the control, and the control to the wrist rotation
    
    cmds.pointConstraint(ikControl, ikH, mo=True)
    cmds.orientConstraint(ikControl, endJoint, mo=True)
    
    # Creating and Positioning PV
    # Query shoulder position
    sPos = cmds.xform(startJoint, q = True, ws = True, t = True)
    # Create the control
    poleVector = cmds.circle(n = 'ctrl_PV_' + extremity, nr = (0,0,1))
    pvGroup = cmds.group(poleVector, n = str(poleVector[0]) + '_grp')
    
    #Calculate the elbow spot and position it behind
    midpoint = (pos[0] + sPos[0])/2
    
    cmds.move(midpoint, 0, -3, pvGroup)
    
    # Create PV Constraint
    cmds.poleVectorConstraint(poleVector, ikH)
    
    return ikGroup, pvGroup, ikH

ikArm = ikSystemCreation('c_IK_shoulder_jnt', 'c_IK_wrist_jnt', 'arm')

## Creating the FK Arm Controls ##
def fkSystem(startJoint):
    #Creating needed variables for naming and parenting controls in a hierarchy
    cmds.select(startJoint, hi = True)
    fkJoints = cmds.ls(sl = True)
    fkControls = []
    counter = 0
    
    
    for f in fkJoints:
        if counter != 3:
            #Querying joint transforms for control placement.
            currentPos = cmds.xform(f, q = True, ws = True, t = True)
            currentRot = cmds.xform(f, q = True, ws = True, ro = True)
            #Splitting joint names for control naming.
            name = f.split('_')
            #Control creation.
            currentControl = cmds.circle(n = 'ctrl_' + name[1] + '_' + name[2], nr = (1,0,0))[0]
            fkControls.append( currentControl )
            currentGroup = cmds.group(currentControl, n = str(currentControl) + '_grp')
            cmds.xform(currentGroup, t = currentPos, ws = True)
            cmds.xform(currentGroup, ro = currentRot, ws = True)
            #If statement: So if theres a previously created fk control, the new one gets parented under it.
            if counter >= 1:
                cmds.parent(currentGroup, fkControls[counter-1])
            #Constraining control to joint    
            cmds.parentConstraint(currentControl, f, mo = True)
            del name
            cmds.select(d=True)
            counter += 1
            
fkSystem('c_FK_shoulder_jnt')
    
# Binding both chains to target chain and creating blend control.

cmds.select('c_TG_shoulder_jnt', hi = True)
tgJoints = cmds.ls(sl = True)

# Creating an IK FK blend control
switchControl = cmds.circle(n = 'ctrl_IkFk_Switch', nr = (0,1,0))
switchGroup = cmds.group(switchControl, n = str(switchControl[0]) + '_grp')
cmds.move(0,0,-3, switchGroup)

#Creating the IK FK Blend Attribute
cmds.addAttr(switchControl, ln = 'ikFk_Switch', at = 'float', k = True, min = 0, max = 1)


#Creating blend colors nodes and connecting the ik and fk chains to the target chain
for t in tgJoints:
    nodeName = t.split('_')
    currentNode = cmds.shadingNode('blendColors', n = nodeName[2] + 'blend_bc', au = True)
    cmds.connectAttr(str(switchControl[0]) + '.ikFk_Switch', str(currentNode) + '.blender')
    cmds.connectAttr('c_IK_' +nodeName[2]+ '_jnt.rotateX', currentNode + '.color1R')
    cmds.connectAttr('c_IK_' +nodeName[2]+ '_jnt.rotateY', currentNode + '.color1G')
    cmds.connectAttr('c_IK_' +nodeName[2]+ '_jnt.rotateZ', currentNode + '.color1B')
    cmds.connectAttr('c_FK_' +nodeName[2]+ '_jnt.rotateX', currentNode + '.color2R')
    cmds.connectAttr('c_FK_' +nodeName[2]+ '_jnt.rotateY', currentNode + '.color2G')
    cmds.connectAttr('c_FK_' +nodeName[2]+ '_jnt.rotateZ', currentNode + '.color2B')
    cmds.connectAttr(currentNode + '.output.outputR', 'c_TG_' +nodeName[2]+ '_jnt.rotateX')
    cmds.connectAttr(currentNode + '.output.outputG', 'c_TG_' +nodeName[2]+ '_jnt.rotateY')
    cmds.connectAttr(currentNode + '.output.outputB', 'c_TG_' +nodeName[2]+ '_jnt.rotateZ')
    
#Cleaning up the Outliner and Scene
ikCGroup = cmds.group(ikArm[0], ikArm[1], n = 'ikControls_grp')
jntsGrp = cmds.group('c_IK_shoulder_jnt', 'c_FK_shoulder_jnt', 'c_TG_shoulder_jnt', n = 'joints_grp')
ikHGroup = cmds.group(ikArm[2], n = 'nodes_grp')
cmds.group(ikCGroup, jntsGrp, ikHGroup, 'ctrl_FK_shoulder_grp', 'ctrl_IkFk_Switch_grp', n = 'arm_grp')
cmds.select(d=True)
cmds.setAttr('c_IK_shoulder_jnt.visibility', 0)
cmds.setAttr('c_FK_shoulder_jnt.visibility', 0)

#Control Visibility
cmds.setDrivenKeyframe('ctrl_FK_shoulder_grp.visibility', cd = 'ctrl_IkFk_Switch.ikFk_Switch', dv = 0, v = 1 )
cmds.setDrivenKeyframe('ctrl_FK_shoulder_grp.visibility', cd = 'ctrl_IkFk_Switch.ikFk_Switch',  dv = 1, v = 0 )
cmds.setDrivenKeyframe('ikControls_grp.visibility', cd = 'ctrl_IkFk_Switch.ikFk_Switch',  dv = 1, v = 1 )
cmds.setDrivenKeyframe('ikControls_grp.visibility', cd = 'ctrl_IkFk_Switch.ikFk_Switch',  dv = 0, v = 0 )