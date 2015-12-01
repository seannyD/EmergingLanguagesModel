library(plyr)
library(ggplot2)
library(lattice)
setwd("~/Documents/MPI/EmergingLanguages/SignSpeechConnieBill/Model/")



plotMeanRun = function(dx, plotIndividualRuns=T){
	px = ggplot(data=dx, aes(x=stage, y=prop.deaf, group=runName)) +
	 geom_smooth(aes(colour=runName), lwd=2)  +
	 xlab("") +
	 ylab("Proportion of\ndeaf agents") +
	 theme(legend.position="top", axis.title.y=element_text(angle=0),legend.title=element_blank())  

	 if(plotIndividualRuns){
	 	px = px + 	geom_line(aes(group=runNameNum, colour=runName), alpha=0.2)
	 }

	return(px)
}

plotMeanHearingSigns = function(dx, plotIndividualRuns=T){
	px = ggplot(data=dx, aes(x=stage, y=prop.signs,group=runName))+
	geom_smooth(aes(colour=runName), lwd=2) +
	xlab("Stages") +
	ylab("Proportion\nof signs\nper hearing\nagent")+
	 theme(legend.position="top", axis.title.y=element_text(angle=0), legend.title=element_blank())
	 
	 if(plotIndividualRuns){
	 	px = px + geom_line(aes(group=runNameNum, colour=runName), alpha=0.2)
	 }
	 return(px)
	}



loadData = function(paramName){
	
	param = params[params$RunName==paramName,]
	popSize = param$nAgents
	#popSize = 76
	
	folder = paste("results/", paramName,'/',sep='')
	res = data.frame()
	files = list.files(folder,"*.res")
	
	for(i in 1:length(files)){
		d = read.csv(paste(folder,files[i],sep=''),header=T,quote='')
		names(d) = c("stage","id","deaf","signs","sounds")
		d$prop.signs = d$signs/(d$signs+d$sounds)
	d$prop.signs[is.nan(d$prop.signs)] = 0
		d$runNum = i
		res = rbind(res,d)
	}
	
	ressum = ddply(res, .(runNum,stage), summarize, prop.signs = mean(prop.signs), nDeaf = sum(deaf))
	ressum$runName = paramName
	ressum$runNameNum = paste(ressum$runName,ressum$runNum)
	
	ressum$prop.deaf = ressum$nDeaf / popSize
	
	return(ressum)
}


##########


params = read.csv("Parameters/KK_Model_parameters.csv")

kk = loadData("Test")

genetics = rbind(
	loadData("KK_LowIncidence"),
	kk,
	loadData("KK_HighIncidence")
)


test2 = rbind(
	loadData("KK_DeafMarriageTabooModerate"),
	loadData("BulelengGeneralSituation")
)

plotMeanRun(test2)


test3 = rbind(
	loadData("KK_Default"),
	loadData("KK_SmallCommunity"),
	loadData("KK_LargeCommunity")
)

test3[test3$runName=="KK_Default",]$runName = "Medium"
test3[test3$runName=="KK_SmallCommunity",]$runName = "Small"
test3[test3$runName=="KK_LargeCommunity",]$runName = "Large"


plotMeanRun(test3,plotIndividualRuns=F)
plotMeanHearingSigns(test3,plotIndividualRuns=F)