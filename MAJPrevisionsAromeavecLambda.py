#  Mise à jour de la base de previsions Arome.sqlite par interrogation du WCS de MF
#  en utilisant les fonctions Lambda développées pour accéder au WCS
#from getWCSCapabilities import getWCSCapabilities
import datetime
import os
import requests
import json
import sqlite3
from dateLimiteRetention import dateLimiteRetention
import boto3
import random
class CoverageId:
    '''
    Une chaine constituant l'Id d'un Coverage du WCS de MF
    Exemple de coverageId : "GEOMETRIC_HEIGHT__GROUND_OR_WATER_SURFACE___2022-05-01T00.00.00Z"
    '''
    def __init__(self,coverageId):
        self.coverageId=coverageId
    def ageRun(self):
        '''
        Retourne l'age actuel du run d'un coverageId
        
        '''
        format="%Y-%m-%dT%H.%M.%SZ" # format dans lequel est codée l'heure du run
        chaineDateRun=self.coverageId.split('___')[1][0:20] # la partie du coverageId indiqant l'heure UTC du run
        dateRunTs=datetime.datetime.strptime(chaineDateRun,format).timestamp()
        nowTs=datetime.datetime.utcnow().timestamp()
        return (nowTs-dateRunTs)/60/60 # age du Run en heures                                                                                                     
    def isCumul(self): 
        '''
        Le CoverageId concerne-t-il une donnée cumulée ou intégrée sur une durée ?
        '''
        index=self.coverageId.find("Z_P")
        if (index<0):
            return False
        else :
            return True
    def cumul(self):   
        '''
        Retourne la partie du CoverageId décrivant la durée du cumul
        '''
        if not self.isCumul():
            return ""
        else:
            index=self.coverageId.find("Z_P")
            return (self.coverageId[index+3:len(self.coverageId)])
    def dureeCumul(self):
        """
        Retourne la durée du cumul en secondes
        """
        cumul=self.cumul()
        #print(cumul)
        if cumul=="":
            return 0
        else:
            uniteDeTemps=cumul[len(cumul)-1:len(cumul)]
            if uniteDeTemps=="H":   #  il s'agit d'une durée exprimée en heures
                unit=3600
                nbUnite=cumul[1:len(cumul)-1]
            elif uniteDeTemps=="D":  # il s'agit d'une durée exprimée en jours
                unit=3600*24
                nbUnite=cumul[0:len(cumul)-1]
            elif uniteDeTemps=="M":  # il s'agit d'une durée exprimée en minutes
                unit=60
                nbUnite=cumul[1:len(cumul)-1]
            nb=int(nbUnite)
            return nb*unit
    def aIgnorer(self):
        '''
        Faut-il ignorer ce CoverageId pour l'actualisation des prévisions ?
        '''
        if (self.isCumul()) :    # cas des cumuls
            if (self.dureeCumul() == 3600) : return False  # on ne traite que les cumuls sur 1 heure 
            return True;   # tous les autres cumuls seront ignorés
        if "TURBULENT_KINETIC_ENERGY" in self.coverageId :   return True  
        if "GEOMETRIC_HEIGHT__" in self.coverageId :   return True  
        if "SPECIFIC_CLOUD_ICE_WATER" in self.coverageId :   return True 
        if "DEW_POINT" in self.coverageId :   return True 
        if "SPECIFIC_RAIN_WATER_CONTENT__ISOBARIC_SURFACE" in self.coverageId :   return True  ; 
        if "SPECIFIC_RAIN_WATER_CONTENT__SPECIFIC_HEIGHT_LEVEL" in self.coverageId :   return True  ;
        if "SPECIFIC_SNOW_WATER_CONTENT__" in self.coverageId :   return True  ;
        #if "SHORT_WAVE_RADIATION_FLUX__GROUND_OR_WATER_SURFACE" in self.coverageId :   return True  ;
        if "RELATIVE_HUMIDITY__ISOBARIC_SURFACE___" in self.coverageId :   return True  ;
        if "LOW_CLOUD_COVER__GROUND" in self.coverageId :   return True  ;
        if "HIGH_CLOUD_COVER__GROUND" in self.coverageId :   return True  ;
        if "MEDIUM_CLOUD_COVER__GROUND" in self.coverageId :   return True  ;
        if "CONVECTIVE_CLOUD_COVER__GROUND" in self.coverageId :   return True  ;
        if "PRESSURE__SPECIFIC_HEIGHT_LEVEL_" in self.coverageId :   return True  ;
        #if "PRESSURE__GROUND_OR_WATER" in self.coverageId :   return True  ;
        if "TOTAL_PRECIPITATION_RATE__SPECIFIC_HEIGHT" in self.coverageId :   return True  ;
        if "TOTAL_PRECIPITATION_RATE__ISOBARIC" in self.coverageId :   return True  ;
        if "ABSOLUTE_VORTICITY__ISOBARIC" in self.coverageId :   return True  ;
        if "TURBULENT_KINETIC_ENERGY__SPECIFIC_HEIGHT" in self.coverageId :   return True  ;
        if "TURBULENT_KINETIC_ENERGY__ISOBARIC" in self.coverageId :   return True  ;
        if "PSEUDO_ADIABATIC_POTENTIAL_TEMPERATURE__ISOBARIC" in self.coverageId :   return True  ;
        if "POTENTIAL_VORTICITY__ISOBARIC" in self.coverageId :   return True  ;
        if "TEMPERATURE__GROUND_OR_WATER_SURFACE" in self.coverageId :   return True  ;
        if "TEMPERATURE__ISOBARIC_SURFACE" in self.coverageId :   return True  ;
        if "U_COMPONENT_OF_WIND__ISOBARIC_" in self.coverageId :   return True  ;
        if "U_COMPONENT_OF_WIND__POTENTIAL_VORTICITY" in self.coverageId :   return True  ;
        if "V_COMPONENT_OF_WIND__ISOBARIC_SURFACE" in self.coverageId :   return True  ;
        if "V_COMPONENT_OF_WIND__POTENTIAL_VORTICITY" in self.coverageId :   return True  ;
        if "GEOPOTENTIAL__ISOBARIC_SURFACE___" in self.coverageId :   return True  ;
        return False
deb=datetime.datetime.utcnow()
print ("debut:",deb)
lati=50.06  # les coordonnées géographiques de Lille
longi=3.06
resolution="0025"  # résolution du modèle Arome ("001" ou "0025")
modele="HIGHRES-AROME"
domaine="FRANCE"
ageMaxi=8.0  # age maximun (heures) des run qu'on va traiter
pathGetCapabilities=f"https://tb6azmdfcizyd4ueobtsdei2v40kxowu.lambda-url.eu-west-1.on.aws/?modele={modele}&resol={resolution}&domaine={domaine}"
covId=requests.get(pathGetCapabilities)
assert covId.status_code == 200 , covId.status_code
covId=json.loads(covId.content)
jeunesCovId=  list(filter(lambda x:CoverageId(x["Id"]).ageRun() <=ageMaxi,covId["lesID"])) # On ne traite que les CoverageId qui ont moins de 8 heures d'age
aTraiterCovId=list(filter(lambda x:CoverageId(x["Id"]).aIgnorer()==False,jeunesCovId))  # On ignore certains CoverageId
nbMaxIter=1000
aTraiterCovId=aTraiterCovId[0:nbMaxIter]
print("Nombre d'Id:",covId["nb_ID"],"Jeunes Id:",len(jeunesCovId),"A traiter:",len(aTraiterCovId))
nbID=0
sqlite_name="Arome_lambda.sqlite"  # ouverture de la bd où l'on va écrire les previsions
con = sqlite3.connect(sqlite_name)
cur = con.cursor()
dateLimite=dateLimiteRetention(40)  # on efface de la base les données plus vieilles que de 40 heures
cmd='DELETE FROM prevision WHERE now <= "'+dateLimite+'"'
cur.execute(cmd)
con.commit()
nbprev=0
random.shuffle(aTraiterCovId)  # on mélange les CoverageId pour ne pas toujours les traiter dans le même ordre
print (aTraiterCovId)
for Id in aTraiterCovId : # Boucle sur les CoverageId à traiter
    lesgetCoveragePaths=[]
    print ("nbID:",nbID," Id:",Id["Id"],"age du Run",str(CoverageId(Id["Id"]).ageRun()))
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
        try:
            now=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
            print(pathGetCoverage)
            rep=requests.get(pathGetCoverage)
            assert rep.status_code == 200, rep.status_code
            nbprev=nbprev+1
            reponse=json.loads(rep.content)
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
        except Exception as exp :
            print ("Heure UTC:", datetime.datetime.utcnow(), "Exception levée pendant getCoverage", exp, "")
    nbID=nbID+1
fin=datetime.datetime.utcnow()
print ("debut:",deb," fin:",fin," durée:", fin-deb," nb CoverageId traités:",nbID," nb prévisions extraites:",nbprev)
con.commit()
con.close()  # Fermeture de la bd des prévisions
s3=boto3.client("s3")
s3.upload_file(sqlite_name, "elasticbeanstalk-eu-west-1-062282685834", "Arome_lambda.sqlite") # upload de la base sqlite vers S3