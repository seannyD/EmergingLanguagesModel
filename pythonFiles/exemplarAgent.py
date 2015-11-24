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
  #      self.children = 0

    def updateCache(self,datapair):
        "datapair = [modality, signal]"
        "modality = 0 (sign) or 1 (speech)"
        "signal = 0,...,n is an integer in the range nSpoken/ManualSigns"
        self.cache.append(datapair)


    def listen(self,datapair):
        if datapair == None:
            return None
        if self.deafStatus == True and datapair[0] ==1:
            return None
        else:
            if str(datapair[0]) in self.memory.keys():
                self.memory[str(datapair[0])].append(datapair[1])
            else:
                self.memory[str(datapair[0])] = [datapair[1]]
            self.updateCache(datapair)

    def attitude(self):
        "If I am not a signer, but I encounter a deaf person, what do I do?"
        # server mod
        #return [0,np.random.randint(self.nm)]
        return [0,random.randint(0,self.nm-1)]


    def speak(self, whoTo):
        "whoTo = another agentEpsilon instance"
        listenerStatus = whoTo.deafStatus #is the listener deaf?
        if listenerStatus == True:
            if "0" in self.memory.keys(): # do i know any signs?
            	# server mod
                #return np.array([0,np.random.choice(self.memory["0"])])
                return np.array([0,random.choice(self.memory["0"])])
            else: # If i don't know signs, what do i do?
                return self.attitude()
        else:
            if self.cache == []:
                if self.deafStatus == True:
                	#server mod
                    #datapair = np.array([0,np.random.randint(self.nm)])
                    datapair = np.array([0,random.randint(0,self.nm-1)])
                    self.memory["0"] = [datapair[1]]
                    self.cache.append(datapair)
                    return datapair
                else:
                    #chosenModality = stats.binom.rvs(n=1,p=self.alpha)
                    # server mod
                    chosenModality = stats.binom.rvs(1,self.alpha)
                    # server mod
                    #datapair = np.array([chosenModality,np.random.randint(self.nm)])
                    datapair = np.array([chosenModality,random.randint(0,self.nm-1)])
                    self.memory[str(chosenModality)] = [datapair[1]]
                    return datapair
            else:
            	# server mod
                #whichDatapair = np.random.choice(range(len(self.cache)))
                whichDatapair = random.choice(range(len(self.cache)))
                return self.cache[whichDatapair]
                


"Example Interaction"
signAgent, speechAgent = agentEpsilon(.55,deaf=True), agentEpsilon(.55)
def epsilonGame(speaker, hearer):
    utterance = speaker.speak(whoTo=hearer)
    hearer.listen(utterance)
    return speaker, hearer

signAgent, speechAgent = epsilonGame(signAgent,speechAgent)




def makeFirstPop(geneticParams):
    "Make an Initial population of agents according to the geneticParams"
    """e.g.

    popSize = geneticParams["popSize"]
    nDeaf = geneticParams["nDeaf"]
    speeachBias = geneticParams["alpha"]

    hearingPopulation = [agentEpsilon(speechBias) for i in range(popSize-nDeaf)]
    deafPopulation = [agentEpsilon(speechBias, deaf=True) for i in range(nDeaf)]
    return hearingPopulation+deafPopulation

    """
    return 0

def birthsDeaths(population,geneticParams,socialParams):
    "remove some, add some, based on geneticParams and socialParams"
    """
    removalRate = geneticParams["removalRate"]
    popSize = geneticParams[popSize]
    nRemovals = stats.binom.rvs(n=popSize, p = removalRate)
    """
    return 0

def chooseInterlocutors(population, socialParams):
    "Choose who interacts"
    return 0

def interact(speaker, listener):
    "Play a Language game"
    utterance = speaker.speak()
    updatedListener = listener.listen(whoTo=speaker)
    return speaker, updatedListener

def speakToEachOther(population, socialParams):
    "How does the interaction update agents' knowledge?"
    speaker, listener = chooseInterlocutors(population, socialParams)
    updatedSpeaker, updatedListener = interact(speaker, listener)
    return 0

def assess(population):
    "What quanitites are we interested in?"
    return 0

def simulationOutline(nInteractions, geneticParams,socialParams):
    metrics = []
    initialPopulation = makeFirstPop(geneticParams)
    for i in range(nInteractions):
        updatedGeneticPopulation = birthsDeaths(initialPopulation, geneticParams)
        updatedCulturalPopulation = speakToEachOther(updatedGeneticPopulation,socialParams)
        metrics.append(asses(updatedCulturalPopulation))
    finalPopulation = updatedCulturalPopulation
    return finalPopulation, metrics







