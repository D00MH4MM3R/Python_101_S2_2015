import pymel.core as pm 

print 'Startup'

# Change the current time unit to ntsc
pm.currentUnit(time='ntsc')

# Change the current linear unit to centimeters
pm.currentUnit(linear='cm')

import ui.ui as ui
