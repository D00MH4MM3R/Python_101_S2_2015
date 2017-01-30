import os
import sys
import maya.cmds as cmds

rd_path = 'D:/RiggingDojo/RD_Python_101/Python_101_S2_2015'

if not rd_path in sys.path:
    sys.path.append(rd_path)

cmds.evalDeferred('import startup')
