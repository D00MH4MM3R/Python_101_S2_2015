import os
import sys
import pymel.core as pm

print 'In User Setup'

sys.path.append(os.environ['RIGGING_TOOL'])
pm.evalDeferred('import startup')

