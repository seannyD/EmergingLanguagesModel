import numpy as np
from scipy import stats
import string
import random



class agentEpsilon:
    """Im an Agent Template.
        I only know one concept, but I can learn learn signals for that
        concept in two modalities. I know whether my interlocutor is deaf or not,
        and I adopt my signal use accordingly. If the person Im speaking to
        isn't deaf, I choose which modality to use according to alpha.
    """

    def __init__(self,alpha,nManualSigns = 10, nSpokenSigns = 10, deaf=False, sex=0, genes=(0,0), ID=-1):
        """

        alpha: prior probability of using speech
        nCOncepts: how many concepts exist?
        nManualSigns: how many manual signs are possible?
        nSpokenSigns: how many spoken signs are posssible?

        Usage Example: speechAgent = agentEpsilon(.55), signAgent = agentEpsilon(0.55,deaf=True)

        """
        self.alpha = alpha # 0<=alpha<=1 is the "speech bias" for non deaf agents
        self.nm = nManualSigns #How many manual signs possible?
        self.ns = nSpokenSigns #How many Spoken signs possible?
        self.deafStatus = deaf #Am I deaf?
        self.memory = {} #Memory for exemplars i enounter: e.g. "0":[3,6,...,4] means I know signals [3,6,...,4] for manual modality
        self.cache = []
        self.sex = sex
        self.genes = genes
        self.ID = ID
        self.age = 0
  #      self.children = 0

    def getSignProp(self):
		""" Return the proportion of signs in the memory"""
		if len(self.memory.keys())==0:
			return 0
		nsign = len(self.memory["0"])
		nspeech = len(self.memory["1"])
		if nsign ==0:
			return 0.0
		if  nspeech ==0:
			return 1.0
		return nsign/float(nspeech+nsign)

    def incAge(self):
        self.age += 1

    def getMeaningCountsM(self,modality):

    	# TODO: this currently gets the proporiton of signed to spoken signals for each signal type
    	# however, it was intended to do it by meaning, not by signal type.

		if not modality in self.memory.keys():
			if modality=="0":
				return np.array([0] * self.nm)
			else:
				return np.array([0] * self.ns)

		if modality=="0":
			return np.array([self.memory[modality].count(x) for x in range(self.nm)],dtype='float')
		if modality=="1":
			return np.array([self.memory[modality].count(x) for x in range(self.ns)],dtype='float')


    def getMeaningCounts(self):
    	dM = self.getMeaningCountsM("0")
    	hM = self.getMeaningCountsM("1")
    	ret = dM + hM

    	ret_max = np.max(ret)
    	if ret_max==0:
    		return ret
    	return ret / np.max(ret)

    def updateCache(self,datapair):
        "datapair = [modality, signal]"
        "modality = 0 (sign) or 1 (speech)"
        "signal = 0,...,n is an integer in the range nSpoken/ManualSigns"
        self.cache.append(datapair)


    def listen(self,datapair):
        if datapair == None:
            return None
        if self.deafStatus and datapair[0] ==1:
            return None
        else:
            if str(datapair[0]) in self.memory.keys():
                self.memory[str(datapair[0])].append(datapair[1])
            else:
                self.memory[str(datapair[0])] = [datapair[1]]
            self.updateCache(datapair)

    def attitude(self):
        "If I am not a signer, but I encounter a deaf person, what do I do?"

        return [0,np.random.randint(self.nm)]
        # server mod
        #return [0,random.randint(0,self.nm-1)]


    def speak(self, whoTo):
        "whoTo = another agentEpsilon instance"
        listenerStatus = whoTo.deafStatus #is the listener deaf?
        if listenerStatus == True:
            if "0" in self.memory.keys(): # do i know any signs?

                return np.array([0,np.random.choice(self.memory["0"])])
            	# server mod
                #return np.array([0,random.choice(self.memory["0"])])
            else: # If i don't know signs, what do i do?
                return self.attitude()
        else:
            if self.cache == []:
                if self.deafStatus == True:
                	#server mod
                	#datapair = np.array([0,random.randint(0,self.nm-1)])
                    datapair = np.array([0,np.random.randint(self.nm)])

                    self.memory["0"] = [datapair[1]]
                    self.cache.append(datapair)
                    return datapair
                else:
                    chosenModality = stats.binom.rvs(n=1,p=self.alpha)
                    # server mod
                    #chosenModality = stats.binom.rvs(1,self.alpha)

                    datapair = np.array([chosenModality,np.random.randint(self.nm)])
                    # server mod
                    #datapair = np.array([chosenModality,random.randint(0,self.nm-1)])
                    self.memory[str(chosenModality)] = [datapair[1]]
                    return datapair
            else:

                whichDatapair = random.choice(range(len(self.cache)))
                # server mod
                #whichDatapair = np.random.choice(range(len(self.cache)))
                return self.cache[whichDatapair]



"Example Interaction"
signAgent, speechAgent = agentEpsilon(.55,deaf=True), agentEpsilon(.55)
def epsilonGame(speaker, hearer):
    utterance = speaker.speak(whoTo=hearer)
    hearer.listen(utterance)
    return speaker, hearer

signAgent, speechAgent = epsilonGame(signAgent,speechAgent)

