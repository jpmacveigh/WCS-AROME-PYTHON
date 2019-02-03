#coding: utf8
import numpy as np
import math
from orthod import orthod
class Espace2D:
    def __init__(self, axeLongi,axeLati,valeurs):
        self.axeLongi=axeLongi
        self.axeLati=axeLati
        self.valeurs=valeurs
        if (self.axeLati.nb,self.axeLongi.nb) != valeurs.shape :
            raise Exception ("Espace2D : valeurs mauvaise shape")
    def valeurSurGrille (self,nLongi,nLati):  #  retour la en un point de la grille
        return self.valeurs[nLati,nLongi]
    def valeur (self,longi,lati):  # valeur en une position par interpllation sur les 4 points entourant la position
        nlongimin=self.axeLongi.interval(longi)[0]  # bord Est encadrant
        nlatimin = self.axeLati.interval(lati)[0]   # bord Nord encadrant (car les latitudes sont décroissantes sur axeLati)
        tot=0
        sumcoeff=0
        for longit in range(2):    # itératon sur les quatre points encadrant
            for latit in range(2):
                lo=nlongimin+longit
                la=nlatimin+latit
                dist=orthod(self.axeLongi.valtick[lo],self.axeLati.valtick[la],longi,lati)
                #print dist
                if (dist==0): return self.valeurSurGrille(lo,la)
                incr=self.valeurSurGrille(lo,la)   #  pondération des terms par l'inverse de la distance au point
                #print incr
                incr=incr/dist
                #print incr
                tot=tot+incr
                sumcoeff=sumcoeff+(1/dist)
        return (tot/sumcoeff)  #  on retourne la moyenne pondérée des valeurs aux quatre points entourant