import pymel.core as pm 
import platform
import os

print 'Startup'

# Change the current time unit to ntsc
pm.currentUnit(time='ntsc')

# Change the current linear unit to centimeters
pm.currentUnit(linear='cm')

# Checking OS
plat = platform.system()
if plat == 'Windows':
	fileName = os.environ['DATA_PATH'] = os.environ['RIGGING_TOOL'] + '/data/rig'
elif plat == 'Darwin':
	fileName = os.environ['DATA_PATH']

if not os.path.exists(fileName):
	os.makedirs(fileName)
else:
	print 'Data path is ', fileName


import ui.ui as ui
reload(ui)

ui.RDojo_UI()
