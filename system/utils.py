import pymel.core as pm 
import json
import tempfile

# json functions
def writeJson(fileName, data):
	with open(fileName, 'w') as outfile:
		json.dump(data, outfile)
	file.close(outfile)

def readJson(fileName):
	with open(fileName, 'r') as infile:
		data = (open(infile.name, 'r').read())
	return data


# create joints for different sides of the body
def createSide(self, bodySide, ikfkList, jntList, posList):
	# used to create the left arm
	for item in ikfkList:
		for j in range(len(jntList)):
			jntName = bodySide+item+jntList[j]
			pm.joint(name=jntName, position=posList[j], radius=.5)

		pm.select(deselect=True)	

def mirrorSide(self, bodySide, ikfkList, jntList, posList):
	# used to create the right arm
	for item in ikfkList:
		for j in range(len(jntList)):
			jntName = bodySide+item+jntList[j]
			if posList[j][0] > 0:
				posList[j][0] = posList[j][0] * -1
			pm.joint(name=jntName, position=posList[j], radius=.5, orientation=(180,0,0))

		pm.select(deselect=True)	



# functions to search the data prep dictionary
def searchControls(self, strName, ikfk, keyNames, ctrls):
	print ctrls	

	# get the index of the list item that has the string name as a substring
	indx = [idx for idx, s in enumerate(ctrls) if strName in s][0]
	return ctrls[indx]

def searchGroups(self, strName, grps):
	# get the index of the list item that has the string name as a substring
	indx = [idx for idx, s in enumerate(grps) if strName in s][0]
	return grps[indx]