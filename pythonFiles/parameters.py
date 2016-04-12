import csv, random

def readParameters():
	filename = "../parameters/KK_Model_parameters.csv"
	params = {}
	with open(filename, 'rb') as csvfile:
		lreader = csv.reader(csvfile, delimiter=',')
		header = ""
		for row in lreader:
			if header=="":
				header = row
			else:
				px = dict(zip(header,row))
				params[int(px["Number"])] = px

	# convert to numbers
	for d in params.keys():
		for attr in params[d].keys():
			if params[d][attr].count("."):
				try:
					params[d][attr] = float(params[d][attr])
				except:
					pass
			else:
				try:
					params[d][attr] = int(params[d][attr])
				except:
					pass
		
	default = params[1]
	
	# fill in defaults
	for d in params.keys()[1:]:
		for attr in params[d].keys():
			if params[d][attr]=="":
				params[d][attr] = default[attr]
	return params

def getParameters(num):
	
	params = readParameters()
	chosenParams = params[num]
	params = createParameters(chosenParams)
	
	params["FolderName"] = "../results/" + params["RunName"] +"/"
	params["ParamFileName"] = params["FolderName"] + params["RunName"] + "_parameters.p"
	# the server will run these programs independetly,
	# so let's just add a random number to the file names
	params["ResultsFileName"] = params["FolderName"] + params["RunName"] + str(random.randint(0,1000)) + ".res"
	return params
# def getResults(Number,nRuns):
# 	paramsRow = df[df.Number==Number]
# 	theseParams = buildParamsDict(paramsRow)
# 	runName = theseParams['RunName']
# 	os.makedirs(runName)
# 	filenameBase = '/runName/'
# 	for run in range(nRuns):
# 		coda = str(run)+.txt
# 		thisRunFilename = filenameBase + coda
# 		simulation(nStages,parameters = theseParams,filename=thisRunFilename)
# 	



basic_parameters = {}
basic_parameters["nAgents"] = 10
basic_parameters["alpha"]=0.9
basic_parameters["nManualSigns"]=10
basic_parameters["nSpokenSigns"]= 10
basic_parameters["initialDeafLocations"] = "Random"  # or "Clan" or "Compound"


kolok_parameters = basic_parameters

kolok_parameters["nAgents"] = 20#2189
kolok_parameters["nClans"] = 10
kolok_parameters["MaxSizeCompounds"] = 3#25

kolok_parameters["clanWeight"] = 3
kolok_parameters["compoundWeight"] = 4
kolok_parameters["genderWeight"] = 2
kolok_parameters["deafCommunityWeight"] = 1
kolok_parameters["maxWeight"] = kolok_parameters["clanWeight"] + kolok_parameters["compoundWeight"] + kolok_parameters["genderWeight"] + kolok_parameters["deafCommunityWeight"] + 1

# This applies to the start of the simulation
kolok_parameters["gCarry"] = 0.176 # proportion of hearing people carrying deaf variant
kolok_parameters["gDom"] = 0.022 # proportion of deaf people

kolok_parameters["probOfBirthDeathEachStage"] = 0.99
kolok_parameters["maxNumberOfBirthDeathEachStage"] = 3

kolok_parameters["maxNumberOfMarriagePartners"]  = 1
kolok_parameters["proportionOfMarriedAgents"]  = 0.64
kolok_parameters["proportionOfMarriedAgentsDeaf"]  = 0.85


probHearingDeafMarriage = 3 / float(2189)
probHearingHearingMarriage = 1 - probHearingDeafMarriage
									      #deaf  + [ deaf        hearing      ]
kolok_parameters["marriageAttitudes"] = { True:    {True:0.875  ,  False: 0.125 },
										  # hearing +[deaf         hearing
										  False:    {True:probHearingDeafMarriage  ,  False: probHearingHearingMarriage }
								}
								
								
def createParameters(d):
	""" take a dictionary of bits and make a properly formatted parameter dictionary"""
	
	d["maxWeight"] = 1 + d["clanWeight"] + d["compoundWeight"] +d["genderWeight"] + d["deafCommunityWeight"]
	d["marriageAttitudes"] = {True : 
		{True:d["marriageAttitudes_deaf_deaf"], False:d["marriageAttitudes_deaf_hearing"]},
		False: {True:d["marriageAttitudes_hearing_deaf"], False:d["marriageAttitudes_hearing_hearing"]}
		}
	
	return d
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	