
sn = "37873245"
from odemis.driver.tlaptmf import MFF 
mff = MFF("MFF101","flipper",sn=sn)
print mff 
print mff.GetInfo()
pos = 2
mff.MoveJog(pos)

