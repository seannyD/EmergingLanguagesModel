setwd("~/Documents/MPI/EmergingLanguages/SignSpeechConnieBill/Model/analysis/")

d = read.csv("../results/text.tab")

names(d) = c("stage","id","deaf","signs","sounds")

par(mfrow=c(2,2))

plot(tapply(d$deaf,d$stage,sum),type='l',main="Number of Deaf People")


signs_in_pop = tapply(d$signs,d$stage,mean)
sounds_in_pop = tapply(d$sounds,d$stage,mean)

plot(signs_in_pop,col=1,type='l', main='Signs used in pop', ylim=range(c(sounds_in_pop,signs_in_pop)))
lines(sounds_in_pop,col=2)
legend(1,max(c(signs_in_pop,sounds_in_pop)),legend=c("sign","sound"),col=1:2, lty=1)


d$prop.signs = d$signs/(d$signs+d$sounds)
d$prop.signs[is.nan(d$prop.signs)] = 0
balance = tapply(d$prop.signs,d$stage,mean,na.rm=T)

balance.hearing = tapply(d$prop.signs[d$deaf==0],d$stage[d$deaf==0],mean,na.rm=T)
plot(balance.hearing,type='l', main='', ylab='Proportion of signs')