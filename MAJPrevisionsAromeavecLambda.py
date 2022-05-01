#  Mise à jour de la base de previsions Arome.sqlite par interrogation du WCS de MF
#  en utilisant les fonctions Lambda développées pour accéder au WCS
#from getWCSCapabilities import getWCSCapabilities
import datetime
import os
import requests
import json
import sqlite3
from dateLimiteRetention import dateLimiteRetention
from Coverage import Coverage
import boto3
deb=datetime.datetime.utcnow()
lati=50.06  # les coordonnées géographiques de Lille
longi=3.06
resolution="0025"  # résolution du modèle Arome ("001" ou "0025")
modele="HIGHRES-AROME"
domaine="FRANCE"
ageMaxi=8.0  # age maximun (heures) des run qu'on va traiter
'''
covId=getWCSCapabilities(modele,resolution,domaine)  # lance requête getCapabilities au WCS de MF
print (covId)
jeunesCovId=  list(filter(lambda x:x["obj"].ageRun() <=ageMaxi,covId["lesID"])) # On ne traite que les CoverageId qui ont moins de 8 heures d'age
aTraiterCovId=list(filter(lambda x:x["obj"].aIgnorer()==False,jeunesCovId))  # On ignore certains CoverageId
exit()
'''
pathGetCapabilities=f"https://tb6azmdfcizyd4ueobtsdei2v40kxowu.lambda-url.eu-west-1.on.aws/?modele={modele}&resol={resolution}&domaine={domaine}"
covId=requests.get(pathGetCapabilities)
assert covId.status_code == 200 , covId.status_code
covId=json.loads(covId.content)
jeunesCovId=  list(filter(lambda x:Coverage(x["Id"],resolution,modele,domaine).ageRun() <=ageMaxi,covId["lesID"])) # On ne traite que les CoverageId qui ont moins de 8 heures d'age
aTraiterCovId=list(filter(lambda x:Coverage(x["Id"],resolution,modele,domaine).aIgnorer()==False,jeunesCovId))  # On ignore certains CoverageId
nbMaxIter=1000
aTraiterCovId=aTraiterCovId[0:nbMaxIter]
print("Nombre d'Id:",covId["nb_ID"],"Jeunes Id:",len(jeunesCovId),"A traiter:",len(aTraiterCovId))
nbID=0
sqlite_name="Arome_lambda.sqlite"  # ouverture de la bd où l'on va écrire les previsions
con = sqlite3.connect(sqlite_name)
cur = con.cursor()
con.commit()
nbprev=0
for Id in aTraiterCovId : # Boucle sur les CoverageId à traiter
    lesgetCoveragePaths=[]
    print ("nbID:",nbID," Id:",Id["Id"],"age du Run",str(Coverage(Id["Id"],resolution,modele,domaine).ageRun()))
    #pathGetDescribeCoverage="https://vs22yndw4thomnysosle3dxxry0aygnh.lambda-url.eu-west-1.on.aws/?modele=HIGHRES-AROME&resolution=0025&domaine=FRANCE&coverageid=TOTAL_PRECIPITATION_RATE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND___2022-04-14T18:00:00Z
    pathGetDescribeCoverage=f"https://vs22yndw4thomnysosle3dxxry0aygnh.lambda-url.eu-west-1.on.aws/?modele={modele}&resolution={resolution}&domaine={domaine}&coverageid={Id['Id']}"
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
    unit=rep["unite"]
    chaineDateRun=rep["timeUTCRun"]
    for numDatePrevi in range(len(lesDatesFutures)): # Boucle sur les dates de prévision futures
        chaineDatePrévi=lesDatesFutures[numDatePrevi]
        if len(lesNiveaux) == 0 :
            pathGetCoverage=f"https://3vgqgy57ncpsr4lsev6pxphlue0nchwv.lambda-url.eu-west-1.on.aws/?modele={modele}&domaine={domaine}&coverageid={Id['Id']}&chainedateprevi={chaineDatePrévi}&resolution={resolution}&lati={lati}&longi={longi}"
            lesgetCoveragePaths.append(pathGetCoverage)
        else:
            for numNiveau in range(len(lesNiveaux)): # Boucle sur les niveaux verticaux du CoverageId
                niveau=lesNiveaux[numNiveau]
                #pathGetCoverage="https://3vgqgy57ncpsr4lsev6pxphlue0nchwv.lambda-url.eu-west-1.on.aws/?modele=HIGHRES-AROME&domaine=FRANCE&param=T(h)&niveau=2&chainedaterun=2022-04-25T00:00:00Z&chainedateprevi=2022-04-26T18:00:00Z&resolution=0025&lati=42.4825&longi=3.1274"
                pathGetCoverage=f"https://3vgqgy57ncpsr4lsev6pxphlue0nchwv.lambda-url.eu-west-1.on.aws/?modele={modele}&domaine={domaine}&coverageid={Id['Id']}&niveau={niveau}&&chainedateprevi={chaineDatePrévi}&resolution={resolution}&lati={lati}&longi={longi}"
                lesgetCoveragePaths.append(pathGetCoverage)
    for pathGetCoverage in lesgetCoveragePaths :
        now=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        print(pathGetCoverage)
        rep=requests.get(pathGetCoverage)
        nbprev=nbprev+1
        reponse=json.loads(rep.content)
        assert rep.status_code == 200, rep.status_code
        print (now,reponse)
        nom=reponse["coverageId"].split("___")[0]
        abrev=reponse["code"]
        niv=reponse["typeNiveau"]
        hauteur=reponse["valNiveau"]
        run=reponse["coverageId"].split("___")[1][0:20]
        date=reponse["chaineDatePrevi"]
        val=reponse["valeur"]
        # écriture dans la bd
        cur.execute("INSERT INTO prevision (now,nom,abrev,niv,hauteur,unit,run,date,val) VALUES(?,?,?,?,?,?,?,?,?)",[now,nom,abrev,niv,hauteur,unit,run,date,val])
        con.commit()                                                                                                            
    nbID=nbID+1
fin=datetime.datetime.utcnow()
print ("debut:",deb," fin:",fin," durée:", fin-deb," nb CoverageId traités:",nbID," nb prévisions extraites:",nbprev)
dateLimite=dateLimiteRetention(40)  # on efface les données plus vieilles que de 40 heures
cmd='DELETE FROM prevision WHERE now <= "'+dateLimite+'"'
cur.execute(cmd)
con.commit()
con.close()  # Fermeture de la bd des prévisions
s3=boto3.client("s3")
s3.upload_file(sqlite_name, "elasticbeanstalk-eu-west-1-062282685834", "Arome_lambda.sqlite") # upload de la base sqlite vers S3