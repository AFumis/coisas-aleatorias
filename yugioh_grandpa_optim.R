# remove the # from the lines with it to make a plot of E[T} by K
# library(ggplot2)

X <- 3
Y <- 1
alpha <- 1/256
pp <- 1/8

e_t <- \(X, Y, alpha, pp, kk){
  (X + Y*(kk + pp*(1/alpha - (1-alpha)^kk*(1/alpha+kk) - kk))) /
    (pp - pp*(1-alpha)^kk)
}

sim_e_t <- \(n_sim, X, Y, alpha, pp, kk){
  runs <- rep(NA, n_sim)
  
  for(i in 1:n_sim){
    event <- F
    tot_time <- 0
    
    while(!event){
      tot_time <- tot_time + X
      possible <- rbinom(1, 1, pp)
      j <- 1
      
      while(!event & j<=kk){
        tot_time <- tot_time + Y
        
        if(possible){
          happened <- rbinom(1, 1, alpha)
          if(happened) event <- T
        }
        
        j <- j+1
      }
    }
    
    runs[i] <- tot_time
  }
  
  mean(runs)
}

kk <- 20
e_t(X, Y, alpha, pp, kk)
sim_e_t(1000, X, Y, alpha, pp, kk)

# ggplot() +
#   stat_function(fun = \(k) e_t(X, Y, alpha, pp, k)) +
#   xlim(15, 50) # change limits for a better view of the curve

optim_res <- optim(par = 10,
                   fn = \(k) e_t(X, Y, alpha, pp, k),
                   method = "BFGS")
k1 <- floor(optim_res$par)
et_k1 <- e_t(X, Y, alpha, pp, k1)
k2 <- k1 + 1
et_k2 <- e_t(X, Y, alpha, pp, k2)

print(paste("Best K is",
            ifelse(et_k1 < et_k2, k1, k2),
            "with E[T] =",
            min(et_k1, et_k2)))











