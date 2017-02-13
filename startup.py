import pymel.core as pm 
import platform

print 'Startup'

# Change the current time unit to ntsc
pm.currentUnit(time='ntsc')

# Change the current linear unit to centimeters
pm.currentUnit(linear='cm')

# Checking OS
plat = platform.system()
if plat == 'Windows':
	os.environ['DATA_PATH'] = 'C:/Users/rhondaray/Documents/GitHub/Python_101_S2_2015/layout/'

import ui.ui as ui
