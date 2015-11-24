def simulation(nStages,filename):
	world1 = world(kolok_parameters)
	im = InteractionsMaker(world1,filename=filename)
	marriages(im.world)

	for stage in xrange(nStages):
		im.simulateOneStage(stage)
		if (stage % 3) ==0:
			marriages(im.world)
			im.world.rebalance_structures()
	return world1
	

def simulationNoWeight(nStages, whichWeight, filename="Results.txt"):
	"e.g. whichWeight = 'clan'/'compound'/'deafCommunity' "
	theseParams = kolok_parameters
	filenameWeight = whichWeight+filename
	theseParams[whichWeight+"Weight"] = 1
	simulation(nStages,parameters = theseParams,filename = filenameWeight)

def simulationParameter(nStages, parameterPair, filename="Results.txt"):
	theseParams = kolok_parameters
	theseParams[parameter[0]] = parameterValue
	filenameParameter = parameter+filename
	simulation(nStages,parameters = theseParams,filename = filenameParameter)
	
x = simulation(1500,"results/text.tab")