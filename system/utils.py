import maya.cmds as cmds
import json

def writeJson(fileName, data, prtyIndent=None):
    with open(fileName, 'w') as outFile:
        json.dump(data, outFile, indent=prtyIndent, separators=(',', ': '), sort_keys=True)
    outFile.close()

def readJson(fileName):
    with open(fileName, 'r') as inFile:
        data = (open(inFile.name, 'r').read())
    return json.loads(data)
