'''
Rhonda Ray

Description:
   Creating IK/FK arm rig

'''

import pymel.core as pm
import system.ctrl_shapes as cShape
import system.utils as utils
import json
import os

print 'Starting IK-FK Arm Rig...'


class RigArm():

	def __init__(self):
		fileName = os.environ['DATA_PATH'] + 'data.json'
		self.rigInfo = json.loads(utils.readJson(fileName))
	 
		self.keyNames = self.rigInfo.get('keyNames')
		# index 0 = bodyPlacement, index 1 = jntType, index 2 = jnts, index 3 = ikCtrls
		# index 4 = fkCtrls, index 5 = ctrlGrps, index 6 = jntPos

		self.bodySide = self.rigInfo.get('bodyPlacement')


	def createRig(self):
		print 'starting create rig...'
		self.createJoint('both')
		self.createIK('both')
		self.createFK('both')
		self.connectJoints('both')
		self.createPoleVector('both')
		self.createIKSwitch('both')


	# when UI is created, the sides parameter with be passed in - left, right or both
	def createJoint(self, sides):
		# get list of joints, type of joints and the joint position from rig info
		ikfkList = self.rigInfo.get(self.keyNames[1])
		jntList = self.rigInfo.get(self.keyNames[2])
		posList = self.rigInfo.get(self.keyNames[6])

		# createSide is used for the left arm and mirrorSide is used for the right arm
		if sides == 'both':
			self.createSide(ikfkList, jntList, posList)
			self.mirrorSide(ikfkList, jntList, posList)
		elif sides == 'left':
			self.createSide(ikfkList, jntList, posList)
		else:
			self.mirrorSide(ikfkList, jntList, posList)


	def createSide(self, ikfkList, jntList, posList):
		# used to create the left arm
		for item in ikfkList:
			for j in range(len(jntList)):
				jntName = self.bodySide[0]+item+jntList[j]
				pm.joint(name=jntName, position=posList[j], radius=.5)

			pm.select(deselect=True)	


	def mirrorSide(self, ikfkList, jntList, posList):
		# used to create the right arm
		for item in ikfkList:
			for j in range(len(jntList)):
				jntName = self.bodySide[1]+item+jntList[j]
				if posList[j][0] > 0:
					posList[j][0] = posList[j][0] * -1
				pm.joint(name=jntName, position=posList[j], radius=.5, orientation=(180,0,0))

			pm.select(deselect=True)	


	def createIK(self, sides):
		if sides == 'both':
			for s in range(len(self.bodySide)):
				self.ikSetup(self.bodySide[s])
		else:
			self.ikSetup(sides)
		

	def ikSetup(self, side):
		# create IK handle
		ikName = self.searchControls('ikh', 'ik')
		ikName = side+ikName
		pm.ikHandle(name=ikName, startJoint=side+'ik_shoulder_jnt', endEffector=side+'ik_wrist_jnt', solver='ikRPsolver', priority=2, weight=1)

		# get world space position of wrist joint
		posWrist = pm.xform(side+'ik_wrist_jnt', query=True, translation=True, worldSpace=True)

		# create an empty group and orient to wrist
		grpName = side+self.searchGroups('ikWrist')
		pm.group(empty=True, name=grpName)
		
		# create square control
		ctrlName = side+self.searchControls('Wrist', 'ik')
		ctrl = cShape.square(self, ctrlName)

		# parent control to group
		pm.parent(ctrl, grpName)

		# move the group to the joint
		pm.xform(grpName, translation=posWrist, worldSpace=True)

		# parent ik handle to wrist control
		pm.parent(ikName, ctrl)

		
	def searchControls(self, strName, ikfk):
		# find the control in the ik controls list
		# get list of ik controls from rig info
		if ikfk == 'ik':
			ctrls = self.rigInfo.get(self.keyNames[3])
		else:
			ctrls = self.rigInfo.get(self.keyNames[4])
	
		# get the index of the list item that has the string name as a substring
		indx = [idx for idx, s in enumerate(ctrls) if strName in s][0]
		return ctrls[indx]


	def searchGroups(self, strName):
		# find the control group in the group list
		# get list of groups from rig info
		grps = self.rigInfo.get(self.keyNames[5])
	
		indx = [idx for idx, s in enumerate(grps) if strName in s][0]
		return grps[indx]


	def createFK(self, sides):
		if sides == 'both':
			for s in range(len(self.bodySide)):
				self.fkSetup(self.bodySide[s])
		else:
			self.fkSetup(sides)

		
	def fkSetup(self, side):	
		# get list of selected objects minus the end joint
		pm.select(side+'fk_shoulder_jnt')
		selJoints = pm.ls(selection=True, dag=True)
		selJoints.pop(-1)

		# loop thru the selected joints
		for jnt in selJoints:
			# get world space position of the joint
			posWrist = pm.xform(jnt, query=True, translation=True, worldSpace=True)

			# pull out the joint name, upper case the first letter and concatenate to fk
			jntName = 'fk' + jnt.split('_')[2].title()

			# create group from joint name
			grpName = side+self.searchGroups(jntName)
			grp = pm.group(name=grpName, empty=True)

			ctrlName = self.searchControls(jntName, 'fk')
			ctrl = cShape.circle(self, ctrlName)
			
			# parent control to grp
			pm.parent(ctrl, grp)

			# move group to joint
			pm.xform(grp, translation=posWrist, worldSpace=True)

			# constrain joint to control
			pm.parentConstraint(ctrl, jnt, maintainOffset=True)


	def connectJoints(self, sides):
		# connect IK and FK to rig joints
		if sides == 'both':
			for s in range(len(self.bodySide)):
				self.connectSetup(self.bodySide[s])
		else:
			self.connectSetup(sides)


	def connectSetup(self, side):
		# select all three joint chains and group together
		pm.select(side+'rig_shoulder_jnt', replace=True)
		pm.select(side+'fk_shoulder_jnt', add=True)
		pm.select(side+'ik_shoulder_jnt', add=True)

		grpName = side+self.searchGroups('arm')
		pm.group(name=grpName)

		# select same joint from each arm and add orient constraint
		pm.orientConstraint(side+'fk_shoulder_jnt', side+'ik_shoulder_jnt', side+'rig_shoulder_jnt')
		pm.orientConstraint(side+'fk_elbow_jnt', side+'ik_elbow_jnt', side+'rig_elbow_jnt')
		pm.orientConstraint(side+'fk_wrist_jnt', side+'ik_wrist_jnt', side+'rig_wrist_jnt')

		# create control hierarchy
		pm.parent(side+'grp_ctrl_fkWrist', side+'ctrl_fkElbow')
		pm.parent(side+'grp_ctrl_fkElbow', side+'ctrl_fkShoulder')

		pm.select(deselect=True)


	def createPoleVector(self, sides):
		if sides == 'both':
			for s in range(len(self.bodySide)):
				self.poleVectorSetup(self.bodySide[s])
		else:
			self.poleVectorSetup(sides)


	def poleVectorSetup(self, side):
		# used Lionel Gallat's idea for the pole vector - just converted to python
		# create locator for placement of the pole vector
		pm.spaceLocator(name='lctr_PV_arm')
		posElbow = pm.xform(side+'ik_elbow_jnt', query=True, translation=True, worldSpace=True)
		pm.xform('lctr_PV_arm', worldSpace=True, translation=posElbow)
		pm.setAttr('lctr_PV_arm.tz', posElbow[2] - 5)

		# create pole vector control
		ctrlName = side+self.searchControls('PV', 'ik')
		ctrl = cShape.pointer(self, ctrlName)

		# move control to locator position
		temp = pm.pointConstraint('lctr_PV_arm', ctrl)
		pm.delete(temp)
		pm.makeIdentity(ctrl, apply=True, translate=1, rotate=1, scale=1, normal=0, preserveNormals=1) 
		pm.delete('lctr_PV_arm')
		pm.select(deselect=True)

		# constrain the IK handle to the pole vector control
		pm.poleVectorConstraint(ctrl, side+'ikh_arm')


	def createIKSwitch(self, sides):
		if sides == 'both':
			for s in range(len(self.bodySide)):
				self.switchSetup(self.bodySide[s])
		else:
			self.switchSetup(sides)


	def switchSetup(self, side):
		# creates text for IK/FK switch 
		ctrlName = side+self.searchControls('Hand', 'ik')
		ctrl = cShape.text(self, ctrlName, 'switch')

		# rename control
		newName = ctrl[0].strip('Shape')
		txtCurve = pm.rename(ctrl[0], newName, ignoreShape = True)
		pm.xform(txtCurve, centerPivots = True)

		# create locator for the IK switch
		pm.spaceLocator(name='lctr_switch')
		posEnd = pm.xform(side+'rig_wristEND_jnt', query=True, translation=True, worldSpace=True)
		pm.xform('lctr_switch', worldSpace=True, translation=posEnd)

		if side == 'rt_':
			pm.setAttr('lctr_switch.tx', posEnd[0] - 1.25)
		else:
			pm.setAttr('lctr_switch.tx', posEnd[0] + 1.25)

		# move control to locator position
		temp = pm.pointConstraint('lctr_switch', txtCurve)
		pm.delete(temp)

		if side == 'rt_':
			pm.xform(txtCurve, worldSpace=True, rotation=(0,90,0), scale=(.5,.5,.5))
		else:
			pm.xform(txtCurve, worldSpace=True, rotation=(0,-90,0), scale=(.5,.5,.5))

		pm.makeIdentity(txtCurve, apply=True, translate=1, rotate=1, scale=1, normal=0, preserveNormals=1) 
		pm.delete('lctr_switch')

		pm.select(deselect=True)




print 'end of script'
