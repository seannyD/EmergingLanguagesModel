
library(lattice)
setwd("~/Documents/MPI/EmergingLanguages/SignSpeechConnieBill/Model/")


folder = "results/KK_SmallCommunity/"
res = data.frame()
files = list.files(folder,"*.res")

for(i in 1:length(files)){
	d = read.csv(paste(folder,files[i],sep=''),header=F,quote='')
	names(d) = c("stage","id","deaf","signs","sounds")
	d$prop.signs = d$signs/(d$signs+d$sounds)
d$prop.signs[is.nan(d$prop.signs)] = 0
	d$runNum = i
	res = rbind(res,d)
}


deaf_in_pop = sapply(unique(res$runNum), function(X){
	tapply(res[res$runNum==X,]$deaf,res[res$runNum==X,]$stage,sum)}
)
plot(NA,xlim=c(0,max(res$stage)), ylim=c(0,2189))
apply(deaf_in_pop,2,function(X){lines(as.numeric(rownames(deaf_in_pop)), X)})

sounds_in_pop = tapply(d$sounds,d$stage,mean)

plot(signs_in_pop,col=1,type='l', main='Signs used in pop', ylim=range(c(sounds_in_pop,signs_in_pop)))
lines(sounds_in_pop,col=2)
legend(1,max(c(signs_in_pop,sounds_in_pop)),legend=c("sign","sound"),col=1:2, lty=1)

xyplot(prop.signs~stage, groups=runNum,data = res)