from populationStructure import *
import numpy as np
from exemplarAgent import *
from parameters import *
from genetics import *
from marriage import *
import copy

class InteractionsMaker:
  "Docstring"

  def __init__(self, world,filename="testfile.csv"):
      self.world = world
      self.filename = filename
      #f = open(self.filename,'w')
      #f.write("")
      #f.close()

  def metrics(self,stage):
      outString = ""
      stage = str(stage)
      for i in range(self.world.nAgents):
        thisAgent = self.world.pop[i]
#        print "MyMemory:", thisAgent.memory
        agentID = str(thisAgent.ID)
        if thisAgent.deafStatus == True:
          deafStatus = "1"
        else:
          deafStatus = "0"

        if "0" in thisAgent.memory.keys():
          nSigns = str(len(thisAgent.memory["0"]))
        else:
          nSigns = "0"
#        print "MYDEAGSTATUS", deafStatus
#        print "MYSINGS", nSigns
        if "1" in thisAgent.memory.keys():
          nSounds = str(len(thisAgent.memory["1"]))
        else:
          nSounds = "0"
        popString = ""
        ageString = str(a.age)
      #  for i in np.nditer(self.world.popStructure):
      #    popString += str(i)+"-"
        outString += ",".join([stage,agentID,deafStatus,nSigns,nSounds,popString,ageString])+"\n"
#      if write:
#        f = open(self.filename,'a')
#        f.write(outString)
#        f.close()
      return outString
      
        


  def interaction(self, speaker, listener):
      "Play an 'I speak you listen' language"
      utterance = speaker.speak(whoTo = listener)
#      print "utterance",utterance
      listener.listen(utterance)
      return speaker, listener

  def interactionsBatch(self):
      # pick agents in random order 
      #  (otherwise agent 0 always updates first)
      agentNums = np.arange(self.world.nAgents)
      random.shuffle(agentNums)
      for i in agentNums:
        "choose a partner"
        counts = copy.deepcopy(self.world.popStructure[i,].astype(np.float)) #Who have I seen before?
#        print "COUNTS",counts
        ps = counts/sum(counts) #Normalise my social counts into probabilities
        chosenPartner = np.where(np.random.multinomial(n=1,pvals = ps)==1)[0][0] #Use numpy multinomial to sample a partner
#        print "worldSize:", self.world.nAgents
#        print "chosenPartner", chosenPartner
#        print "me", i
        "Run an interaction and update the World"
        newSpeaker, newListener = self.interaction(self.world.pop[i], self.world.pop[chosenPartner])
        self.world.pop[i] = newSpeaker
        self.world.pop[chosenPartner] = newListener


  def simulateOneStage(self,stage,sampleEvery=20):
      self.interactionsBatch()
#      if stage == 0:
#        marriages(self.world)
      births_and_deaths(self.world)
#      print "NUMBER MARRIED",numberOfMarriedAgents(self.world)
#     increase age of agents
      [a.incAge() for a in self.world.pop]		
      if (stage % sampleEvery) ==0:
              return self.metrics(stage)
      else:
              return ""




