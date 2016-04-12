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

    def __init__(self,alpha,nManualSigns = 10, nSpokenSigns = 10, deaf=False, sex=0, genes=(0,0), ID=-1, nConcepts = 5):
        """

        alpha: prior probability of using speech
        nCOncepts: how many concepts exist?
        nManualSigns: how many manual signs are possible?
        nSpokenSigns: how many spoken signs are posssible?

        Usage Example: speechAgent = agentEpsilon(.55), signAgent = agentEpsilon(0.55,deaf=True)

        """
        self.alpha = alpha # 0<=alpha<=1 is the "speech bias" for non deaf agents
        self.nm = nManualSigns #How many manual signs possible?
        self.ns = nSpokenSigns #How many Spoken signs possible? NOTE: it should be true that ns=nm
        self.nc = nConcepts
        self.deafStatus = deaf #Am I deaf?
        self.memory = np.zeros((2,self.nc,self.ns))
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

    def updateCache(self,data):
        "data = [modality, meaning, signal]"
        "modality = 0 (sign) or 1 (speech)"
        "meaning = 0,...,m is an integer in the range self.nc"
        "signal = 0,...,n is an integer in the range self.ns"
        modality, meaning, signal = data[0],data[1],data[2]
        self.memory[modality,meaning,signal] +=1


    def listen(self,data):
        if data == None:
            return None
        if self.deafStatus and data[0] ==1:
            return None
        else:
            modality, meaning, signal = data[0],data[1],data[2]
            self.memory[modality, meaning, signal] += 1

    def attitude(self,meaning):
        "If I am not a signer, but I encounter a deaf person, what do I do?"
        chosenSign = np.random.randint(self.nm)
        self.memory[0,meaning,chosenSign] +=1
        return np.array([0,meaning,chosenSign])
        # server mod
        #return [0,random.randint(0,self.nm-1)]


    def speak(self, whoTo):
        "whoTo = another agentEpsilon instance"
        meaning = random.randint(0,self.nc-1)
        signMemory = self.memory[0,meaning,:] #The signs I know for this meaning
        vocalMemory = self.memory[1,meaning,:] #The signs I know for this meaning
        listenerStatus = whoTo.deafStatus #is the listener deaf?
        if listenerStatus == True:
            nSigns = sum(signMemory)
            if nSigns > 0: # do i know any signs?
                ps = signMemory/nSigns
                chosenSign = np.where(np.random.multinomial(1,pvals = ps)==1)[0][0]
                return [0,meaning,chosenSign]
            	# server mod
                #return np.array([0,random.choice(self.memory["0"])])
            else: # If i don't know signs, what do i do?
                return self.attitude(meaning=meaning)
        else:
            if np.sum(self.memory) == 0:
                if self.deafStatus == True:
                	#server mod
                	#datapair = np.array([0,random.randint(0,self.nm-1)])
                    chosenSign = np.random.randint(self.nm)
                    datapair = np.array([0,meaning, chosenSign])
                    self.memory[0,meaning,chosenSign] += 1
                    return datapair
                else:
                    chosenModality = stats.binom.rvs(n=1,p=self.alpha)
                    # server mod
                    #chosenModality = stats.binom.rvs(1,self.alpha)
                    chosenSign = np.random.randint(self.nm)
                    datapair = np.array([chosenModality,meaning,chosenSign])
                    # server mod
                    #datapair = np.array([chosenModality,random.randint(0,self.nm-1)])
                    self.memory[0,meaning,chosenSign] += 1
                    return datapair
            else:
                signs = self.memory[0,meaning,:]
                sounds = self.memory[1,meaning,:]
                totalSum = sum(signs)+sum(sounds)
                allKnownSignals = [signs,sounds]

                signProb = (sum(signs)/totalSum) *(1-self.alpha)
                soundProb = (sum(sounds)/totalSum)* self.alpha

                totalProb = signProb+soundProb

                chosenModality = stats.binom.rvs(n=1,p=soundProb)
                contenders = allKnownSignals[chosenModality]
                contenderPs = contenders/sum(contenders)

                chosenSignalIndex =  np.where(np.random.multinomial(1,contenderPs)==1)[0][0]

                return [chosenModality,meaning,chosenSignalIndex]



"Example Interaction"
signAgent, speechAgent = agentEpsilon(.55,deaf=True), agentEpsilon(.55)
def epsilonGame(speaker, hearer):
    utterance = speaker.speak(whoTo=hearer)
    hearer.listen(utterance)
    return speaker, hearer

signAgent, speechAgent = epsilonGame(signAgent,speechAgent)

