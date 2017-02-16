import maya.cmds as cmds

print "Startup"

# Change time unit to NTSC
# cmds.currentUnit(time='ntsc')

# Change the current linear unit
# cmds.currentUnit(linear='cm')

import ui.ui as ui
reload(ui)
ui.RDojo_UI()