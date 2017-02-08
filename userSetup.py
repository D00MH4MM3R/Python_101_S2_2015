import os
import sys
import maya.cmds as cmds

rd_path = os.environ['RIGGING_TOOL']

if not rd_path in sys.path:
    sys.path.append(rd_path)

cmds.evalDeferred('import startup')
