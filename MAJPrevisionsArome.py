#  Mise à jour de la base de previsions Arome.sqlite par interrogation du WCS de MF
from getWCSCapabilities import getWCSCapabilities
from allPrevisionsForCov import allPrevisionsForCov
import datetime
import os
from traiteAromePrevi import traiteAromePrevi
deb=datetime.datetime.utcnow()
print (deb)
lat=50.06  # les coordonnées géographiques de Lille
lng=3.06
resolution="0025"  # résolution du modèle Arome ("001" ou "0025")
modele="HIGHRES-AROME"
domaine="FRANCE"
ageMaxi=8.0  # age maximun (heures) des run qu'on va traiter
covId=getWCSCapabilities(modele,resolution,domaine)  # lance requête getCapabilities au WCS de MF
print(covId["lesID"][0])
jeunesCovId=  list(filter(lambda x:x["obj"].ageRun() <=ageMaxi,covId["lesID"])) # on ne traite que les CoverageId qui ont moins de 8 heures d'age
aTraiterCovId=list(filter(lambda x:x["obj"].aIgnorer()==False,jeunesCovId))
nbMaxIter=100
aTraiterCovId=aTraiterCovId[0:nbMaxIter]
print(len(covId),len(jeunesCovId),len(aTraiterCovId))
result=[]
nbID=0
for Id in aTraiterCovId :
    if nbID <= 0 :
        print ("nbID:",nbID)
        print (Id["obj"].coverageId)
        print ("age du Run",str(Id["obj"].ageRun()))
        result=result+allPrevisionsForCov(Id["obj"],lng,lat,all_previ=False,grib=True)  # on utilise le format tiff ou grib
        nbID=nbID+1
    else : break
fin=datetime.datetime.utcnow()
print (len(covId),len(jeunesCovId),len(aTraiterCovId))
print (len(result),deb,fin)
#fic = open("logArome.txt","a")
#fic.write(len(covId),len(jeunesCovId),len(aTraiterCovId),len(result),deb,fin)
#fic.close()
if len(result) != 0 :
    repcourant=os.getcwd()+"/"
    fic = open(repcourant+"previArome.txt","w") # Ecriture des résultats dans fichier temporaire
    for previ in result:
        fic.writelines(str(previ)+"\n")
    fic.close()
    traiteAromePrevi() # Ecriture du fichier previArome.txt dans base Arome.sqlite