import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy import *
from pylab import *
import numpy as np

Pr = 0.7
ro = 1.225
mu = 0.00003

def fNusselt(Re) :
    if Re > 0.4 and Re <= 4 :
        return 0.989*(Re**0.33)*(Pr**(1/3))
    elif Re > 4 and Re <= 40 :
        return 0.911*(Re**0.385)*(Pr**(1/3))
    elif Re > 40 and Re <= 4000 :
        return 0.613*(Re**0.466)*(Pr**(1/3))
    elif Re > 4000 and Re <= 40000 :
        return 0.193*(Re**0.618)*(Pr**(1/3))
    elif Re > 40000 :
        return 0.027*(Re**0.805)*(Pr**(1/3))
        
def Nusselt(v,d) :
    Re = (ro*v*d)/mu
    return fNusselt(Re)
    
        
def tracer3D_Nusselt(Dmin,Dmax,Vmin,Vmax,n) :
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    D = linspace(Dmin,Dmax,n)
    V = linspace(Vmin,Vmax,n)
    Dprime, Vprime = np.meshgrid(D, V)
    N = [[0.0 for _ in range(0,len(D))] for _ in range(0,len(V))]
    for i in range (0,len(D)) :
        for j in range (0,len(V)):
             N[i][j] = Nusselt(V[j],D[i])
    surf = ax.plot_surface(np.array(Dprime), np.array(Vprime), np.array(N),cmap=cm.jet, antialiased=False)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()