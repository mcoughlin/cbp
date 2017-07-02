

import os, sys
import numpy as np

focuses = np.arange(9000,18000,1000)
focuses[-1] = 16383

focuses = np.arange(13000,17000,500)
focuses[-1] = 16383

focuses = np.arange(14500,16500,200)

focuses = np.arange(15100,15325,25)

#focuses = np.arange(15175,15325,25)
#focuses = np.arange(15180,15230,10)


print focuses
print len(focuses)

for focus in focuses:
    sys_command = "python runinst.py --doRun -i birger --doFocus -f %d"%focus
    os.system(sys_command)
    raw_input("Press enter when ready.")

