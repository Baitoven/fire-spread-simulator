import math
import matplotlib.pyplot as plt
import numpy as np

alpha = 50 #à modifier
tempsdemivie = 50
puissancefeumax = 1000

def tracer() :
    T = np.linspace(0,100,1000)
    Y = [CI_r0(T[i]) for i in range(len(T))]
    plt.plot(T,Y)
    plt.show()

def solve_Cranck_Nicolson_v1(dr,dt,tmax,rmax) :
    
    #Conditions initiales
    def CI_r0(t) :
        return puissancefeumax*math.exp(-((t-tempsdemivie)/tempsdemivie)**2)
    
    #initialisation    
    lent = int(tmax/dt)
    lenr = int(rmax/dr)
    T = [[0 for _ in range(lenr)] for _ in range(lent)]
    for i in range(lent) : 
        T[i][0] = CI_r0(i*dr)
        
        #résolution
    for t in range(0,lent-1) :
        for r in range(1,lenr -1) :
            T[t+1][r] = alpha*dt*((r/(dr**2))*(T[t][r+1] - 2*T[t][r] + T[t][r-1]) + (1/dr)*(T[t][r] - T[t][r-1])) + T[t][r]
            
    return T
    
def tracer_solution(t) :
    dr = 0.1
    dt = 0.1
    tmax =50
    rmax =10
    T = solve_Cranck_Nicolson_v2(dr,dt,tmax,rmax)
    for k in t :
        X = [(r*dr) for r in range(len(T[k]))]
        Y = [T[k][r] for r in range(len(T[k]))]
        plt.plot(X,Y)
    plt.show()
    
def solve_Cranck_Nicolson_v2(dr,dt,tmax,rmax) : # ne fonctionne pas ?!?
    
    #Conditions initiales
    def CI_r0(t) :
        return puissancefeumax*math.exp(-((t-tempsdemivie)/tempsdemivie)**2)
    
    #initialisation    
    lent = int(tmax/dt)
    lenr = int(rmax/dr)
    T = [[0 for _ in range(lenr)] for _ in range(lent)]
    for i in range(lent) : 
        T[i][0] = CI_r0(i*dr)
        #T[i][1] = CI_r0(i*dr)
        
        #résolution
    for t in range(1,lent-1) :
        for r in range(1,lenr -1) :
            T[t][r+1] = (1/(alpha*((1/(dr**2))+(1/(2*r*dr)))))*((1/dt)*(T[t][r]-T[t-1][r]) + (alpha/(dr**2))*(2*T[t][r] - T[t][r-1]) + (alpha/(2*r*dr))*T[t][r-1])
            
    return T
        
    
    