import os, csv,stat
from parameters import *

sge= """python modelAnalysis.py NUMX
"""

param = readParameters()
simNums = param.keys()
print simNums

out= "cd ~/Documents/MPI/EmergingLanguages/SignSpeechConnieBill/Model/pythonFiles\n"
for r in range(param[1]["nSimulations"]):
	for i in simNums:
		out += sge.replace("NUMX",str(i)) 
print out

o = open("../localRuns/runModelsLocally.sh",'w')
o.write(out)
o.close()
