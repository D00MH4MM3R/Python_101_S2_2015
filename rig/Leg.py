import maya.cmds as cmds
import maya.OpenMaya as om
import system.utils as utils
import system.rig_utils as rig_utils
import os
import json

class Rig_Leg:

    def __init__(self):
        self.rig_info = {}
        self.rig_data = {}
        self.layoutPos = {}
        self.stretch = cmds.checkBox('stretchLegBox', q = True, v = True)
        self.sysPath =  os.environ["RDOJO_DATA"] + '/leg_log.json'
        self.dataPath = os.environ["RDOJO_DATA"] + '/leg_data.json'

    ## Importing parameters such as names and positions ##
    def importData(self, path):
        importData = utils.readJson(self.dataPath) 
        self.rig_data = json.loads(importData)
        print 'Parameters Imported'

    ## Executing the required functions for building the arm ##
    def rig_leg(self):
        reload(rig_utils)
        cmds.select(d = True)

        self.importData(self.dataPath)
        ## Build Left Arm ##
        self.getCoords('legLy', 'L')
        
        self.rig_info['ikJnts_L'] = rig_utils.jointCreation(self.rig_data['prefix'][0], self.rig_data['type'][0], self.rig_data['bones'], self.layoutPos, self.rig_data['ext'][1])
        
        self.rig_info['fkJnts_L'] = rig_utils.jointCreation(self.rig_data['prefix'][0], self.rig_data['type'][1], self.rig_data['bones'], self.layoutPos, self.rig_data['ext'][1])
        
        self.rig_info['rigJnts_L'] = rig_utils.jointCreation(self.rig_data['prefix'][0], self.rig_data['type'][2], self.rig_data['bones'], self.layoutPos, self.rig_data['ext'][1])
           
        self.rig_info['ikLeg_L'] = rig_utils.ikSystemCreation(self.rig_info['ikJnts_L'][0], self.rig_info['ikJnts_L'][1], self.rig_info['ikJnts_L'][2], self.rig_data['ext'][1])
        
        self.rig_info['fkCtrls_L'] = rig_utils.fkSystem(self.rig_info['fkJnts_L'][0])
        
        self.rig_info['nodes_L'] = self.ikFkBlend(self.rig_info['rigJnts_L'], self.rig_info['ikJnts_L'], self.rig_info['fkJnts_L'], self.rig_data['ext'][1])

        self.cleanUpLeft()

        utils.colOverride(self.rig_data['ext'][1], (self.rig_info['ikLeg_L'][3], self.rig_info['ikLeg_L'][4], self.rig_info['fkCtrls_L']))
        
        if self.stretch == 1:
            self.rig_info['stretchNodes_L'] = rig_utils.stretchNodes(self.rig_data['prefix'][0], self.rig_info['ikJnts_L'][0], self.rig_info['ikJnts_L'][1], self.rig_info['ikJnts_L'][2], self.rig_info['ikLeg_L'][3], self.rig_info['rigJnts_L'], self.rig_data['ext'][1])


        ## Build Right Arm ##
        self.getCoords('legLy', 'R')
        
        self.rig_info['ikJnts_R'] = rig_utils.jointCreation(self.rig_data['prefix'][0], self.rig_data['type'][0], self.rig_data['bones'], self.layoutPos, self.rig_data['ext'][3])
        
        self.rig_info['fkJnts_R'] = rig_utils.jointCreation(self.rig_data['prefix'][0], self.rig_data['type'][1], self.rig_data['bones'], self.layoutPos, self.rig_data['ext'][3])
        
        self.rig_info['rigJnts_R'] = rig_utils.jointCreation(self.rig_data['prefix'][0], self.rig_data['type'][2], self.rig_data['bones'], self.layoutPos, self.rig_data['ext'][3])
           
        self.rig_info['ikLeg_R'] = rig_utils.ikSystemCreation(self.rig_info['ikJnts_R'][0], self.rig_info['ikJnts_R'][1], self.rig_info['ikJnts_R'][2], self.rig_data['ext'][3])
        
        self.rig_info['fkCtrls_R'] = rig_utils.fkSystem(self.rig_info['fkJnts_R'][0])
        
        self.rig_info['nodes_R'] = self.ikFkBlend(self.rig_info['rigJnts_R'], self.rig_info['ikJnts_R'], self.rig_info['fkJnts_R'], self.rig_data['ext'][3])

        self.cleanUpRight()

        utils.colOverride(self.rig_data['ext'][3], (self.rig_info['ikLeg_R'][3], self.rig_info['ikLeg_R'][4], self.rig_info['fkCtrls_R']))
        
        if self.stretch == 1:   
            self.rig_info['stretchNodes_R'] = rig_utils.stretchNodes(self.rig_data['prefix'][0], self.rig_info['ikJnts_R'][0], self.rig_info['ikJnts_R'][1], self.rig_info['ikJnts_R'][2], self.rig_info['ikLeg_R'][3], self.rig_info['rigJnts_R'], self.rig_data['ext'][3])

        utils.writeJson(self.sysPath, self.rig_info)
        
    ## Get the positions from the layout objects ##
    def getCoords(self, ext, side):
        # Select all the layout objects by type#
        layoutObjs = cmds.ls(typ = 'joint')
        for l in layoutObjs:
            #Check to see if they should be taken into account for the arm#
            name = l.split('_')
            if name[0] == ext and name[2] == side:
                #List their transform node and query their position#
                name = l.split('_')[1]
                self.layoutPos[name] = cmds.xform(l, ws = True, q = True, t = True)
    
               
    
        
    def ikFkBlend(self, target, iksource, fksource, ext):
        
        # Binding both chains to target chain and creating blend control.
        tgJoints = target
        
        # Creating an IK FK blend control
        switchControl = cmds.circle(n = 'ctrl_' + str(ext) + '_IkFk_Switch', nr = (0,1,0))
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
            cmds.connectAttr(iksource[tgJoints.index(t)] + '.rotate', currentNode + '.color1')            
            cmds.connectAttr(fksource[tgJoints.index(t)] + '.rotate', currentNode + '.color2')
            cmds.connectAttr(currentNode + '.output', t + '.rotate')
    
        return nodes



    def cleanUpLeft(self, *args):
        #Cleaning up the Outliner and Scene
        ikCGroup = cmds.group(self.rig_info['ikLeg_L'][0], self.rig_info['ikLeg_L'][1], n = 'ikControls_LL_grp')
        jntsGrp = cmds.group(self.rig_info['ikJnts_L'][0], self.rig_info['fkJnts_L'][0], self.rig_info['rigJnts_L'][0], n = 'joints_LL_grp')
        ikHGroup = cmds.group(self.rig_info['ikLeg_L'][2], n = 'nodes_grp')
        cmds.group(ikCGroup, jntsGrp, ikHGroup, 'ctrl_LL_FK_femur_grp', 'ctrl_LL_IkFk_Switch_grp', n = 'L_leg_grp')
        cmds.select(d=True)
        cmds.setAttr(str(self.rig_info['ikJnts_L'][0]) +'.visibility', 0)
        cmds.setAttr(str(self.rig_info['fkJnts_L'][0]) + '.visibility', 0)

        #Control Visibility
        cmds.setDrivenKeyframe('ctrl_LL_FK_femur_grp.visibility', cd = 'ctrl_LL_IkFk_Switch.ikFk_Switch', dv = 0, v = 1 )
        cmds.setDrivenKeyframe('ctrl_LL_FK_femur_grp.visibility', cd = 'ctrl_LL_IkFk_Switch.ikFk_Switch',  dv = 1, v = 0 )
        cmds.setDrivenKeyframe(ikCGroup + '.visibility', cd = 'ctrl_LL_IkFk_Switch.ikFk_Switch',  dv = 1, v = 1 )
        cmds.setDrivenKeyframe(ikCGroup + '.visibility', cd = 'ctrl_LL_IkFk_Switch.ikFk_Switch',  dv = 0, v = 0 )

    def cleanUpRight(self, *args):
        #Cleaning up the Outliner and Scene
        ikCGroup = cmds.group(self.rig_info['ikLeg_R'][0], self.rig_info['ikLeg_R'][1], n = 'ikControls_RL_grp')
        jntsGrp = cmds.group(self.rig_info['ikJnts_R'][0], self.rig_info['fkJnts_R'][0], self.rig_info['rigJnts_R'][0], n = 'joints_RL_grp')
        ikHGroup = cmds.group(self.rig_info['ikLeg_R'][2], n = 'nodes_grp')
        cmds.group(ikCGroup, jntsGrp, ikHGroup, 'ctrl_RL_FK_femur_grp', 'ctrl_RL_IkFk_Switch_grp', n = 'R_leg_grp')
        cmds.select(d=True)
        cmds.setAttr(str(self.rig_info['ikJnts_R'][0]) +'.visibility', 0)
        cmds.setAttr(str(self.rig_info['fkJnts_R'][0]) + '.visibility', 0)

        #Control Visibility
        cmds.setDrivenKeyframe('ctrl_RL_FK_femur_grp.visibility', cd = 'ctrl_RL_IkFk_Switch.ikFk_Switch', dv = 0, v = 1 )
        cmds.setDrivenKeyframe('ctrl_RL_FK_femur_grp.visibility', cd = 'ctrl_RL_IkFk_Switch.ikFk_Switch',  dv = 1, v = 0 )
        cmds.setDrivenKeyframe(ikCGroup + '.visibility', cd = 'ctrl_RL_IkFk_Switch.ikFk_Switch',  dv = 1, v = 1 )
        cmds.setDrivenKeyframe(ikCGroup + '.visibility', cd = 'ctrl_RL_IkFk_Switch.ikFk_Switch',  dv = 0, v = 0 )
