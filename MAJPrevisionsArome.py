#  Mise a jour de la base de previsions Arome.sqlite par interrogation du WCS de MF
from getWCSCapabilities import getWCSCapabilities
from allPrevisionsForCov import allPrevisionsForCov
import datetime
import os
import random
import traceback
from traiteAromePrevi import traiteAromePrevi
deb=datetime.datetime.utcnow()
print (deb)
lat=50.7  # les coordonnees geographiques de Lille
lng=3.06
resolution="0025"  # résolution du modèle Arome ("001" ou "0025")
modele="HIGHRES-AROME"
domaine="FRANCE"
ageMaxi=8.0  # age maximun (heures) des run qu'on va traiter
covId=getWCSCapabilities(modele,resolution,domaine)  # lance requête getCapabilities au WCS de MF
print(covId["lesID"][0])
jeunesCovId=  list(filter(lambda x:x["obj"].ageRun() <=ageMaxi,covId["lesID"])) # on ne traite que les CoverageId qui ont moins de 8 heures d'age
aTraiterCovId=list(filter(lambda x:x["obj"].aIgnorer()==False,jeunesCovId))
random.shuffle(aTraiterCovId)  # on mélange les CoverageId pour ne pas toujours les traiter dans le même ordre
nbMaxIter=3 # On ne traite ue les premiers CoverageId
aTraiterCovId=aTraiterCovId[0:nbMaxIter]
print(len(covId),len(jeunesCovId),len(aTraiterCovId))
result=[]
nbID=0
with open("res_tempo.txt","w") as f:
    pass
for Id in aTraiterCovId :
    print ("nbID:",nbID)
    print (Id["obj"].coverageId)
    print ("age du Run",str(Id["obj"].ageRun()))
    try:
        result=result+allPrevisionsForCov(Id["obj"],lng,lat,all_previ=False,grib=True)  # on utilise le format tiff ou grib
    except Exception as ex :
        print (ex ,"Erreur dans allPrevisionForCov, nbID= ",nbID)
        traceback.print_exc()
        exit()
    nbID=nbID+1 # On passe au CoverageId suivant
fin=datetime.datetime.utcnow()
print (len(covId),len(jeunesCovId),len(aTraiterCovId))
print (len(result),deb,fin)
fic = open("logArome.txt","a")
fic.write(len(covId),len(jeunesCovId),len(aTraiterCovId),len(result),deb,fin)
fic.close()