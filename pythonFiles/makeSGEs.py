import os, csv,stat
from parameters import *

sge= """#!/bin/sh
#$ -N SeanRXRFCI4001
#$ -cwd
#$ -q all.q
#$ -S /bin/bash
#$ -p -10
dir=$HOME/SignSpeechModel/Model/pythonFiles
binary=/usr/local/lib64/R/bin/Rscript
cd $dir
$binary modelAnalysis.py NUMX
"""

gfolder = "../gridEngineFiles/"
prevFiles = os.listdir(gfolder)
for f in prevFiles:
	os.remove(gfolder+f)


param = readParameters()


simNums = param.keys()
print simNums

for i in simNums:
	out = sge.replace("NUMX",str(i))
	fname = "../gridEngineFiles/runModel_"+str(i)+".sge"
	shname = "../gridEngineFiles/runModel_"+str(i)+".sh"
	o = open(fname,'w')
	o.write(out)
	o.close()
	
	sh = "#!/bin/sh\n"
	for s in range(param[i]["nSimulations"]):
		sh += "qsub "+fname + "\n"
	o = open(shname,'w')
	o.write(sh)
	o.close()
	#os.chmod(shname,stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

bigSH = """#!/bin/sh
cd ../gridEngineFiles
""" + "\n".join([x for x in os.listdir(gfolder) if x.endswith(".sh")])

bigShfile = "../gridEngineFiles/runModels.sh"
o = open(bigShfile,'w')
o.write(bigSH)
o.close()
#os.chmod(bigShfile, stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)