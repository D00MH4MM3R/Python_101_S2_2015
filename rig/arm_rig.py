import maya.cmds as cmds
import maya.OpenMaya as om
import system.utils as utils
import system.rig_utils as rig_utils
import os
import json

class Rig_Arm:

    def __init__(self):
        self.rig_info = {}
        self.rig_data = {}
        self.layoutPos = {}
        self.stretch = cmds.checkBox('stretchBox', q = True, v = True)
        self.sysPath =  os.environ["RDOJO_DATA"] + 'layout/log.json'
        self.dataPath = os.environ["RDOJO_DATA"] + 'layout/data.json'

    ## Importing parameters such as names and positions ##
    def importData(self, path):
        importData = utils.readJson(self.dataPath) 
        self.rig_data = json.loads(importData)
        print 'Parameters Imported'

    ## Executing the required functions for building the arm ##
    def rig_arm(self):
        reload(rig_utils)

        self.importData(self.dataPath)

        self.getCoords()
        
        self.rig_info['ikJnts'] = rig_utils.jointCreation(self.rig_data['prefix'][0], self.rig_data['type'][0], self.rig_data['bones'], self.layoutPos)
        
        self.rig_info['fkJnts'] = rig_utils.jointCreation(self.rig_data['prefix'][0], self.rig_data['type'][1], self.rig_data['bones'], self.layoutPos)
        
        self.rig_info['rigJnts'] = rig_utils.jointCreation(self.rig_data['prefix'][0], self.rig_data['type'][2], self.rig_data['bones'], self.layoutPos)
            
        self.rig_info['ikArm'] = rig_utils.ikSystemCreation(self.rig_info['ikJnts'][0], self.rig_info['ikJnts'][1], self.rig_info['ikJnts'][2], self.rig_data['ext'][0])
        
        self.rig_info['fkCtrls'] = self.fkSystem(self.rig_info['fkJnts'][0])
        
        self.rig_info['nodes'] = self.ikFkBlend()

        self.cleanUp()

        utils.colOverride(self.rig_data['ext'][0], (self.rig_info['ikArm'][3], self.rig_info['ikArm'][4], self.rig_info['fkCtrls']))

        if self.stretch == 1:
            self.rig_info['stretchNodes'] = rig_utils.stretchNodes(self.rig_data['prefix'][0], self.rig_info['ikJnts'][0], self.rig_info['ikJnts'][1], self.rig_info['ikJnts'][2], self.rig_info['ikArm'][3], self.rig_info['rigJnts'], self.rig_data['ext'][0])

        utils.writeJson(self.sysPath, self.rig_info)
        
    ## Get the positions from the layout objects ##
    def getCoords(self, *args):
        # Select all the layout objects by type#
        layoutObjs = cmds.ls(typ = 'joint')
        for l in layoutObjs:
            #Check to see if they should be taken into account for the arm#
            name = l.split('_')[0]
            if name == 'armLy':
                #List their transform node and query their position#
                #locTrans = cmds.listRelatives(l, p = True)[0]
                name = l.split('_')[1]
                self.layoutPos[name] = cmds.xform(l, ws = True, q = True, t = True)
    
    
    
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


