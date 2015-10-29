import maya.cmds as cmds

print "Startup"

#change the current time unit to film
cmds.currentUnit(time = 'film')

#change the current linear unit to inches
cmds.currentUnit(linear = 'cm')

import rdui.ui as ui
reload(ui)
