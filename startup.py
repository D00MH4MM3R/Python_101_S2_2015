import sys

import maya.cmds as cmds

print 'Startup functional'

#change time to ntsc because 30fps for games
cmds.currentUnit(time='ntsc')

#and units to cm on the off chance they weren't
cmds.currentUnit(linear='cm')

#import ui.py for tool menu
import ui.kcUI as ui
