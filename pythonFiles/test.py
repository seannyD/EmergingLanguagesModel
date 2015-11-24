from populationStructure import *
from exemplarAgent import *
from parameters import *
from genetics import *
from marriage import *
from parameters import *
from interactions import *

world1 = world(kolok_parameters["nAgents"],propDeaf=0.0,alpha=0.5, nManualSigns=10, nSpokenSigns= 10,parameters=kolok_parameters)
assignGenetics(world1)
marriages(world1)

im = InteractionsMaker(world1)

births_and_deaths(world1)

im.interactionsBatch()

