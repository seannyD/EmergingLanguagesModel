from marriage import *
from parameters import *
from interactions import *

# test update

import os, csv, sys, random, pickle
# (removed pandas because it's not installed on the server)


def runSimulations():
	command = sys.argv[-1]
	paramNum = int(command)
	print paramNum
	parameters = getParameters(paramNum)
	setUpFolders(parameters)
	simulation(parameters)

def setUpFolders(parameters, deletePrevResults = False):
	folderName = parameters["FolderName"]
	if len(folderName)>0:
		if not os.path.exists(folderName):
			os.makedirs(folderName)
		pFileName = parameters["ParamFileName"]
		pickle.dump( parameters, open(pFileName , "wb" ) )
		
		if deletePrevResults:
			prevFiles = [ folderName + f for f in os.listdir(folderName) if f.endswith(".res") ]
			for f in prevFiles:
				os.remove(f)
	

def simulation(parameters):
	world1 = world(parameters)
	im = InteractionsMaker(world1,filename=parameters["ResultsFileName"])
	marriages(im.world)
	nStages = parameters["nStages"]
	
	for stage in xrange(nStages):
		im.simulateOneStage(stage)
		if (stage % 3) ==0:
			marriages(im.world)
			im.world.rebalance_structures()
	return world1



runSimulations()