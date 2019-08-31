# coding: utf8
#  Mise à jour de la base de previsions Arome.sqlite par interrogation du WCS de MF
from __future__ import unicode_literals
from getWCSCapabilities import getWCSCapabilities
from getWCSCapabilities import allFuturesPrevisionsForId
import datetime
import sys
from traiteAromePrevi import traiteAromePrevi
deb=datetime.datetime.now()
lat=50.06  # les coordonnées géographiques de Lille
lng=3.06
resolution="0025"  # résolution du modèle Arome ("001" ou "0025")
ageMaxi=8.0  # age maximun (heures) des run qu'on va traiter
covId=getWCSCapabilities(resolution)  # lance requête getCpabilities au WCS de MF
jeunesCovId=  list(filter(lambda x:x.ageRun() <=ageMaxi,covId)) # on ne traite que les CoverageId qui ont moins de 8 heures d'age
aTraiterCovId=list(filter(lambda x:x.aIgnorer()==False,jeunesCovId))
print(len(covId),len(jeunesCovId),len(aTraiterCovId))
result=[]
for Id in aTraiterCovId :
    print Id.coverageId
    result=result+allFuturesPrevisionsForId(Id,lng,lat)
fin=datetime.datetime.now()
print (len(covId),len(jeunesCovId),len(aTraiterCovId))
print (len(result),deb,fin)
#fic = open("logArome.txt","a")
#fic.write(len(covId),len(jeunesCovId),len(aTraiterCovId),len(result),deb,fin)
#fic.close()
fic = open("previArome.txt","w") # Ecriture des résultat dans fichier temporaire
for previ in result:
    fic.writelines(str(previ)+"\n")
fic.close()
traiteAromePrevi() # Ecriture du fichier previArome.txt dans base Arome.sqlite