import os
import sys

import maya.cmds as cmds
print 'In user setup'

sys.path.append('/Users/Miko/Desktop/DojoClass/Python_101_S2_2015')
cmds.evalDeferred('import startup')