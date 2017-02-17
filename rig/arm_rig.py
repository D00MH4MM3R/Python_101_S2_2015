import maya.cmds as cmds
import maya.OpenMaya as om
import system.utils as utils
import json
import collections

class Rig_Arm:

    def __init__(self):
        self.rig_info = {}
        self.rig_data = {}
        self.layoutPos = {}
        self.sysPath = 'C:/Users/Mauricio Pachon/Documents/GitHub/Python_101_S2_2015/layout/log.json'
        self.dataPath = 'C:/Users/Mauricio Pachon/Documents/GitHub/Python_101_S2_2015/layout/data.json'

    ## Importing parameters such as names and positions ##
    def importData(self, path):
        importData = utils.readJson(self.dataPath) 
        self.rig_data = json.loads(importData)
        print 'Parameters Imported'

    ## Executing the required functions for building the arm ##
    def rig_arm(self):

        self.importData(self.dataPath)

        self.getCoords()
        
        self.rig_info['ikJnts'] = self.jointCreation(self.rig_data['prefix'][0], self.rig_data['type'][0], self.rig_data['bones'], self.layoutPos)
        
        self.rig_info['fkJnts'] = self.jointCreation(self.rig_data['prefix'][0], self.rig_data['type'][1], self.rig_data['bones'], self.layoutPos)
        
        self.rig_info['rigJnts'] = self.jointCreation(self.rig_data['prefix'][0], self.rig_data['type'][2], self.rig_data['bones'], self.layoutPos)
            
        self.rig_info['ikArm'] = self.ikSystemCreation(self.rig_info['ikJnts'][0], self.rig_info['ikJnts'][1], self.rig_info['ikJnts'][2], 'arm')
        
        self.rig_info['fkCtrls'] = self.fkSystem(self.rig_info['fkJnts'][0])
        
        self.rig_info['nodes'] = self.ikFkBlend()

        self.cleanUp()

        utils.writeJson(self.sysPath, self.rig_info)
        
    ## Get the positions from the layout objects ##
    def getCoords(self, *args):
        self.rawCoords = {}
        layoutObjs = cmds.ls(typ = 'locator')
        for l in layoutObjs:
            name = l.split('_')
            if name[0] == 'armLy':
                locTrans = cmds.listRelatives(l, p = True)
                self.rawCoords[locTrans[0]] = cmds.xform(locTrans, q = True, t = True)
                print locTrans
        
        for key, value in self.rawCoords.iteritems():
            newKey = key.split('_')
            convertedVal = []
            for v in value:
                convertedVal.append(int(v))
            self.layoutPos[newKey[1]] = convertedVal
        print self.rawCoords            
        print self.layoutPos
        print layoutObjs

        


        '''
        [self.layoutPos[l] = cmds.xform(l, q = True, t = True) if name[0] == 'armLy' for l in layoutObjs]
        '''
    ## Creating the joint chains ##
    def jointCreation(self, prefix, chainTypes, name, position):
        joints = []
        for n in name:
            #For each chain created, it then creates each joint specified in the name argument #
            joints.append(cmds.joint(n = prefix + '_' + chainTypes + '_' + n + '_jnt', p = position[n]))
            if name.index(n) != 0:
                # If the joint isnt the first one, it will orient it's parent #
                cmds.joint(prefix + '_' + chainTypes + '_' + name[name.index(n)-1] + '_jnt', e = True, zso = True, oj = 'xyz', sao = 'yup')
        cmds.select(d=True)
        return joints
    

    
    
    ## Creating the IK Arm ##
    def ikSystemCreation(self, startJoint, midJoint, endJoint, extremity):
        # Creating the IK handle    
        ikH = cmds.ikHandle( sj=startJoint, ee=endJoint, p=2, w=.5, n = extremity + '_ikHandle', sol = 'ikRPsolver')[0]
        
        # Creating the IK Arm Control   
        ikControl = cmds.circle(n = 'ctrl_IK_' + extremity, nr = (1,0,0))[0]
        ikGroup = cmds.group(ikControl, n = str(ikControl) + '_grp')
        
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
        # Query shoulder Position and Vectors
        sRaw = cmds.xform(startJoint, q = True, ws = True, t = True)
        sPos = om.MVector(sRaw[0], sRaw[1], sRaw[2])
        
        #Query Elbow Position and Vectors
        eRaw = cmds.xform(midJoint, q = True, ws = True, t = True)
        ePos = om.MVector(eRaw[0], eRaw[1], eRaw[2])
        
        #Query Wrist Position and Vectors
        wRaw = cmds.xform(endJoint, q = True, ws = True, t = True)
        wPos = om.MVector(wRaw[0], wRaw[1], wRaw[2])
        
        # Create the control
        poleVector = cmds.circle(n = 'ctrl_PV_' + extremity, nr = (0,0,1))[0]
        pvGroup = cmds.group(poleVector, n = str(poleVector) + '_grp')
        
        #Calculate the elbow spot and position it behind
        midpoint = (wPos + sPos)/2
        
        #Calculate the Pv Direction
        pvOrigin = ePos - midpoint
        
        pvRaw = pvOrigin * 2
        
        pvPos = pvRaw + midpoint
        
        cmds.move(pvPos.x, pvPos.y, pvPos.z, pvGroup)
        
        # Create PV Constraint
        cmds.poleVectorConstraint(poleVector, ikH)
        
        return ikGroup, pvGroup, ikH, ikControl, poleVector
    
    
    
    ## Creating the FK Arm Controls ##
    def fkSystem(self, startJoint):
        #Creating needed variables for naming and parenting controls in a hierarchy
        cmds.select(startJoint, hi = True)
        fkJoints = cmds.ls(sl = True)
        fkControls = []
        
        
        for f in fkJoints:
            if fkJoints.index(f) != len(fkJoints)-1:
                #Querying joint transforms for control placement.
                currentPos = cmds.xform(f, q = True, ws = True, t = True)
                currentRot = cmds.xform(f, q = True, ws = True, ro = True)
                #Splitting joint names for control naming.
                name = f.split('_')
                #Control creation.
                fkControls.append(cmds.circle(n = 'ctrl_' + name[1] + '_' + name[2], nr = (1,0,0))[0])
                currentGroup = cmds.group(fkControls[fkJoints.index(f)], n = str(fkControls[fkJoints.index(f)]) + '_grp')
                cmds.xform(currentGroup, t = currentPos, ws = True)
                cmds.xform(currentGroup, ro = currentRot, ws = True)
                #If statement: So if theres a previously created fk control, the new one gets parented under it.
                if fkJoints.index(f) >= 1:
                    cmds.parent(currentGroup, fkControls[fkJoints.index(f)-1])
                #Constraining control to joint    
                cmds.parentConstraint(fkControls[fkJoints.index(f)], f, mo = True)
                del name
                cmds.select(d=True)
        return fkControls
               
    
        
    def ikFkBlend(self, *args):
        
        # Binding both chains to target chain and creating blend control.
        tgJoints = self.rig_info['rigJnts']
        
        # Creating an IK FK blend control
        switchControl = cmds.circle(n = 'ctrl_IkFk_Switch', nr = (0,1,0))
        switchGroup = cmds.group(switchControl, n = switchControl[0] + '_grp')
        cmds.move(0,0,-3, switchGroup)
        
        #Creating the IK FK Blend Attribute
        cmds.addAttr(switchControl, ln = 'ikFk_Switch', at = 'float', k = True, min = 0, max = 1)
        
        nodes = []
        #Creating blend colors nodes and connecting the ik and fk chains to the target chain
        for t in tgJoints:
            nodeName = t.split('_')
            currentNode = cmds.shadingNode('blendColors', n = nodeName[2] + 'Blend_bc', au = True)
            nodes.append(currentNode)
            cmds.connectAttr(str(switchControl[0]) + '.ikFk_Switch', str(currentNode) + '.blender')
            cmds.connectAttr(self.rig_info['ikJnts'][tgJoints.index(t)] + '.rotate', currentNode + '.color1')            
            cmds.connectAttr(self.rig_info['fkJnts'][tgJoints.index(t)] + '.rotate', currentNode + '.color2')
            cmds.connectAttr(currentNode + '.output', t + '.rotate')
    
        return nodes



    def cleanUp(self, *args):
        #Cleaning up the Outliner and Scene
        ikCGroup = cmds.group(self.rig_info['ikArm'][0], self.rig_info['ikArm'][1], n = 'ikControls_grp')
        jntsGrp = cmds.group(self.rig_info['ikJnts'][0], self.rig_info['fkJnts'][0], self.rig_info['rigJnts'][0], n = 'joints_grp')
        ikHGroup = cmds.group(self.rig_info['ikArm'][2], n = 'nodes_grp')
        cmds.group(ikCGroup, jntsGrp, ikHGroup, 'ctrl_FK_shoulder_grp', 'ctrl_IkFk_Switch_grp', n = 'arm_grp')
        cmds.select(d=True)
        cmds.setAttr(str(self.rig_info['ikJnts'][0]) +'.visibility', 0)
        cmds.setAttr(str(self.rig_info['fkJnts'][0]) + '.visibility', 0)

        #Control Visibility
        cmds.setDrivenKeyframe('ctrl_FK_shoulder_grp.visibility', cd = 'ctrl_IkFk_Switch.ikFk_Switch', dv = 0, v = 1 )
        cmds.setDrivenKeyframe('ctrl_FK_shoulder_grp.visibility', cd = 'ctrl_IkFk_Switch.ikFk_Switch',  dv = 1, v = 0 )
        cmds.setDrivenKeyframe('ikControls_grp.visibility', cd = 'ctrl_IkFk_Switch.ikFk_Switch',  dv = 1, v = 1 )
        cmds.setDrivenKeyframe('ikControls_grp.visibility', cd = 'ctrl_IkFk_Switch.ikFk_Switch',  dv = 0, v = 0 )