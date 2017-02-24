# rig_arm.py
# @author: TOMG
# @reason: RiggingDojo
# @modified: 2/23/2017
# TODO : Mathify PoleVector Placements; set PV root position via config; Fix IK setup in general <see legs>
# TODO : Get the IKFK switch / BlendColor Node hooked up one of these days
# TODO : Find elegant solution for mirror axis
# TODO : Setup RvL control colours for each type, e.g. 'ctrl_colors': { 'fk_right': [0,1,0], 'fk_left': [1,0,0] }, etc.
# TODO : Final Cleanup Phase of parenting full groups; RIGHT_ARM -> SPINE <- LEFT_ARM, etc.

import maya.cmds as cmds
import system.utils as utils

print "We Have Imported RIG_ARM"


class RigArm(object):
    def __init__(self):
        print "Initializing RigArm:", self


    def rig_arm(self, jsonRigData):
        print "commencing rig... ", self
        for chain in jsonRigData['chains']:
            chainData = jsonRigData['chains'][chain]
            #completedChains = {}
            completedChains = []

            for pfx in jsonRigData['prefix']:
                # short circuit if we already established we don't want to build the current chain
                if chainData['use_ik'] is False and pfx.lower() == 'ik':
                    continue
                if chainData['use_fk'] is False and pfx.lower() == 'fk':
                    continue

                if chainData['use_mirror'] == True:
                    for mName in jsonRigData['mirrorName']:
                        completedChains.append(utils.ConstructJointChain(pfx, chain, chainData, mName))
                else:
                    completedChains.append(utils.ConstructJointChain(pfx, chain, chainData))

            utils.AttachToBaseRig(completedChains, chainData['use_mirror'])


    def DebugPrint(self):
        print "Hello: ", self


'''
# declare a data structure, fill it with useful information
_jointData = {
    'default': {
        'prefix': ['IK', 'FK', 'RIG'],
        'postfix': '',
        'mirrorName': ['Right', 'Left'],
        'mirrorAxis': 'x',
        'chains': {
            'arm': {
                'use_mirror': True,
                'use_ik': True,
                'use_fk': True,
                'ctrl_alignment': (1, 0, 0),
                'offset_value': 3.0,
                'joints': [
                    {'name': 'shoulder', 'position': [4.0, 13.0, 0.0]},
                    {'name': 'elbow', 'position': [7.0, 13.0, -1.5]},
                    {'name': 'wrist', 'position': [10.0, 13.0, 0.0]},
                    {'name': 'wristEnd', 'position': [10.5, 13.0, 0.0]}
                ]
            },
            'leg': {
                'use_mirror': True,
                'use_ik': True,
                'use_fk': True,
                'offset_value': -3.0,
                'ctrl_alignment': (0, 1, 0),
                'joints': [
                    {'name': 'hip', 'position': [1.5, 7.5, 0.0]},
                    {'name': 'upper', 'position': [2.5, 6.0, 0.0]},
                    {'name': 'lower', 'position': [2.5, 3.0, 1.5]},
                    {'name': 'foot', 'position': [2.5, 0.0, 0.0]}
                ]
            }
        }
    },
    'RiggingDojo': {
        'prefix': ['ik', 'fk', 'rig'],
        'postfix': 'jnt',
        'mirrorName': ['R', 'L'],
        'mirrorAxis': 'x',
        'chains': {
            'arm': {
                'use_mirror': True,
                'use_ik': True,
                'use_fk': True,
                'ctrl_alignment': (1, 0, 0),
                'offset_value': 3.0,
                'joints': [
                    {'name': 'shoulder', 'position': [4.0, 13.0, 0.0]},
                    {'name': 'elbow', 'position': [7.0, 13.0, -1.5]},
                    {'name': 'wrist', 'position': [10.0, 13.0, 0.0]},
                    {'name': 'wristEnd', 'position': [10.5, 13.0, 0.0]}
                ]
            },
            'leg': {
                'use_mirror': True,
                'use_ik': True,
                'use_fk': True,
                'offset_value': -3.0,
                'ctrl_alignment': (0, 1, 0),
                'joints': [
                    {'name': 'hip', 'position': [1.5, 7.5, 0.0]},
                    {'name': 'upper', 'position': [2.5, 6.0, 0.0]},
                    {'name': 'lower', 'position': [2.5, 3.0, 1.5]},
                    {'name': 'foot', 'position': [2.5, 0.0, 0.0]}
                ]
            },
            'spine': {
                'use_mirror': False,
                'use_ik': False,
                'use_fk': True,
                'offset_value': -3.0,
                'ctrl_alignment': (0, 1, 0),
                'joints': [
                    {'name': 'pelvis', 'position': [0.0, 7.5, 0.0]},
                    {'name': 'spine', 'position': [0.0, 8.5, 0.0]},
                    {'name': 'spine1', 'position': [0.0, 10.0, -1.0]},
                    {'name': 'spine2', 'position': [0.0, 13.5, 0.0]}
                    {'name': 'neck', 'position': [0.0, 14.0, 0.0]}
                ]
            }
        }
    }
}
jsonFilePath = os.path.join( os.environ['RIGGING_TOOL'], 'layout', 'layout.json' )
utils.writeJson(jsonFilePath, _jointData)
# _jsonRigData = utils.readJson(jsonFilePath)
'''
