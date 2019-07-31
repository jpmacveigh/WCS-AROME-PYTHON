# coding: utf8
from __future__ import unicode_literals
from getWCSCapabilities import getWCSCapabilities
from getWCSCapabilities import allFuturesPrevisionsForId
import datetime
import sys
deb=datetime.datetime.now()
resolution="0025"  # resolution du modèle Arome ("001" ou "0025")
ageMaxi=8.0  # age maximun (heures) des run qu'on va traiter
covId=getWCSCapabilities(resolution)  # lance requête getCpabilities au WCS de MF
jeunesCovId=  list(filter(lambda x:x.ageRun() <=ageMaxi,covId)) # on ne traite que les CoverageId qui ont moins de 8 heures d'age
aTraiterCovId=list(filter(lambda x:x.aIgnorer()==False,jeunesCovId))
print(len(covId),len(jeunesCovId),len(aTraiterCovId))
result=[]
for Id in aTraiterCovId :
    print Id.coverageId
    result=result+allFuturesPrevisionsForId(Id,3.06,50.6)
fin=datetime.datetime.now()
print (len(result),deb,fin)
#fic = open("logArome.txt","a")
#fic.write(len(covId),len(jeunesCovId),len(aTraiterCovId),len(result),deb,fin)
#fic.close()
fic = open("previArome.txt","w")
for previ in result:
    fic.writelines(str(previ)+"\n")
fic.close()
