import maya.cmds as cmds
import json
# import tempFile #???

def writeJson(fileName, data):
    with open(fileName, 'w') as outFile:
        json.dump(data,outFile)
    outFile.close()

def readJson(fileName):
    with open(fileName, 'r') as inFile:
        data = (open(inFile.name, 'r').read())
    return json.loads(data)
