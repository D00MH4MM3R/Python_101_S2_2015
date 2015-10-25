import maya.cmds as cmds

print "Startup"

#change the current time unit to ntsc
cmds.currentUnit(time = 'ntsc')

#change the current linear unit to inches
cmds.currentUnit(linear = 'cm')

import ui.ui as ui