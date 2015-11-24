from exemplarAgent import *
from marriage import *
import math
import random
from scipy.stats import binom

# def assignGenetics(world):
# 	
# 	nDeaf = int(math.ceil(world.nAgents *world.parameters["gDom"]))
# 	
# 	n_oneCopy = int((world.nAgents-nDeaf) * world.parameters["gCarry"])
# 	n_twoCopies = nDeaf
# 	n_zeroCopies = len(world.pop) - n_oneCopy - n_twoCopies
# 	
# 	# 0 = hearing, 1 = deaf
# 	gene_distribution = [random.choice([(0,1),(1,0)]) for i in range(n_oneCopy)] + ([(1,1)] * n_twoCopies) + ([(0,0)] * n_zeroCopies)
# 	
# 	random.shuffle(gene_distribution)
# 	
# 	for i in range(len(gene_distribution)):
# 		agent = world.pop[i]
# 		agent.genes = gene_distribution[i]
# 		if gene_distribution[i] == (1,1):
# 			agent.deafStatus = True
# 		else:
# 			agent.deafStatus = False

def assignGenetics(world):
	
	nDeaf = int(math.ceil(world.nAgents *world.parameters["gDom"]))
	
	n_oneCopy = int((world.nAgents-nDeaf) * world.parameters["gCarry"])
	n_twoCopies = nDeaf
	n_zeroCopies = len(world.pop) - n_oneCopy - n_twoCopies
	
	# 0 = hearing, 1 = deaf

	#nZeroOne = binom.rvs(n=n_oneCopy,p=.5)
	# server mod
	nZeroOne = binom.rvs(n_oneCopy,.5)
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


def assignSex(world):
	for agent in world.pop:
		agent.sex = random.choice([0,1])
			
def recombination(agentA,agentB):
	"""Return a random genetic recombination of two parents
	"""
	
	fgene = random.choice(agentA.genes)
	mgene = random.choice(agentB.genes)
	bgene = [fgene,mgene]
	random.shuffle(bgene)

	return((bgene[0],bgene[1]))
	
def reproduce(agentA,agentB, world):
	
	father,mother = agentA,agentB
	if agentA.sex > 0.5:
		father,mother = agentB, agentA
	
	baby_genetics = recombination(father,mother)
	
	baby = agentEpsilon(father.alpha, nManualSigns = father.nm, nSpokenSigns = father.ns, deaf=baby_genetics == (1,1), sex=random.choice([0,1]), genes=baby_genetics)

	# patrilineal culture
	world.addAgent( baby, father, [mother])
#	father.children += 1
#	mother.children += 1
	
def births_and_deaths(world):
	""" Population change by replacement
	"""
	# server mod
	#nHits = binom.rvs(n=world.parameters["maxNumberOfBirthDeathEachStage"],p=world.parameters["probOfBirthDeathEachStage"])
	nHits = binom.rvs(world.parameters["maxNumberOfBirthDeathEachStage"],world.parameters["probOfBirthDeathEachStage"])

	for i in range(nHits):
			# find a couple to have a child
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
				
