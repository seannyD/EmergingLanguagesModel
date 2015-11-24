import numpy as np
from scipy import stats
import string
import random
import math
import copy
from collections import Counter


from exemplarAgent import *
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


def RUN_INTERACTION(agentA,agentB):
    pass

def outer_equals(x):
	x = abs(np.subtract.outer(x,x))
	x[x <> 0] = -1
	x[x ==0] = 1
	x[x ==-1] = 0
	return(x)


class world:
    """A world of interacting agents
    """
    
    
    def __init__(self,parameters = {}):

        self.parameters = parameters    

        self.nAgents = self.parameters["nAgents"]
        self.alpha = self.parameters["alpha"]
        self.nManualSigns = self.parameters["nManualSigns"]
        self.nSpokenSigns = self.parameters["nSpokenSigns"]
#        self.propDeaf = propDeaf

        self.makePopulation()
        assignGenetics(self)
        self.setUpSocialStructure()
        
        self.setUpMarriageStructure()
		
        self.idCounter = self.nAgents
        self.initialNumberOfClans = len(set(self.clans))
        self.initialNumberOfCompounds = len(set(self.compounds))
        self.compound_clan_dictionary = dict(set([(self.compounds[i],self.clans[i]) for i in range(len(self.clans))]))
        	
        
    def makePopulation(self):
        """
        Make a population of agents.  Assign all hearing for now, the use genetics to assign deafness
        """
       # nHearing = int(round(float(self.nAgents) * (1-self.propDeaf)))
        #nDeaf = int(math.ceil(float(self.nAgents) * self.propDeaf))
        # create population of agents (just an array of agentEpsilon instances)
        self.pop = [agentEpsilon(self.alpha,self.nManualSigns, self.nSpokenSigns , deaf=False, sex=random.choice([0,1]), ID= i)  for i in range(self.nAgents)]
        
        
        
    def setUpSocialStructure(self):
        """ The social structure is a 2 dimensional array, with shape nAgents x nAgents
        Each entry indicates the probability of a pair interacting
        """
      
        # create clans
        clans = range(self.parameters["nClans"]) * int(math.ceil(self.nAgents/float(self.parameters["nClans"])))
        clans = clans[:self.nAgents]
        self.clans = sorted(clans)
       
       # fill compounds
        self.compounds = [0]
        currentComp = 0
        compCount = 0
        for i in range(len(self.clans))[1:]:
            if self.clans[i]==self.clans[i-1]:
                 self.compounds.append(currentComp)
                 compCount += 1
                 if self.compounds.count(currentComp)>= self.parameters["MaxSizeCompounds"]:
                     currentComp += 1
            else:
            	currentComp += 1
            	self.compounds.append(currentComp)
            	compCount = 1
		# get social structures
        self.popStructure = self.getSocialStructure()
        
    def getClanStructure(self):
    	return(outer_equals(self.clans) * self.parameters["clanWeight"])
        
    def getCompoundStructure(self):
        return(outer_equals(self.compounds) * self.parameters["compoundWeight"])
        
    def getGenderStructure(self):
    	return(outer_equals([x.sex for x in self.pop]) * self.parameters["genderWeight"])
    
    def getDeafCommunityStructure(self):
    	# this is a matrix which is only 1 if both people are deaf (no advnatage for hearing-hearing)
    	d = [int(a.deafStatus) for a in self.pop]
    	return(np.outer(d,d) * self.parameters["deafCommunityWeight"])
    
    def getSocialStructure(self):
        # some chance of communicating with everyone
        dx = len(self.pop)
        sStructure = np.ones((dx,dx))

    	clanPopStructure = self.getClanStructure()
        compoundPopStructure = self.getCompoundStructure()
        genderPopStructure = self.getGenderStructure()
        deafCommunityStructure = self.getDeafCommunityStructure()
        
        #print clanPopStructure.shape, compoundPopStructure.shape, genderPopStructure.shape, deafCommunityStructure.shape
        
        
        # add social structures
        sStructure += clanPopStructure + compoundPopStructure + genderPopStructure + deafCommunityStructure
        # zero chance of communicating with self.
        np.fill_diagonal(sStructure, 0.0)
        
        return(sStructure)

    def setUpMarriageStructure(self):
    	self.marriageStructure = np.zeros((self.nAgents,self.nAgents))
    	
    
#    def updateSocialStructure(self,pop_index_i, pop_index_j,amount=1):
#        self.popStructure[pop_index_i,pop_index_j] += 1
        # keep symmetrical
#        self.popStructure[pop_index_j,pop_index_i] += 1
        
        
#    def normaliseSocialStructure(self):
#        # divide each number by the sum of the matrix
#        self.popStructure = self.popStructure / np.sum(self.popStructure)
        
    def choosePairs(self):
        """For each agent, choose another person to communicate with.
        Each agent will communicate at least once
        """
       
        return([roulette_wheel(self.popStructure[i,]) for i in range(self.popStructure.shape[0])])
    
    
    
    def addAgent(self, new_agent, parent_agent, secondary_caregivers):
        """Add an agent to the population, in the parent_agent's clan and compound,
           With strong social links to parent_agent and all in secondary_caregivers
        """
        # set unique id
        new_agent.ID = self.idCounter
        self.idCounter += 1
        
        self.pop.append(new_agent)
        newPopStructure = np.zeros((self.popStructure.shape[0]+1,self.popStructure.shape[1]+1))
        newPopStructure[:-1,:-1] = self.popStructure

        
        # inherit social structure from parent
        parent_id = self.findAgentIndexById(parent_agent)
        secondary_caregivers_ids = [self.findAgentIndexById(a) for a in secondary_caregivers]
        newPopStructure[-1,] = newPopStructure[parent_id,]
        newPopStructure[:,-1] = newPopStructure[:,parent_id]   

		# strong bond between parents
        newPopStructure[-1,parent_id] = self.parameters["maxWeight"]
        newPopStructure[parent_id,-1] = self.parameters["maxWeight"]
        for s in secondary_caregivers_ids:
        	newPopStructure[-1,s] =self.parameters["maxWeight"]
        	newPopStructure[s,-1] =self.parameters["maxWeight"]

        # can't communicate with self
        np.fill_diagonal(newPopStructure, 0.0)
        
        self.popStructure = newPopStructure
        
        # start unmarried
        newMarriageStructure = np.zeros((self.marriageStructure.shape[0]+1,self.marriageStructure.shape[1]+1))
        newMarriageStructure[:-1,:-1] = self.marriageStructure
        newMarriageStructure[-1,] = 0
        newMarriageStructure[:,-1] = 0
        self.marriageStructure = newMarriageStructure
        
		# inherit clan from parent
        parent_clan = self.clans[parent_id]
        parent_compound = self.compounds[parent_id]
        
        self.clans.append(parent_clan)
        self.compounds.append(parent_compound)

        self.nAgents  = len(self.pop)

#     def findAgentIndexById(self,agent):
#     	#print agent
#     	return([i for i in range(len(self.pop)) if self.pop[i].ID == agent.ID][0])

    def findAgentIndexById(self,agent):
    	for i in range(len(self.pop)):
    		if self.pop[i].ID == agent.ID:
    			return i

    def removeAgent(self,agent):
    	agent_index = self.findAgentIndexById(agent)
    	# remove (pop) item from population
        self.pop.pop(agent_index)
        # remove from population structure
      #  self.popStructure =np.delete(self.popStructure, agent_index ,axis=0)
     #   self.popStructure =np.delete(self.popStructure, agent_index ,axis=1)
        
        # remove marriage links
        self.marriageStructure[agent_index,:] = 0
        self.marriageStructure[:,agent_index] = 0
        
        self.marriageStructure =np.delete(self.marriageStructure,agent_index,axis=0)
        self.marriageStructure =np.delete(self.marriageStructure,agent_index,axis=1)
        
        # remove from social structure
        self.popStructure = np.delete(self.popStructure, agent_index ,axis=0)
        self.popStructure = np.delete(self.popStructure, agent_index ,axis=1)
        
        self.compounds.pop(agent_index)
        self.clans.pop(agent_index)
        
        self.nAgents  = len(self.pop)
	
	
    def changeSocialStructruresAfterMarriage(self,target,new_partner):
		if not type(target) is int:
			target = self.findAgentIndexById(target)
		if not type(new_partner) is int:
			new_partner = self.findAgentIndexById(new_partner)
			
		groom_id = target
		bride_id = new_partner
		if self.pop[target].sex > 0.5: # if target is female:
			groom_id = new_partner
			bride_id = target

		# patrilocal residence: change bride's clan and compound
		self.compounds[bride_id] = self.compounds[groom_id]
		self.clans[bride_id] = self.clans[groom_id]
		
		# female adopts default social structure for male's clan and compound
		self.popStructure[bride_id,:] = self.getSocialStructure()[bride_id,:]
		self.popStructure[:,bride_id] = self.getSocialStructure()[:,bride_id]
		
		# strong bond between husband and wife
		self.popStructure[bride_id,groom_id] = self.parameters["maxWeight"]
		self.popStructure[groom_id, bride_id] = self.parameters["maxWeight"]
        # zero chance of communicating with self.
		np.fill_diagonal(self.popStructure, 0.0)

    def getCompoundCounts(self):
    	return [(i,sum([z==i for z in self.compounds])) for i in range(self.initialNumberOfCompounds)]
    	

    def rebalance_structures(self):
		"""Find compounds with zero people.  Find the largest compound, and send half the people
		to adopt the empty compound, along with its clan.  
		That is, keep the number of clans and compouds equal
		"""
#		print "REBALANCE"
		comps = set(self.compounds)
		clans = set(self.clans)
		
		
		
		while len(set(self.compounds)) < self.initialNumberOfCompounds:
			
			comps_cnt = self.getCompoundCounts()
			# find (first) biggest compound
			maxC = max([x[1] for x in comps_cnt])
			biggest = random.choice([x[0] for x in comps_cnt if x[1]==maxC])
			zeroCompound = random.choice([x[0] for x in comps_cnt if x[1]==0])

			newCompound = np.array(copy.deepcopy(self.compounds))
			# pick all people in the biggest compond
			toChange = np.where(newCompound==biggest)[0]
			
			propToChange = int(len(toChange)/2.0)
			if propToChange ==0:
				propToChange = 1
			if propToChange > self.parameters["MaxSizeCompounds"]:
				propToChange = self.parameters["MaxSizeCompounds"]
			
			# pick newest people in compound

			#toChange = np.ndarray.tolist(toChange)
			toChange = toChange[:propToChange]

			newCompound[toChange] = zeroCompound

			self.compounds = np.ndarray.tolist(newCompound)

			newClan = self.compound_clan_dictionary[zeroCompound]
			newClans = np.array(copy.deepcopy(self.clans))
			newClans[toChange] = newClan
			self.clans= np.ndarray.tolist(newClans)
