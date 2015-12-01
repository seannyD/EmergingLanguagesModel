from marriage import *
from parameters import *
from interactions import *
from genetics import *
import os, csv, sys, random, pickle
# (removed pandas because it's not installed on the server)


#python modelAnalysis.py 1
# Will run 1 simulation with parameters taken from the first line of the csv file.


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

def writeResultsString(res,file):
	o = open(file,'w')
	o.write(res)
	o.close()

def simulation(parameters):

	resultsString = "stage,id,deaf,signs,sounds,structure\n"
	
	world1 = world(parameters)
	if world1.parameters["RunName"]=="Test":
		print "TEST"
		for x in world1.parameters.keys():
			print x,world1.parameters[x]
		print [a.genes for a in world1.pop]
	im = InteractionsMaker(world1,filename=parameters["ResultsFileName"])
	marriages(im.world)
	nStages = parameters["nStages"]
	
	for stage in xrange(nStages):
		resultsString += im.simulateOneStage(stage)
		if (stage % 3) ==0:
			marriages(im.world)
			im.world.rebalance_structures()
	writeResultsString(resultsString,im.filename)
	return world1



runSimulations()