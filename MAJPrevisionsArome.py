# coding: utf8
#  Mise à jour de la base de previsions Arome.sqlite par interrogation du WCS de MF
#from __future__ import unicode_literals
from getWCSCapabilities import getWCSCapabilities
from getWCSCapabilities import allFuturesPrevisionsForId
import datetime
import os
from traiteAromePrevi import traiteAromePrevi
deb=datetime.datetime.utcnow()
print (deb)
lat=50.06  # les coordonnées géographiques de Lille
lng=3.06
resolution="0025"  # résolution du modèle Arome ("001" ou "0025")
ageMaxi=8.0  # age maximun (heures) des run qu'on va traiter
covId=getWCSCapabilities(resolution)  # lance requête getCpabilities au WCS de MF
jeunesCovId=  list(filter(lambda x:x.ageRun() <=ageMaxi,covId)) # on ne traite que les CoverageId qui ont moins de 8 heures d'age
aTraiterCovId=list(filter(lambda x:x.aIgnorer()==False,jeunesCovId))
nbMaxIter=100
aTraiterCovId=aTraiterCovId[0:nbMaxIter]
print(len(covId),len(jeunesCovId),len(aTraiterCovId))
result=[]
nbID=0
for Id in aTraiterCovId :
    if nbID <= 200002 :
        print ("nbID:",nbID)
        print (Id.coverageId)
        print ("age du Run",str(Id.ageRun()))
        result=result+allFuturesPrevisionsForId(Id,lng,lat)
        nbID=nbID+1
    else : break
fin=datetime.datetime.utcnow()
print (len(covId),len(jeunesCovId),len(aTraiterCovId))
print (len(result),deb,fin)
#fic = open("logArome.txt","a")
#fic.write(len(covId),len(jeunesCovId),len(aTraiterCovId),len(result),deb,fin)
#fic.close()
repcourant=os.getcwd()+"/"
fic = open(repcourant+"previArome.txt","w") # Ecriture des résultats dans fichier temporaire
for previ in result:
    fic.writelines(str(previ)+"\n")
fic.close()
traiteAromePrevi() # Ecriture du fichier previArome.txt dans base Arome.sqlite