"""In genetics.py"""

def assignGenetics(world):
	
	nDeaf = int(math.ceil(world.nAgents *world.parameters["gDom"]))
	
	n_oneCopy = int((world.nAgents-nDeaf) * world.parameters["gCarry"])
	n_twoCopies = nDeaf
	n_zeroCopies = len(world.pop) - n_oneCopy - n_twoCopies
	
	# 0 = hearing, 1 = deaf

	nZeroOne = binom.rvs(n=n_oneCopy,p=.5)
	nOneZero = n_oneCopy - nZeroOne
	gene_distribution = ([(0,1)]*nZeroOne) + ([(1,0)]*nOneZero) + ([(1,1)] * n_twoCopies) + ([(0,0)] * n_zeroCopies)
	
	random.shuffle(gene_distribution)
	
	for i in range(len(gene_distribution)):
		agent = world.pop[i]
		agent.genes = gene_distribution[i]
		if gene_distribution[i] == (1,1):
			agent.deafStatus = True
		else:
			agent.deafStatus = False
			

def births_and_deaths(world):
	""" Population change by replacement
	"""
	nHits = binom.rvs(n=world.parameters["maxNumberOfBirthDeathEachStage"],p=world.parameters["probOfBirthDeathEachStage"])

	for i in range(nHits):
		couples =findMarriedCouples(world)
		if len(couples)>0:

			couples =findMarriedCouples(world)
			new_parents = random.choice(couples)
			#print new_parents
			#print len(world.pop)
			# have a child
			reproduce(world.pop[new_parents[0]], world.pop[new_parents[1]], world)
			# remove someone
			agent_to_remove = random.choice(world.pop)
			world.removeAgent(agent_to_remove)




"""In marriage.py"""

def findCandidatePartners(target_agent_id, agent_ids,world):
	# can't marry self
	#agent_ids.remove(target_agent_id)
	agent_ids.remove(target_agent_id)
	possibleFreeAgents = np.array(agent_ids)

	stagCompound = world.compounds[target_agent_id]
	stagSex = world.pop[target_agent_id].sex
	possibleCandidates = []
	for i in agent_ids:
		if world.pop[i].sex != stagSex: #Cant marry same gender
			if world.compounds[i] != stagCompound: #cant marry within compound
				possibleCandidates.append(i)
	return(possibleCandidates)
	
def getCandidateWeights(target_agent_id, agent_ids, world):

	# weight marriage by modality attitudes
	attitudes = world.parameters["marriageAttitudes"][world.pop[target_agent_id].deafStatus]
	cand_weights = [attitudes[world.pop[i].deafStatus] for i in agent_ids]
	
	# weight candidates by social links
	socialLinks = world.popStructure[target_agent_id,agent_ids] + 1
	
	#total_weights = [cand_weights[i] * socialLinks[i] for i in range(len(cand_weights))]
	total_weights = np.array(cand_weights) * np.array(socialLinks)
	return(total_weights)



"""In populationStructure.py"""
def findAgentIndexById(self,agent):
    for i in range(len(self.pop)):
        if self.pop[i].ID == agent.ID:
            return i


"""Parameter Range sweeping tools"""

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
#x = simulation(500,"text.csv")
