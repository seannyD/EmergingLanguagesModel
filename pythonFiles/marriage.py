import numpy as np
import math
import random
import copy
from populationStructure import *
from genetics import *

def roulette_wheel(scores):
    "Given a list of scores, returns a position in that list randomly in proportion to its score (stolen code!)"
#     total = 0
#     for s in scores:
#         total += s
#     r = random.uniform(0,total)
#     total = 0
#     for i in range(len(scores)):
#         total += scores[i]
#         if r < total:
#             return i
# convert to probabilities
    sx = [i/float(sum(scores)) for i in scores]
    return(np.where(np.random.multinomial(n=1,pvals = sx)==1)[0])

def findMarriedCouples(world):
	m = np.where(world.marriageStructure>0)
	return(zip(m[0],m[1]))

def marriages(world):
	nDeaf = sum([x.deafStatus for x in world.pop])
	nHearing = len(world.pop) - nDeaf
	
	# ideal proportions, as governed by the parameters
	idealNumMarriages_hearing = math.floor(world.parameters["proportionOfMarriedAgents"] * nHearing)
	idealNumMarriages_deaf = math.floor(world.parameters["proportionOfMarriedAgentsDeaf"]* nDeaf)
	
	# number we need to add in each modality
	shortage_hearing = nHearing - idealNumMarriages_hearing
	shortage_deaf = nDeaf - idealNumMarriages_deaf

	# numbers must be even
	shortage_hearing -= (shortage_hearing % 2)
	shortage_deaf -= (shortage_deaf % 2)
	
	#print "GET MARRIAGES INIT"
	mp = getMarriageProbs(world)
	
	while (shortage_hearing >0 or shortage_deaf >0) and np.sum(mp)>0:
		#print "WHILE"
		mpx = np.where(mp>0)
		chosenPartners = zip(mpx[0],mpx[1])[np.random.choice(range(len(mpx[0])), p=mp[mpx])]
		marryTwoAgents(world,int(chosenPartners[0]),int(chosenPartners[1]))
		
		# update marriage probs with new couple
		mp[chosenPartners] = 0
		mp[(chosenPartners[1],chosenPartners[0])] = 0
		# normalise probabilities
		if np.sum(mp)==0:
			break
		mp /= np.sum(mp)

		if world.pop[chosenPartners[0]].deafStatus:
			shortage_deaf -= 1
		else:
			shortage_hearing -= 1
		if world.pop[chosenPartners[1]].deafStatus:
			shortage_deaf -= 1
		else:
			shortage_hearing -= 1
		#minmp = np.min(mp)*0.01
		
		# If we've reached quota for a class, make these marriages unlikely
		if shortage_deaf<=0 and shortage_deaf >-2:
			deafx = [a.deafStatus for a in world.pop]
			deafx =  np.subtract.outer(deafx,deafx)
			mp[deafx] *= 0.01
			sumx = np.sum(mp)
			if sumx>0:
				mp /= sumx
			shortage_deaf = -2
		if shortage_hearing<=0 and shortage_hearing >-2:
			deafx = [not a.deafStatus for a in world.pop]
			deafx =  np.subtract.outer(deafx,deafx)
			mp[deafx] *= 0.01
			sumx = np.sum(mp)
			if sumx>0:
				mp /= sumx
			shortage_hearing = -2

# def getMarriageProbs_old(world):
# 	
# 	ms = copy.deepcopy(world.marriageStructure)
# 	ps = copy.deepcopy(world.popStructure)
# 	# exclude agents who have enough marriage partners
# 	married = np.where(np.sum(ms,axis=1)>=world.parameters["maxNumberOfMarriagePartners"])
# 	ps[married,:] = 0
# 	ps[:,married] = 0
# 	
# 	# exclude agents in the same compound
# 	cx = outer_equals(world.compounds)
# 	ps[np.where(cx==1)] = 0
# 	
# 	# exclude agents of the same sex
# 	g = [a.sex for a in world.pop]
# 	gx = abs(np.subtract.outer(g,g))
# 	ps[np.where(gx<0.5)] = 0
# 	
# 	# weight preferences by social structure
# 	dpref = copy.deepcopy(world.popStructure)
# 	dpref[:] = 0
# 	deafx = [a.deafStatus for a in world.pop]
# 	deafx =  np.subtract.outer(deafx,deafx)
# 	
# 	# weight social structure by marriage attitudes
# 	dpref[np.where(deafx)] = world.parameters["marriageAttitudes_deaf_deaf"]
# 	dpref[np.where(deafx==False)] = world.parameters["marriageAttitudes_deaf_hearing"]
# 	
# 	# manipulate dpref to exclude agents as above
# 	mpref = dpref * ps
# 	sump = np.sum(mpref)
# 	if sump>0:
# 		# normalise
# 		mpref = mpref /sump
# 	return mpref

def getMarriageProbs(world):
	"""Set marriage preferences based on seperate marriage weights,
	  and by communicative success"""

	ms = copy.deepcopy(world.marriageStructure)
	ps = copy.deepcopy(world.popStructure)
	# exclude agents who have enough marriage partners
	married = np.where(np.sum(ms,axis=1)>=world.parameters["maxNumberOfMarriagePartners"])
	ps[married,:] = 0
	ps[:,married] = 0
	
	
	# exclude agents in the same compound
	cx = outer_equals(np.array(world.compounds))
	# set to zero to exclude agents in same compound
	ps[np.where(cx==1)] *= world.parameters["compoundWeightMarry"]
	
	# weight by clans
	# (e.g. data suggests 50% chance marrying inside clan)
	clanx = outer_equals(np.array(world.clans))
	ps[np.where(clanx==1)] *= world.parameters["clanWeightMarry"]
	
	# exclude agents of the same sex
	g = np.array([a.sex for a in world.pop])
	gx = abs(np.subtract.outer(g,g))
	ps[np.where(gx<0.5)] = 0
	
	# set any negative values to zero
	#ps[np.where(ps<0)] = 0
	
	# weight preferences by communicative ability
	cs = getCommunicativeSimilarity(world) #* world.parameters["comSimilarityMarry"]
	cs *= world.parameters["comSimilarityMarry"]
	mpref = ps * cs
	# Normalise
 	sump = np.sum(mpref)
 	if sump>0:
 		# normalise
 		mpref = mpref /sump
 	return mpref


# def getMarriageProbs(world):
# 	
# 	ms = copy.deepcopy(world.marriageStructure)
# 	ps = copy.deepcopy(world.popStructure)
# 	# exclude agents who have enough marriage partners
# 	married = np.where(np.sum(ms,axis=1)>=world.parameters["maxNumberOfMarriagePartners"])
# 	ps[married,:] = 0
# 	ps[:,married] = 0
# 	
# 	# exclude agents in the same compound
# 	cx = outer_equals(world.compounds)
# 	ps[np.where(cx==1)] = 0
# 	
# 	# exclude agents of the same sex
# 	g = [a.sex for a in world.pop]
# 	gx = abs(np.subtract.outer(g,g))
# 	ps[np.where(gx<0.5)] = 0
# 	
# 	# weight preferences by social structure
# 	dpref = copy.deepcopy(world.popStructure)
# 	dpref[:] = 0
# 	deafx = [a.deafStatus for a in world.pop]
# 	deafx =  np.subtract.outer(deafx,deafx)
# 	
# 	# weight social structure by marriage attitudes
# 	dpref[np.where(deafx)] = world.parameters["marriageAttitudes_deaf_deaf"]
# 	dpref[np.where(deafx==False)] = world.parameters["marriageAttitudes_deaf_hearing"]
# 	
# 	# manipulate dpref to exclude agents as above
# 	mpref = dpref * ps
# 	sump = np.sum(mpref)
# 	if sump>0:
# 		# normalise
# 		mpref = mpref /sump
# 	return mpref

def getCommunicativeSimilarity(world):
	#signProp = [a.getMeaningCounts() for a in world.pop]
	#np.subtract.outer(signProp,signProp)
	
	# compare how well each agent can communicate
	mCounts = [a.getMeaningCounts() for a in world.pop]
	lx = len(mCounts)
	dist = np.zeros((lx,lx))
	# iterate through lower triangle
	for i in range(lx-1):
		for j in range((lx-1)-i):
			dist[i,j] = sum(np.abs(mCounts[i] - mCounts[j]))
	# copy accross diagonal
	
	dist[np.triu_indices(lx)] = dist[np.tril_indices(lx)]
	
	return dist + 0.001

def marryTwoAgents(world,a_index1,a_index2):
	world.marriageStructure[a_index1,a_index2] = 1
	world.marriageStructure[a_index2,a_index1] = 1
	world.changeSocialStructruresAfterMarriage(a_index1,a_index2)

def numberOfMarriedAgents(world):
	return sum(np.sum(world.marriageStructure, axis=1)>0)


def marriages_old(world):
	""" Arrange marriages until the number of marriages matches the proscribed number
	"""
	#print "Arrange marriages"
	
	if world.parameters["proportionOfMarriedAgents"] != world.parameters["proportionOfMarriedAgentsDeaf"]:
		marriages_sep(world)
	else:	
		max_num_of_attempts  = 10 # number of attempts at finding partners before giving up
		idealNumMarriages = math.floor(world.parameters["proportionOfMarriedAgents"] * world.nAgents)
		freeAgents =findCandidateTargets(world)
		attempts = 0
		if freeAgents > 0:
			while numberOfMarriedAgents(world) < idealNumMarriages and attempts < max_num_of_attempts:
				success = marriage(world)
				if not success:
					attempts += 1
				else:
					attempts = 0
		#print "finish marriages", numberOfMarriedAgents(world)
		#print world.marriageStructure
#	print countMarried(world,True),countMarried(world,False)
	

def marriages_sep(world):
	"""Arrange marraiges, but aim for different proportions of marraiges for hearing and non-hearing
	"""
#	print "start marriages"
	max_num_of_attempts  = 10 # number of attempts at finding partners before giving up
	
	# count number of deaf and hearing
	nDeaf = sum([x.deafStatus for x in world.pop])
	nHearing = len(world.pop) - nDeaf
	
	# ideal proportions, as governed by the parameters
	idealNumMarriages_hearing = math.floor(world.parameters["proportionOfMarriedAgents"] * nHearing)
	idealNumMarriages_deaf = math.floor(world.parameters["proportionOfMarriedAgentsDeaf"]* nDeaf)
	
	# number we need to add in each modality
	shortage_hearing = nHearing - idealNumMarriages_hearing
	shortage_deaf = nDeaf - idealNumMarriages_deaf
	#print idealNumMarriages_hearing,idealNumMarriages_deaf, len(set(world.compounds))
#	print world.compounds
	# If we got all the deaf people married first, then they would have a greater chance of being married
	# So, we choose a random order in which to address marriages
	opportunities = ([True] * int(shortage_deaf)) + ([False] * int(shortage_hearing))
	random.shuffle(opportunities)
	opcount = 0
	
	freeAgents =findCandidateTargets(world)
	attempts = [0,0]
	# aboslute cut off, in case we get into a loop
	cutoff = (shortage_hearing + shortage_hearing)*max_num_of_attempts*100
	ncount = 0
	# If there are people who are not married
	if freeAgents > 0:
		# while there are still marriages to add
		#  and we've failed less than 10 times in a row for a given modality
		while (ncount < cutoff) and ((countMarried(world, True) < idealNumMarriages_deaf and attempts[1] < max_num_of_attempts) or (countMarried(world, False) < idealNumMarriages_hearing and attempts[0] < max_num_of_attempts)):
			ncount += 1
			# find settings for the current modality
			#print attempts, opportunities
			modality = opportunities[opcount]
			ideal = {True: idealNumMarriages_deaf , False: idealNumMarriages_hearing}[modality]
			#print modality,attempts
			cm = countMarried(world,modality)
			# if we need to count more people
			if cm < ideal:
				# try marrying someone
				success = marriage(world,modality)
				if not success:
						#print "HERE"
						# if we didn't succeed, increase the attempts for the modality
						attempts[int(modality)] += 1
				else:
						# otherwise, re-set attempts, 
						attempts[int(modality)] = 0
						if len(opportunities)>1:
							opportunities.pop(opcount)
						
						# if we've found enough for one modality, only focus on the other
						#if (cm +1) >= ideal:
						#	opportunities = [x for x in opportunities if x!= modality]
						#	opcount = 0							
			opcount += 1
			# we might need to go through the list more than once, so set the opcount back to zero when at end
			if opcount >= len(opportunities):
				opcount = 0
	
	#print "finished marriages",countMarried(world,False),countMarried(world,True)
		
	

def countMarried(world,deafStatus=True):
	""" Count the number of married people, either in the deaf or hearing population"""
	mx = findMarriedCouples(world)
	dstatus = [a.deafStatus==deafStatus for a in world.pop]
	number_of_deaf_people_married = np.sum(np.sum(world.marriageStructure[np.where(dstatus),:], axis=2)>0)
	return number_of_deaf_people_married	



	
def marriage(world, deafStatus=None):
	# find agents elligible for marriage
	freeAgents =findCandidateTargets(world, deafStatus)
	if len(freeAgents) ==0:
		return(False)
	# choose a target agent to marry
	target = random.choice(freeAgents)
	# find compatible spouses
	candidates = findCandidatePartners(target, freeAgents, world)
	
	if len(candidates) >0:
		candidate_weights = getCandidateWeights(target,freeAgents,world)
		new_partner = (freeAgents[roulette_wheel(candidate_weights)])
		marryTwoAgents(world,target,new_partner)
		world.marriageStructure[target,new_partner] = 1
		world.marriageStructure[new_partner,target] = 1
		world.changeSocialStructruresAfterMarriage(target,new_partner)
		return(True)
	return(False)
	

def findCandidateTargets(world, deafStatus=None):
	spouses = np.sum(world.marriageStructure,axis = 1) 
	if deafStatus:
		return([i for i in range(world.nAgents) if spouses[i]<world.parameters["maxNumberOfMarriagePartners"] and world.pop[i].deafStatus == deafStatus])
	else:
		return([i for i in range(world.nAgents) if spouses[i]<world.parameters["maxNumberOfMarriagePartners"]])
	

def findCandidatePartners(target_agent_id, agent_ids,world):
	# can't marry self
	agent_ids.remove(target_agent_id)
	targetCompound = world.compounds[target_agent_id]
	targetSex = world.pop[target_agent_id].sex
	possibleCandidates = []
	for i in agent_ids:
		if world.pop[i].sex != targetSex: #Cant marry same gender
			if world.compounds[i] != targetCompound: #cant marry within compound
				possibleCandidates.append(i)
	return(possibleCandidates)
#	# must marry different sex
#	agent_ids = [i for i in agent_ids if abs(world.pop[target_agent_id].sex - world.pop[i].sex)>0.5]
#	# can't marry within compound
#	agent_ids  = [i for i in agent_ids if world.compounds[target_agent_id] != world.compounds[i]]
#	
#	return(agent_ids)
	

	
def getCandidateWeights(target_agent_id, agent_ids, world):

	# weight marriage by modality attitudes
	attitudes = world.parameters["marriageAttitudes"][world.pop[target_agent_id].deafStatus]
	cand_weights = [attitudes[world.pop[i].deafStatus] for i in agent_ids]
	
	# weight candidates by social links
	socialLinks = world.popStructure[target_agent_id,agent_ids] + 1
	
	#total_weights = [cand_weights[i] * socialLinks[i] for i in range(len(cand_weights))]
	total_weights = np.array(cand_weights) * np.array(socialLinks)
	return(total_weights)
	





