# coding: utf8
from __future__ import unicode_literals
from getWCSCapabilities import getWCSCapabilities
resolution="0025"  # resolution du modèle Arome ("001" ou "0025")
ageMaxi=8.0  # age maximun (heures) des run qu'on va traiter
covId=getWCSCapabilities(resolution)  # lance requête getCpabilities au WCS de MF
jeunesCovId=list(filter(lambda x:x.ageRun() <=ageMaxi,covId)) # on ne traite que les CoverageId qui ont moins de 8 heures d'age
print(len(covId),len(jeunesCovId))
for covId in jeunesCovId :
    covId.describeCoverage()
    #print(covId.timeDatePrevi)
    #print(covId.descr,covId.timeDatePreviFutures)
    covId.affiche()