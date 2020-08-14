# Importations

import numpy as np
import math
import matplotlib.pyplot as plt
import random
import numpy
import copy
import matplotlib.animation as animation
import time
import os
import matplotlib.colors as cm

# Variables Globales :

temperaturebase = 0
energiebase = 0
massevol = 10000
tempsfin = 100
energiemax = 1000
pas = 1000
energieFeu = 250
xmax = 1000
ymax = 1000
rmax = 1
energierelax = 50



# Programmes

class Arbre :
    """Classe définissant un arbre caractérisé par :
    - ses positions x et y
    - son rayon
    - sa hauteur
    - ..."""

    def __init__(self):
        self.energiefeu = energiebase
        self.coordx = 5
        self.coordy = 5
        self.rayon = 1
        self.etat = 'non brulé'
        self.tempsfeu = 1
        self.volume = 10*math.pi*(self.rayon)**2
        self.masse = self.volume*massevol
        self.masseinit = self.volume*massevol
        self.distancecentre = math.sqrt(self.coordx**2+self.coordy**2) #distance au centre (0,0)
        self.foret_anchor = (int(self.coordx),int(self.coordy)) #ancrage de l'arbre dans la foret
        self.temperature = 0
    
    def set_location(self,x,y) :
        self.coordx = x
        self.coordy = y
    
    def set_radius(self,r) :
        self.rayon = r
        
    def bruleTriangle(self) :
        '''brule un arbre'''
        assert self.tempsfeu >= 0
        assert self.etat == 'en feu'
        if self.tempsfeu <= tempsdureefeu/2 :
            self.energie +=  (2*energiemax*self.tempsfeu/tempsfin)
            self.tempsfeu += 1
        elif self.tempsfeu > tempsfin/2 and self.tempsfeu <= tempsfin :
            self.energie += -(2*energiemax*self.tempsfeu/tempsfin)+2*energiemax
            self.tempsfeu += 1
        elif self.tempsfeu > tempsfin :
            self.tempsfeu += 1
            
    def arbreRelax(self) :
        if (self.etat == 'non brulé' or self.etat == 'brulé') and self.energiefeu >= 1 :
            self.energie -= 600
            
    def prend_feu(self) :
        if self.etat == 'non brulé':
            self.etat = 'en feu'
            
    def energie(self) :
        if self.tempsfeu <= tempsfin/2 :
            return (2*energiemax*self.tempsfeu/tempsfin)
        elif self.tempsfeu > tempsfin/2 and self.tempsfeu <= tempsfin :
            return -(2*energiemax*self.tempsfeu/tempsfin)+2*energiemax
        elif self.tempsfeu > tempsfin :
            return 0
            
    def feu(self,dist,rcalc) :
        return self.energie() - (dist/rcalc)*self.energie()
            

            

        
 
class Foret :
        
    '''Type foret 2 :
    type enregistrement :
    - (arbres) liste de liste contenant pour chaque arbre [coordx,coordy,rayon, temps en feu]
    - (température) matrice de taille n*n de la chaleur 
    - (énergie) matrice de taille n*n de l'énergie (qui n'est pas linéaire en fonction de la chaleur)'''
    
    
    
    def __init__(self) :
        self.arbres = []
        self.xmax = xmax
        self.xmin = 0
        self.ymax = ymax
        self.ymin = 0
        self.rmax = rmax
        self.rmin = rmax/2
        self.taille = 0
        self.energiemap = [[0 for i in range(pas)] for j in range(pas)]
    
    def ajouter_arbre(self,x,y,r) :
        a = Arbre()
        a.set_location(x,y)
        a.set_radius(r)
        b = True
        i = 0
        while (b == True) and (i != self.taille) :
            aa = self.arbres[i]
            if math.sqrt((x-aa.coordx)**2+(y-aa.coordy)**2) <= aa.rayon + r :
                b = False
            i +=1
        if b == True :
            self.arbres.append(a)
            self.taille += 1
        
    def remplir_foret(self,nombre) :
        nombrecompteur = nombre
        while nombrecompteur != 0 :
            p = random.random()
            q = random.random()
            s = random.random()
            self.ajouter_arbre((self.xmax-self.xmin)*p+self.xmin,(self.ymax-self.ymin)*q+self.ymin,(self.rmax-self.rmin)*s+(self.rmin))
            nombrecompteur = nombre - self.taille
            print((nombre-nombrecompteur))
            
        
    def allumerlefeu(self) :
        p = random.randint(0,self.taille-1)
        self.arbres[p].etat = 'en feu'
        print(p)
        
    def quienfeu(self) :
        for i in range(self.taille) :
            if self.arbres[i].etat == 'en feu' :
                print(i)
            
            
        
            
class Ellipse :
    
    def __init__(self) :
        self.fmax = 250
        self.hmax = 150
        self.gxmax = 25
        self.gymax = 25
        self.vent = (10,10)
    
    def e(self,temps) :
        calc = math.sqrt(abs(self.f(temps)**2-self.h(temps)**2))/self.f(temps)
        if calc == 0 :
            return 0.001
        else :
            return calc
        
    def f(self,temps) : #valide la plupart du temps
        calc = 0
        if temps <= tempsfin/2 :
            calc = (2*self.fmax*temps/tempsfin)
        elif temps > tempsfin/2 and temps <= tempsfin :
            calc =  -(2*self.fmax*temps/(tempsfin+1))+2*self.fmax
        elif temps > tempsfin :
            calc = 0.001
        if calc == 0 :
            return 0.001
        else :
            return calc
    
    def h(self,temps) :
        if temps <= tempsfin/2 :
            return (2*self.hmax*temps/tempsfin)
        elif temps > tempsfin/2 and temps <= tempsfin :
            return -(2*self.hmax*temps/tempsfin)+2*self.hmax
        elif temps > tempsfin :
            return 0
    
    def gx(self,temps) :
        if temps <= tempsfin/2 :
            return (2*self.gxmax*temps/tempsfin)
        elif temps > tempsfin/2 and temps <= tempsfin :
            return -(2*self.gxmax*temps/tempsfin)+2*self.gxmax
        elif temps > tempsfin :
            return 0
            
    def gy(self,temps) :
        if temps <= tempsfin/2 :
            return (2*self.gymax*temps/tempsfin)
        elif temps > tempsfin/2 and temps <= tempsfin :
            return -(2*self.gymax*temps/tempsfin)+2*self.gymax
        elif temps > tempsfin :
            return 0
            
    
        
    def r(self,costheta,temps) :
        if abs(costheta) > 1 :
            costheta = 1
        elif costheta == 0 :
            costheta = 0.0001
        return self.h(temps)/math.sqrt(1-abs((self.e(temps))**2*(costheta)**2))
        
        
        
    
def modeleEllipse(arbre,foret,ellipse,temps) :
    n = pas
    x,y = arbre.coordx,arbre.coordy
    x += e.gx(temps)
    y += e.gy(temps)
    (xv,yv) = ellipse.vent
    m = foret.energiemap
    def cosinus(x1,x2,y1,y2) :
        return (x1*x2+y1*y2)/(math.sqrt(x1**2+y1**2)*math.sqrt(x2**2+y2**2))
    for i in range(n) :
        for j in range(n) :
            d = math.sqrt(i**2+j**2)
            if d > 0 and (i != x or j != y) :
                dprime = math.sqrt((i-x)**2+(j-y)**2)
                r = ellipse.r(cosinus(xv,i-x,yv,j-y),arbre.tempsfeu)
                if dprime < r :
                    foret.energiemap[i][j] += arbre.feu(dprime,r)
    for k in range(foret.taille) :
        if foret.arbres[k].distancecentre > 0 :
            xa,ya = foret.arbres[k].coordx,foret.arbres[k].coordy
            dprime = math.sqrt((xa-x)**2+(ya-y)**2)
            r = ellipse.r(cosinus(xv,xa-x,yv,xa-y),arbre.tempsfeu)
            if dprime < r :
                foret.arbres[k].temperature += arbre.feu(dprime,r)
        
    
def modeleEllipseForet(foret,ellipse,temps) :
    n = pas
    for k in range(foret.taille) :
        if foret.arbres[k].etat == 'en feu' :
            modeleEllipse(foret.arbres[k],foret,ellipse,temps)
    print('fin étape propagation')
    for k in range(foret.taille) :
        if foret.arbres[k].temperature > energieFeu :
            foret.arbres[k].prend_feu()
        foret.arbres[k].arbreRelax()
    print('fin étape mise en feu')
    for i in range(n) :
        for j in range(n) :
            foret.energiemap[i][j] -= energierelax
            if foret.energiemap[i][j] < 0:
                foret.energiemap[i][j] = 0
    for k in range(foret.taille) :
        foret.arbres[k].temperature -= energierelax
        if foret.arbres[k].etat == 'en feu' :
            foret.arbres[k].tempsfeu += 1
    print('fin étape relaxation')
    

def enregistrer_animation(t,foret,ellipse) :
    os.chdir("C:/Users/Adrien/Desktop/TIPE 2/images")
    for k in t :
        modeleEllipseForet(foret,ellipse,k)
        map = foret.energiemap
        plt.matshow(map)
        plt.imsave(fname='image'+str(k)+'.png',arr=map)
        plt.clf()



def affichagecouleur(foret) :
    map = foret.energiemap
    plt.matshow(map)
    plt.show()
    
    
 
def etude_arbre_seul() :
    f = Foret()
    xa,ya = (f.xmax/2),(f.ymax/2)
    f.ajouter_arbre(xa,ya,rmax)
    f.arbres[0].etat = 'en feu'
    return f
    
def test_propa_4arbres() :
    f = Foret()
    xa,ya = (f.xmax/6),(f.ymax/6)
    f.ajouter_arbre(3*xa,3*ya,rmax)
    f.ajouter_arbre(3*xa,4*ya,rmax)
    f.ajouter_arbre(4*xa,3*ya,rmax)
    f.ajouter_arbre(4*xa,4*ya,rmax)
    f.arbres[0].etat = 'en feu'
    return f
    
    
    
def test_foret_random(n) :
    f= Foret()
    for k in range(n) :
        x = random.randrange(0,f.xmax)
        y = random.randrange(0,f.ymax)
        f.ajouter_arbre(x,y,rmax)
    f.arbres[0].etat = 'en feu'
    return f
    
   
        
def signalaleat(temps,val1,val2) :
    tf = [1]
    for i in range(1,len(t)) :
        p = random.random()
        n = random.randrange(1, 10)
        amp = int((val2 - val1)/3)
        if p >0.5 :
            res = int(tf[i-1]+(amp/n))
            if res > val2 :
                tf.append(tf[i-1])
            else :
                tf.append(res)
        else :
            res = int(tf[i-1]-(amp/n))
            if res < val1 :
                tf.append(tf[i-1])
            else :
                tf.append(res)
    return tf 
    

        
    
def modeleEllipseForetventmodifie(foret,ellipse,temps) : #à modifier
    
    def ventmodifie() :
        val1 = -25
        val2 = 25
        temps2 = 10000
        return (signalaleat(temps2,val1,val2),signalaleat(temps2,val1,val2))
    
    def modeleEllipseventmodifie(arbre,foret,ellipse,temps) :
        n = pas
        x,y = arbre.coordx,arbre.coordy
        x += e.gx(temps)
        y += e.gy(temps)
        (xv,yv) = ventmodifie()
        m = foret.energiemap
        def cosinus(x1,x2,y1,y2) :
            return (x1*x2+y1*y2)/(math.sqrt(x1**2+y1**2)*math.sqrt(x2**2+y2**2))
        for i in range(n) :
            for j in range(n) :
                d = math.sqrt(i**2+j**2)
                if d > 0 and (i != x or j != y) :
                    dprime = math.sqrt((i-x)**2+(j-y)**2)
                    r = ellipse.r(cosinus(xv[temps],i-x,yv[temps],j-y),temps) #buggé ici
                    if dprime < r :
                        foret.energiemap[i][j] += ellipse.feu(dprime,r,temps)
        for k in range(foret.taille) :
            if foret.arbres[k].distancecentre > 0 :
                xa,ya = foret.arbres[k].coordx,foret.arbres[k].coordy
                dprime = math.sqrt((xa-x)**2+(ya-y)**2)
                r = ellipse.r(cosinus(xv[temps],xa-x,yv[temps],xa-y),temps)
                if dprime < r :
                    foret.arbres[k].temperature += ellipse.feu(dprime,r,temps)
    
    n = pas
    for k in range(foret.taille) :
        if foret.arbres[k].etat == 'en feu' :
            modeleEllipseventmodifie(foret.arbres[k],foret,ellipse,temps)
    print('fin étape propagation')
    for k in range(foret.taille) :
        if foret.arbres[k].temperature > energieFeu :
            foret.arbres[k].prend_feu()
        foret.arbres[k].arbreRelax()
    print('fin étape mise en feu')
    for i in range(n) :
        for j in range(n) :
            foret.energiemap[i][j] -= energierelax
            if foret.energiemap[i][j] < 0:
                foret.energiemap[i][j] = 0
    for k in range(foret.taille) :
        foret.arbres[k].temperature -= energierelax
    print('fin étape relaxation')
    

def enregistrer_animationventmodifie(t,foret,ellipse) :
    os.chdir("C:/Users/Adrien/Desktop/TIPE 2/images")
    for k in t :
        modeleEllipseForetventmodifie(foret,ellipse,k)
        map = foret.energiemap
        plt.matshow(map)
        plt.imsave(fname='image'+str(k)+'.png',arr=map)
        plt.clf()
    
    
    
    

        
    