

import os, sys
import numpy as np

wavelengths = np.arange(400,1020,20)

for wavelength in wavelengths:
    sys_command = "python runinst.py --doRun --doMonoWavelength -i monochrometer --wavelength %d"%wavelength
    os.system(sys_command)
    raw_input("Press enter when ready.")
    sys_command = "python runinst.py --doRun --doShutter -i shutter -s 1000"
    os.system(sys_command)
    raw_input("Press enter when ready.")
    sys_command = "python runinst.py --doRun --doShutter -i shutter -s -1"
    os.system(sys_command)
    raw_input("Press enter when ready.")

