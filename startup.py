import maya.cmds as cmds

print 'Startup'

cmds.currentUnit( linear = 'cm')
print 'Setting units to Centimeters'

cmds.currentUnit( time = 'ntsc')
print 'Setting time to NTSC 30 fps'

import ui.ui as ui
