#  Mise à jour de la base de previsions Arome.sqlite par interrogation du WCS de MF
#  en utilisant les function Lambda développées pour accéder au WCS
from getWCSCapabilities import getWCSCapabilities
import datetime
import os
import requests
import json
deb=datetime.datetime.utcnow()
lati=50.06  # les coordonnées géographiques de Lille
longi=3.06
resolution="0025"  # résolution du modèle Arome ("001" ou "0025")
modele="HIGHRES-AROME"
domaine="FRANCE"
ageMaxi=8.0  # age maximun (heures) des run qu'on va traiter
covId=getWCSCapabilities(modele,resolution,domaine)  # lance requête getCapabilities au WCS de MF
jeunesCovId=  list(filter(lambda x:x["obj"].ageRun() <=ageMaxi,covId["lesID"])) # On ne traite que les CoverageId qui ont moins de 8 heures d'age
aTraiterCovId=list(filter(lambda x:x["obj"].aIgnorer()==False,jeunesCovId))  # On ignore certains CoverageId
nbMaxIter=1000
aTraiterCovId=aTraiterCovId[0:nbMaxIter]
print("Nombre d'Id:",covId["nb_ID"],"Jeunes Id:",len(jeunesCovId),"A traiter:",len(aTraiterCovId))
nbID=0
for Id in aTraiterCovId : # Boucle sur les CoverageId à traiter
    print ("nbID:",nbID," Id:",Id["obj"].coverageId,"age du Run",str(Id["obj"].ageRun()))
    #pathGetDescribeCoverage="https://vs22yndw4thomnysosle3dxxry0aygnh.lambda-url.eu-west-1.on.aws/?modele=HIGHRES-AROME&resolution=0025&domaine=FRANCE&coverageid=TOTAL_PRECIPITATION_RATE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND___2022-04-14T18:00:00Z
    pathGetDescribeCoverage=f"https://vs22yndw4thomnysosle3dxxry0aygnh.lambda-url.eu-west-1.on.aws/?modele={modele}&resolution={resolution}&domaine={domaine}&coverageid={Id['obj'].coverageId}"
    print(pathGetDescribeCoverage)
    rep=requests.get(pathGetDescribeCoverage)  # Requette describeCoverage au WCS
    print (rep.status_code)
    rep=json.loads(rep.content)
    lesDatesFutures=rep["timeDatePreviFutures"]
    print(lesDatesFutures)
    if rep["dim"]==4:
        lesNiveaux=rep[rep['niv']]
    else:
        lesNiveaux=[]
    print(lesNiveaux)
    print(rep["code"])
    param=rep["code"]
    chaineDateRun=rep["timeUTCRun"]
    for numDatePrevi in range(len(lesDatesFutures)): # Boucle sur les dates de prévision futures
        chaineDatePrévi=lesDatesFutures[numDatePrevi]
        if len(lesNiveaux) == 0 :
            pathGetCoverage=f"https://3vgqgy57ncpsr4lsev6pxphlue0nchwv.lambda-url.eu-west-1.on.aws/?modele={modele}&domaine={domaine}&coverageid={Id['obj'].coverageId}&chainedateprevi={chaineDatePrévi}&resolution={resolution}&lati={lati}&longi={longi}"
            print(pathGetCoverage)
            rep=requests.get(pathGetCoverage)
            print(rep.status_code)
            assert rep.status_code == 200
        else:
            for numNiveau in range(len(lesNiveaux)): # Boucle sur les niveaux verticaux du CoverageId
                niveau=lesNiveaux[numNiveau]
                #pathGetCoverage="https://3vgqgy57ncpsr4lsev6pxphlue0nchwv.lambda-url.eu-west-1.on.aws/?modele=HIGHRES-AROME&domaine=FRANCE&param=T(h)&niveau=2&chainedaterun=2022-04-25T00:00:00Z&chainedateprevi=2022-04-26T18:00:00Z&resolution=0025&lati=42.4825&longi=3.1274"
                pathGetCoverage=f"https://3vgqgy57ncpsr4lsev6pxphlue0nchwv.lambda-url.eu-west-1.on.aws/?modele={modele}&domaine={domaine}&coverageid={Id['obj'].coverageId}&niveau={niveau}&&chainedateprevi={chaineDatePrévi}&resolution={resolution}&lati={lati}&longi={longi}"
                print(pathGetCoverage)
                rep=requests.get(pathGetCoverage)
                print(rep.status_code)
                assert rep.status_code == 200
    nbID=nbID+1
fin=datetime.datetime.utcnow()
print (deb,fin, fin-deb)