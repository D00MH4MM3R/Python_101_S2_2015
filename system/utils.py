import maya.cmds as cmds
import json
import tempfile


def writeJson(fileName, data):
	with open (fileName, 'w') as outfile:
		json.dump(data, outfile)
	file.close(outfile)

def readJson(fileName):
	with open (fileName, 'r') as infile:
		data = (open(infile.name, 'r').read())
	return data

def colOverride(ext, controls):

	if ext == 'LA' or side == 'LL':
		color = 6
	elif ext == 'RA' or side == 'RL':
		color = 13
	elif ext == 'LA' or side == 'LL':
		color = 17

	for c in controls:
		targetShape = cmds.listRelatives( c , s = True, pa = True)
		cmds.setAttr( str(targetShape[0]) + ".overrideEnabled", 1)
		cmds.setAttr( str(targetShape[0]) + ".overrideColor", color)
		shapeAmount = len(targetShape)
		if shapeAmount > 1:
			for t in targetShape[1:]:
				cmds.setAttr( str(t) + ".overrideEnabled", 1)
				cmds.setAttr( str(t) + ".overrideColor", color)