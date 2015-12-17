library(plyr)
library(ggplot2)
library(lattice)
setwd("~/Documents/MPI/EmergingLanguages/SignSpeechConnieBill/Model/")

# 500 stages = 70 years
timescale = 70/500

makePDF = function(pdfName,widthx){
  pdf(paste("analysis/graphs/",pdfName,sep=''),width=widthx,height=4)
}

fixLabels = function(dx,labs){
  current_labs = unique(dx$runName)
  for(i in 1:length(current_labs)){
    dx[dx$runName==current_labs[i],]$runName = labs[i]
  }
  dx$runName = factor(dx$runName,levels = labs)
  #dx$runName = relevel(dx$runName,labs[i])
  return(dx)
}

plotMeanRun = function(dx, labels, plotIndividualRuns=F,pdfName=NA,plotYears = T,widthx=4,ylimx=c(0,10.5)){
  
  if(!is.na(pdfName)){
    makePDF(pdfName,widthx)
  }
  dx = fixLabels(dx,labels)
  
  if(plotYears){
	  px = ggplot(data=dx, aes(x=year, y=prop.deaf, group=runName)) 
  } else{
    px = ggplot(data=dx, aes(x=stage, y=prop.deaf, group=runName))  
  }
	  
	px = px + geom_smooth(aes(colour=runName), lwd=2)  +
	 xlab("Years") +
	 ylab("% Deaf Individuals") +
#	  coord_cartesian(ylim=ylimx) +
	 theme(legend.position="top", axis.title.y=element_text(angle=90),legend.title=element_blank())  

	 if(plotIndividualRuns){
	 	px = px + 	geom_line(aes(group=runNameNum, colour=runName), alpha=0.2)
	 }
	print(px)
	if(!is.na(pdfName)){
	  dev.off()
	}
	return(px)
}

plotMeanHearingSigns = function(dx,labels, plotIndividualRuns=F,pdfName=NA,plotYears = T,widthx=4,ylimx=c(0,40)){
  
  if(!is.na(pdfName)){
    makePDF(pdfName,widthx)
  }
  
  dx = fixLabels(dx,labels)
  
  if(plotYears){
   	px = ggplot(data=dx, aes(x=year, y=prop.signs,group=runName))
  } else{
    px = ggplot(data=dx, aes(x=stage, y=prop.signs,group=runName))
  }
	px = px +geom_smooth(aes(colour=runName), lwd=2) +
	xlab("Years") +
	ylab("% Sign Vocabulary of Hearing Individuals")+
#	  coord_cartesian(ylim=ylimx) +
	 theme(legend.position="top", axis.title.y=element_text(angle=90), legend.title=element_blank())
	 
	 if(plotIndividualRuns){
	 	px = px + geom_line(aes(group=runNameNum, colour=runName), alpha=0.2)
	 }
	print(px)
	if(!is.na(pdfName)){
	  dev.off()
	}
	
	 return(px)
	}



loadData = function(paramName){
	 res = loadDataHist(paramName)
 	param = params[params$RunName==paramName,]
 	popSize = param$nAgents
# 	#popSize = 76
# 	
# 	folder = paste("results/", paramName,'/',sep='')
# 	res = data.frame()
# 	files = list.files(folder,"*.res")
# 	
# 	for(i in 1:length(files)){
# 		d = read.csv(paste(folder,files[i],sep=''),header=T,quote='')
# 		names(d) = c("stage","id","deaf","signs","sounds",'structure','age')
# 		d$prop.signs = d$signs/(d$signs+d$sounds)
# 	d$prop.signs[is.nan(d$prop.signs)] = 0
# 		d$runNum = i
# 		res = rbind(res,d)
# 	}
	
	ressum = ddply(res, .(runNum,stage), summarize, prop.signs = mean(prop.signs,na.rm=T), nDeaf = sum(deaf))
	ressum$runName = paramName
	ressum$runNameNum = paste(ressum$runName,ressum$runNum)
	
	ressum$prop.deaf = ressum$nDeaf / popSize
	
	ressum$prop.deaf = ressum$prop.deaf *100
	res$prop.signs = 100* res$prop.signs
	
	ressum$year = ressum$stage * timescale
	
	return(ressum)
}

loadDataHist = function(paramName){
    
    param = params[params$RunName==paramName,]
    popSize = param$nAgents
    #popSize = 76
    
    folder = paste("results/", paramName,'/',sep='')
    res = data.frame()
    files = list.files(folder,"*.res")
    
    for(i in 1:length(files)){
      d = read.csv(paste(folder,files[i],sep=''),header=T,quote='')
      names(d) = c("stage","id","deaf","signs","sounds",'structure','age')
      d$prop.signs = d$signs/(d$signs+d$sounds)
      d$prop.signs[is.nan(d$prop.signs)] = 0
      d$runNum = i
      res = rbind(res,d)
    }
    res$prop.signs = res$signs/(res$signs+res$sounds)
    
    return(res)
}

plotFluency = function(dxx,cuts = c(0.45,0.30,0.1) ,stagex = 100, measure = "prop.signs"){
  
  colx = c("#FF7F00", "#00B0FF")
  
  dx = dxx[dxx$stage==stagex,]
  nonfluent = 681/(2189-372)
  fluent = 449 / (2189-372)
  balanced = 78 / (2189-372)
  non = 562 / (2189-372)
  
  nonfluent.chican = 211/(720-156)
  fluent.chican = 100 / (720-156)
  balanced.chican = 21 / (720-156)
  non.chican = 215 / (2189-372)
  
  
  
  # balanced
  balanced.m = sum(dx[dx$deaf==0,measure] > cuts[1],na.rm=T)/nrow(dx)
  # fluent
  fluent.m = sum(dx[dx$deaf==0,measure] > cuts[2] & (dx[dx$deaf==0,measure] <= cuts[1]),na.rm=T) / nrow(dx)
  # non-fluent
  nonfluent.m = sum(dx[dx$deaf==0,measure] > cuts[3] & (dx[dx$deaf==0,measure] <= cuts[2]),na.rm=T)/nrow(dx)
  # non-signers
  non.m = sum(dx[dx$deaf==0,measure] <= cuts[3],na.rm=T)/nrow(dx)
  
  
  barplot(rbind(
    c(non,nonfluent,fluent,balanced)
   # ,c(non.chican, nonfluent.chican,fluent.chican,balanced.chican)
    ,c(non.m,nonfluent.m,fluent.m,balanced.m)
    ),beside=T, ylab='Proportion of population',  names.arg = c("Non\nSigner","Non\nFluent",'Fluent','Balanced'), col =colx,border=NA, space=c(0,0.5))
  legend(6,0.6,legend=c("Kata Kolok","Model"),col=colx,pch=15,cex=1)
  
}

##########


params = read.csv("Parameters/KK_Model_parameters.csv",stringsAsFactors=F)
for(i in 1:ncol(params)){
	params[is.na(params[,i]),i] = params[1,i]
}

params = rbind(params,params[1,])
params[nrow(params),c("RunName","nAgents")] = c("KK_100Community",100)
params = rbind(params,params[1,])
params[nrow(params),c("RunName","nAgents")] = c("KK_500Community",500)
params = rbind(params,params[1,])
params[nrow(params),c("RunName","nAgents")] = c("KK_800Community",800)

params$nAgents = as.numeric(params$nAgents)

kkDefault = loadData("KK_Default")

test3 = rbind(
	loadData("KK_SmallCommunity"),
	kkDefault,
	loadData("KK_LargeCommunity")
)



test4 = rbind(
  loadData("BulelengGeneralSituation"),
  kkDefault,
	loadData("KK_NoSocialStructure"),
  loadData("UrbanSituation")
)


test5 = rbind(
	loadData("KK_LowIncidence"),
	kkDefault
	,loadData("KK_HighIncidence")
)


test6 = rbind(
 	loadData("KK_HearingCarriersLow"),
 	kkDefault,
 	loadData("KK_HearingCarriersHigh")
 )
# plotMeanRun(test6)
# plotMeanHearingSigns(test6)

test7 = rbind(
  loadData("KK_CommVeryHigh"),
	#loadData("KK_CommHigh"),
	kkDefault,
	loadData("KK_CommLow")
)



plotMeanRun(test3, c("Small","KK","Large"), plotIndividualRuns=F,pdfName='MR_Size.pdf')
plotMeanHearingSigns(test3, c("Small","KK","Large"),plotIndividualRuns=F,'HS_Size.pdf')


plotMeanRun(test4, c("Region","KK","No Social Structure","Urban"), pdfName = 'MR_Social.pdf')
plotMeanHearingSigns(test4, c("Region","KK","No Social Structure","Urban"), pdfName = 'HS_Social.pdf')

plotMeanRun(test5, c("Low","KK","High"), pdfName = 'MR_DIncidence.pdf',widthx=3)
plotMeanHearingSigns(test5, c("Low","KK","High"), pdfName = 'HS_DIncidence.pdf',widthx=3)

plotMeanRun(test6, c("Low","KK","High"), pdfName = 'MR_DCarriers.pdf',widthx=3)
plotMeanHearingSigns(test6, c("Low","KK","High"), pdfName = 'HS_DCarriers.pdf',widthx=3)

plotMeanRun(test7, c("Important","KK","Not important"), pdfName = 'MR_Comm.pdf',ylimx=c(0.013,0.025))
plotMeanHearingSigns(test7, c("Important","KK","Not important"), pdfName = 'HS_Comm.pdf')



kdh = loadDataHist("KK_Default")
pdf("analysis/graphs/Fluency.pdf", width=4.5,height=5)
plotFluency(kdh,stagex=600,cuts = c(0.45,0.25,0.1))
dev.off()



####
d = read.csv("results/KK_Default/KK_Default236.res")

d = d[d$stage>500,]

deaf.m = median(d[d$deaf==1,]$fluency,na.rm=T)
deaf.sd = sd(d[d$deaf==1,]$ fluency,na.rm=T)

d$fluency2 = (d$fluency - deaf.m)/deaf.sd
d$fluency2 = -d$fluency2 
hist(d[d$deaf==0,]$fluency2)

hist(d[d$deaf==0 & d$stage==600,]$fluency2, breaks=c(2,1,0,1,2))

plotFluency(d[d$deaf==0,],stagex=600,cuts =c(1,0,-1), measure='fluency2')
