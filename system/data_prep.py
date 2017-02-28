import system.utils as utils
import json
import os

def loadData():
	print 'loading data...'

	# create dictionary file with general rig information
	fileName = os.environ['DATA_PATH'] + 'menuData.json'

	menu_data = {}
	menu_data['bodyPart'] = [' ', 'arm', 'leg']
	menu_data['bodySide'] = [' ', 'both', 'left', 'right']
	menu_data['rigType'] = [' ', 'all', 'ik', 'fk', 'rig']
	
	utils.writeJson(fileName, menu_data)


	# create dictionary file with arm information
	fileName = os.environ['DATA_PATH'] + 'armData.json'

	arm_data = {}
	arm_data['keyNames'] = ['jnts', 'ikCtrls', 'fkCtrls', 'ctrlGrps', 'jntPos']
	arm_data['jnts']	= ['shoulder_jnt', 'elbow_jnt', 'wrist_jnt', 'wristEND_jnt']
	arm_data['ikCtrls']	= ['ctrl_ikWrist', 'ikh_arm', 'ctrl_PV_arm', 'ctrl_ikHand']
	arm_data['fkCtrls']	= ['ctrl_fkShoulder', 'ctrl_fkElbow', 'ctrl_fkWrist']
	arm_data['ctrlGrps'] = ['grp_ctrl_ikWrist', 'grp_ctrl_fkShoulder', 'grp_ctrl_fkElbow', 'grp_ctrl_fkWrist', 'grp_arm']
	arm_data['jntPos'] = [[13, 131.3, 0], [35.25, 128.5, 0], [56.3, 128.5, 0], [74, 129, 0]]
	#arm_data['jntPos'] = [[.5, 0, 0], [6, 0, 0], [12, 0, 2], [15, 0, 4]]

	utils.writeJson(fileName, arm_data)


	# create dictionary file of leg information
	fileName = os.environ['DATA_PATH'] + 'legData.json'

	leg_data = {}
	leg_data['keyNames'] = ['jnts', 'ikCtrls', 'fkCtrls', 'ctrlGrps', 'jntPos']
	leg_data['jnts']	= ['hip_jnt', 'knee_jnt', 'ankle_jnt', 'toetEND_jnt']
	leg_data['ikCtrls']	= ['ctrl_ikAnkle', 'ikh_leg', 'ctrl_PV_leg', 'ctrl_ikFoot']
	leg_data['fkCtrls']	= ['ctrl_fkAnkle', 'ctrl_fkKnee', 'ctrl_fkAnkle']
	leg_data['ctrlGrps'] = ['grp_ctrl_ikAnkle', 'grp_ctrl_fkHip', 'grp_ctrl_fkKnee', 'grp_ctrl_fkAnkle', 'grp_leg']
	leg_data['jntPos'] = [[8, 85, 3.2], [8, 48.5, 1.5], [8, 9.5, -.17], [8, 1, 22.5]]

	utils.writeJson(fileName, leg_data)
