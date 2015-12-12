from marriage import *
from populationStructure import *
from parameters import *
import copy
import numpy as np

def marriages2(world):
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
	
	mp = getMarriageProbs(world)
	
	while (shortage_hearing >0 or shortage_deaf >0) and np.sum(mp)>0:
#		print "CURRENT MARRIAGE"
#		print w.marriageStructure
		mpx = np.where(mp>0)
		#print zip(mpx[0],mpx[1])
		#print mp[mpx]
		# choose people to marry
		chosenPartners = zip(mpx[0],mpx[1])[np.random.choice(range(len(mpx[0])), p=mp[mpx])]
#		print "CHOSEN",chosenPartners
		# marry them!
		marryTwoAgents(world,int(chosenPartners[0]),int(chosenPartners[1]))
#		print w.marriageStructure
		# update marriage probs
		mp = getMarriageProbs(world)
		if world.pop[chosenPartners[0]].deafStatus:
			shortage_deaf -= 1
		else:
			shortage_hearing -= 1
		if world.pop[chosenPartners[1]].deafStatus:
			shortage_deaf -= 1
		else:
			shortage_hearing -= 1
		minmp = np.min(mp)*0.01
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
			shortage_hearing = -1
#		print "CURRENT MARRIAGEXXX"
#		print w.marriageStructure
	

		
	
	


def getMarriageProbs(world):
	
	ms = copy.deepcopy(world.marriageStructure)
	
#	print ms
	ps = copy.deepcopy(world.popStructure)
#	print ps
	
	# exclude agents who have enough marriage partners
	married = np.where(np.sum(ms,axis=1)>=world.parameters["maxNumberOfMarriagePartners"])
	#print "MARRIED"
	#print married
	#print ps
	ps[married,:] = 0
	ps[:,married] = 0
#	print ps
#	ps[np.where(ms>world.parameters["maxNumberOfMarriagePartners"])] = 0
#	print ps
	
	# exclude agents in the same compound
	cx = outer_equals(world.compounds)
#	print cx
	ps[np.where(cx==1)] = 0
	
	# exclude agents of the same sex
	g = [a.sex for a in world.pop]
	gx = abs(np.subtract.outer(g,g))
	ps[np.where(gx<0.5)] = 0
	
	# weight preferences by social structure
	dpref = copy.deepcopy(world.popStructure)
	dpref[:] = 0
	deafx = [a.deafStatus for a in world.pop]
#	print deafx
	deafx =  np.subtract.outer(deafx,deafx)
#	print deafx
#	print world.parameters["marriageAttitudes_deaf_hearing"]
	dpref[np.where(deafx)] = world.parameters["marriageAttitudes_deaf_deaf"]
	dpref[np.where(deafx==False)] = world.parameters["marriageAttitudes_deaf_hearing"]
	
#	print "DPREF"
#	print dpref
#	print "PS"
#	print ps
	
	mpref = dpref * ps
#	print "MPREF"
#	print mpref
	sump = np.sum(mpref)
	if sump>0:
		mpref = mpref /sump
#	print mpref
	return mpref
	




parameters = getParameters(14)
parameters["nAgents"] = 500

w = world(parameters)
for i in range(len(w.pop)):
	w.pop[i].deafStatus = i>=3
marriages2(w)
#print "END"
#print w.marriageStructure


