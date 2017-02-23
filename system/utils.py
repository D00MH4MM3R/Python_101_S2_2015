import maya.cmds as cmds
import json
import tempfile

def writeJson(filename, data):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
    file.close(outfile)

def readJson(filename):
    with open(filename, 'r') as infile:
        data = (open(infile.name, 'r').read())
    return data