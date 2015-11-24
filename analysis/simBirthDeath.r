n = 10
births.deaths.per.cycle = 3

sim = function(n,births.deaths.per.cycle){
	d = rep(0,n)
	count =0
	while(d[1]>=0){
		for(i in births.deaths.per.cycle){
			die = sample(1:n,1)
			d[die] = -d[die]
			count = count +1
			birth = sample(1:n,1)
			d[birth] = d[birth]+1
		}
	}
	return(c(count,d[1]))
}

res = replicate(1000,sim(10,1))

par(mfrow=c(1,2))
hist(res[1,],main='count')
hist(-res[2,],main='children')

plot(res[1,],-res[2,])

res = data.frame()
for(n in seq(10,2000,length.out=8)){
	for(births.deaths.per.cycle in c(1,2,3,4,5)){
		s = replicate(100,sim(n,births.deaths.per.cycle))
		res = rbind(res,cbind(t(s),rep(n,ncol(s)),rep(births.deaths.per.cycle,ncol(s))))
	}
}

names(res) = c("survive",'children','n','bd')
res$children = - res$children

par(mfrow=c(3,4))
for(nx in sort(unique(res$n))){
	plotmeans(res[res$n==nx,]$children~res[res$n==nx,]$bd, main= nx)
	}

m.children = lm(bd~ n * children,data=res)

predict(m.children, data.frame(n=2189, children=3))
predict(m.children, data.frame(n=2189, children=4))

