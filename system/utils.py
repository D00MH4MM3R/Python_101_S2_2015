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


def SaveCustomShape(shapeName=None, debug=False):
    if shapeName == None:
        shapeName = cmds.ls(sl=True)[0]
    cvCount = cmds.getAttr(shapeName + '.cp', s=1)
    cvPos = []
    for i in range(0, cvCount):
        cp = cmds.select(shapeName + '.cv[' + str(i) + ']')
        p = cmds.xform(cp, q=True, t=True, ws=True)
        cvPos.append(p)

    # TODO : write to CustomShapes.json:
    # { "shapeName": [cvPos, cvPos, cvPos] }
    if debug:
        return cvPos


def CreateCustomShape(shapeName=None, cvPositions=[]):
    # load Resources/CustomShapes.json
    # check for shapeName in keys
    # if found:
    # shapesJson = {}
    if shapeName:  # and shapesJson:
        # Create Curve
        cmds.curve(n=shapeName, p=cvPositions)

        # Get Some Renaming Done
        cmds.select(shapeName, r=True)
        all = cmds.ls(sl=True, dag=True, shapes=True)
        for shape in all:
            cmds.rename(shape, "{0}Shape".format(cmds.listRelatives(shape, parent=True)[0]))
    else:
        print "FAILED TO CREATE CUSTOM SHAPE"
# del temp
# temp = None
# temp = SaveCustomShape()
# CreateCustomShape(shapeName="ctrl_control_name", cvPositions=temp)

def SetCustomColor(objectName=None, rgb=None, *args):
    for a in args:
        print a
    if objectName:
        if rgb:
            r, g, b = rgb[0], rgb[1], rgb[2]
            try:
                # override default display draw
                cmds.setAttr(objectName + ".overrideEnabled", True)
                cmds.setAttr(objectName + ".overrideRGBColors", True)
                # set RGB color
                cmds.setAttr(objectName + ".overrideColorRGB", r, g, b)
            except:
                print "Something has gone terribly wrong while attempting to override {0} colors with {1}".format(objectName, rgb)
        else:
            print "Missing an RGB list - continue with defaults"
    else:
        print "Missing a control name to set color - moving on"