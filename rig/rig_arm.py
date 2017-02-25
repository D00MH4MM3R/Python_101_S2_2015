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


class RigArm():
	print 'Starting IK-FK Arm Rig...'

	def __init__(self):
		print 'processing init'

		fileName = os.environ['DATA_PATH'] + 'arm.json'
		self.rigInfo = json.loads(utils.readJson(fileName))
		self.keyNames = self.rigInfo.get('keyNames')
		# index 0 = jnts, index 1 = ikCtrls, index 2 = fkCtrls, index 3 = ctrlGrps, index 4 = jntPos


	def createRig(self):
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

		# createSide is used for the left side and mirrorSide is used for the right side
		if sides == 'both':
			utils.createSide(self, ikfkList, jntList, posList)
			utils.mirrorSide(self, ikfkList, jntList, posList)
		elif sides == 'left':
			utils.createSide(self, ikfkList, jntList, posList)
		else:
			utils.mirrorSide(self, ikfkList, jntList, posList)


	def createIK(self, sides):
		if sides == 'both':
			for s in range(len(self.bodySide)):
				self.ikSetup(self.bodySide[s])
		else:
			self.ikSetup(sides)
		

	def ikSetup(self, side):
		# create IK handle
		ikName = utils.searchControls(self, 'ikh', 'ik')
		ikName = side+ikName
		pm.ikHandle(name=ikName, startJoint=side+'ik_shoulder_jnt', endEffector=side+'ik_wrist_jnt', solver='ikRPsolver', priority=2, weight=1)

		# get world space position of wrist joint
		posWrist = pm.xform(side+'ik_wrist_jnt', query=True, translation=True, worldSpace=True)

		# create an empty group and orient to wrist
		grpName = side+utils.searchGroups(self, 'ikWrist')
		pm.group(empty=True, name=grpName)
		
		# create square control
		ctrlName = side+utils.searchControls(self, 'Wrist', 'ik')
		ctrl = cShape.square(self, ctrlName)

		# parent control to group
		pm.parent(ctrl, grpName)

		# move the group to the joint
		pm.xform(grpName, translation=posWrist, worldSpace=True)

		# parent ik handle to wrist control
		pm.parent(ikName, ctrl)


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
			grpName = side+utils.searchGroups(self, jntName)
			grp = pm.group(name=grpName, empty=True)

			ctrlName = utils.searchControls(self, jntName, 'fk')
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

		grpName = side+utils.searchGroups(self, 'arm')
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
		ctrlName = side+utils.searchControls(self, 'PV', 'ik')
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
		ctrlName = side+utils.searchControls(self, 'Hand', 'ik')
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
