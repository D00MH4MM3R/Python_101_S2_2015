import system.utils as utils
import json
import os

fileName = os.environ['DATA_PATH'] + 'data.json'

arm_data = {}
arm_data['keyNames'] = ['bodyPlacement', 'jntType', 'jnts', 'ikCtrls', 'fkCtrls', 'ctrlGrps', 'jntPos']
arm_data['bodyPlacement'] = ['lt_', 'rt_']
arm_data['jntType'] = ['ik_', 'fk_', 'rig_']
arm_data['jnts']	= ['shoulder_jnt', 'elbow_jnt', 'wrist_jnt', 'wristEND_jnt']
arm_data['ikCtrls']	= ['ctrl_ikWrist', 'ikh_arm', 'ctrl_PV_arm', 'ctrl_ikHand']
arm_data['fkCtrls']	= ['ctrl_fkShoulder', 'ctrl_fkElbow', 'ctrl_fkWrist']
arm_data['ctrlGrps'] = ['grp_ctrl_ikWrist', 'grp_ctrl_fkShoulder', 'grp_ctrl_fkElbow', 'grp_ctrl_fkWrist', 'grp_arm']
arm_data['jntPos'] = [[-7, 0, 2], [-1, 0, 0], [4, 0, 2], [7, 0, 3]]

utils.writeJson(fileName, arm_data)
