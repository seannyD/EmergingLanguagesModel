from marriage import *
from parameters import *
from interactions import *



def simulation(nStages,filename):
	world1 = world(kolok_parameters)
	im = InteractionsMaker(world1,filename=filename)
	marriages(im.world)

	for stage in xrange(nStages):
		im.simulateOneStage(stage)
		if (stage % 3) ==0:
			marriages(im.world)
			im.world.rebalance_structures()
	return world1

x = simulation(50,"../results/text.tab")
