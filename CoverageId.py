# coding: utf8
import sys
import requests
import string
import datetime
import time
import calendar
#import gdal
import json
import numpy as np
sys.path.insert(0, '/home/ubuntu/workspace/Utils') # insérer dans sys.path le dossier contenant le/les modules
from Utils import chaineUTCFromTs,tsNow
from xml.dom import minidom
from CatalogueWCS import CatalogueWCS
from WCSGeotiff import WCSGeotiff
class CoverageId :
    def __init__(self, coverageId,resol):
        self.coverageId = coverageId  # le label renvoyé par la requête getCapabilities du WCS
        self.resol=resol  # la résolution ("001" ou "0025"), la même que celle fournie à la requête getCapabilities du WCS
        self.descr=""  # description renvoyée par la requette getCapabilities du WCS
        self.code=""
        for k,v in CatalogueWCS.catalogueWCS.items():
            (nom,desc)=v
            if nom==self.chaineNom():
                self.code=k
                break
        if self.code=="":
            raise Exception (self.chaineNom() + " non trouvee dans le dictionnaire"  +self.descr)
        self.timeUTCRun=self.chaineDate()
        self.timeUTCRunTs=self.tsUTCRun()
        self.timeDeb=""
        self.timeFin=""
    def chaineNom (self):
        #index=string.find(self.coverageId,"___");
        index=self.coverageId.find("___");
        rep=self.coverageId[0:index];
        return rep
    def chaineDate(self):  # retourne la partie de l'Id indiquant la date du run sous un format du type : "2019-01-13T13:00:00Z"
        #index=string.find(self.coverageId,"___");
        index=self.coverageId.find("___");
        rep=self.coverageId[index+3:index+23];
        rep=rep.replace(".",":")
        return rep
    def dateUTCRun(self):   # objet date UTC du RUN par decodage de chaineDate()
        chaine=self.chaineDate()
        return self.dateFromChaine(chaine)
    def dateFromChaine(self,chaine):  #  objet date à partir d'une chaine du type : "2019-01-13T13:00:00Z"
        rep=datetime.datetime.strptime(chaine,'%Y-%m-%dT%H:%M:%SZ')
        return rep
    def tsUTCRun(self):    # timestamp UTC du RUN
        dateUTC=self.dateUTCRun()
        return self.ts(dateUTC)
    def ts(self,dateUTC):  #  timestamp d'une date UTC
        #return int(dateUTC.strftime('%s'))
        epoch=datetime.datetime(1970,1,1)
        dt=dateUTC-epoch
        ts=(dt.microseconds + (dt.seconds + dt.days * 86400) * 10**6) / 10**6
        return ts
    def ageRun(self):      # age du RUN en heures par différence à l'heure actuelle
        ts = time.time()   
        #ts= calendar.timegm(time.gmtime())
        return (ts-self.tsUTCRun())/60./60.
    def isCumul(self):    # le CoverageId concerne-t-il une donnée cumulée ou intégrée sur une durée ?
        #index=string.find(self.coverageId,"Z_P")
        index=self.coverageId.find("Z_P");
        if (index<0):
            return False;
        else :
            return True;
    def cumul(self):   #  partie du CoverageId décrivant la durée du cumul
        if not self.isCumul():
            return ""
        else:
            #index=string.find(self.coverageId,"Z_P")
            index=self.coverageId.find("Z_P");
            return (self.coverageId[index+3:len(self.coverageId)])
    def dureeCumul(self):  #  durée du cumul en secondes
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
    def describeCoveragePath(self) :  #calcul le path pour une requête describeCoverage pour ce CoverageID
        model="MF-NWP-HIGHRES-AROME-"+self.resol+"-FRANCE-WCS";
        path="https://geoservices.meteofrance.fr/services/"+model+"?SERVICE=WCS&version=2.0.1&REQUEST=DescribeCoverage&coverageID=";
        path=path+self.coverageId+"&token=__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__"; 
        print("path pour getdescribeCoverage : ",path)
        return path
    def describeCoverage(self):  # Envoi et traitement d'une requette describeCoverage pour ce CoverageId
        path = self.describeCoveragePath()
        status=-1
        retry=0
        while status != 200 and retry<=10:
            retry=retry+1
            r=requests.get(path)  # envoi d'une requête "describeCoverage" du WCS
            status=r.status_code
            time.sleep(1)
            #print("path: ",path," status decribeCoverage : ",str(status))
        if retry>10 :
            print("retry : "+str(retry)+" path: ",path," status decribeCoverage : ",str(status))
            sys.exit(retry)
        with open("WCSDescribeCoverage.xml","wb") as fichier:
            fichier.write(r.content)
        res=self.analyseXML("WCSDescribeCoverage.xml")
        return res    # renvoi la liste des résultats
    def analyseXML(self,XMLFileName):
        mydoc = minidom.parse(XMLFileName)  # parse an XML file given by his name
        res={}  # le résultat de la requête sera mis dans un dictionnaire
        def getItems (tagName,code):
            #print (tagName)
            items = mydoc.getElementsByTagName(tagName) # recherches du tagName dans le ficheir XML parsé
            for i in range (0,len(items)):
                if (len(items[i].childNodes)>0):
                    val=items[i].childNodes[0].nodeValue
                else:
                    val=items[i].nodeValue
                #print val
                if len(items)>1:
                    complem=str(i)
                else:
                    complem=""
                if (val):
                    self.__dict__[code+complem]=val
                    res[code+complem]=val  # écriture de la valeur associée au tagName dans le dictionnire des résultats
        getItems ('swe:description',"descr")
        unit=mydoc.getElementsByTagName("swe:uom")[0].attributes.getNamedItem("code").nodeValue
        res["descrUnite"]=unit
        self.unite=unit
        #gmlrgrid:offsetVector srsDimension="4"
        dim=mydoc.getElementsByTagName("gmlrgrid:offsetVector")[0].attributes.getNamedItem("srsDimension").nodeValue
        self.dim=int(dim)   # nombre d'axes (dimensions) du coverageId
        getItems ('gmlrgrid:gridAxesSpanned',"axe")
        getItems ('gmlrgrid:coefficients',"axeCoeff")
        getItems ('gml:pos',"pos")
        getItems ('gml:low',"grilleLow")
        getItems ('gml:high',"grilleHigh")
        getItems ('gml:lowerCorner',"cornerLow")
        getItems ('gml:upperCorner',"cornerUpper")
        getItems ('gml:beginPosition',"timeDeb")
        self.timeDebTs=self.ts(self.dateFromChaine(self.timeDeb))
        getItems ('gml:endPosition',"timeFin")
        self.timeFinTs=self.ts(self.dateFromChaine(self.timeFin))
        self.timeCumul=self.dureeCumul()
        self.Id=self.coverageId
        self.code=self.code
        for cle in self.__dict__:  # découpage des coefficients des axes et mise dans un tableau
            if "Coeff" in cle:
                val=self.__dict__[cle]
                val=list(map(lambda x: int(x), val.split()))
                self.__dict__[cle]=val
        if self.dim==3 :    # contôle cohérence timeDeb, timeFin et axe des temps
            axeTime="axeCoeff2"
            self.niv=None
        else:  #  cas où dim= 4 et où il y a un niveau vertical
            axeTime="axeCoeff3"
            axeNiv="axeCoeff2"
            self.niv=self.__dict__["axe2"]
            self.__dict__[self.niv]=self.__dict__[axeNiv]
            del self.__dict__[axeNiv]
        self.time=self.__dict__[axeTime]  #  renommage de l'axe des temps
        del self.__dict__[axeTime]
        tab=[]
        for ts in self.time:  # Ajout des dates des prévisions
            tsPrevi=self.timeUTCRunTs+ts
            chainePrevi=chaineUTCFromTs(tsPrevi)
            tab.append(chainePrevi)
        self.timeDatePrevi=tab
        self.timeNbEch=len(self.time)  # nombre d'échéance temporelles dasn le CoverageId
        tsFin=self.timeUTCRunTs+self.time[-1]
        if tsFin != self.timeFinTs :
            print (self.timeDeb)
            print (self.timeDebTs)
            print (self.time[-1])
            print (tsFin)
            print (self.timeFin)
            print (self.timeFinTs)
            raise Exception ("Erreur timeFinTs")
        tsDeb=self.timeUTCRunTs+self.time[0]
        if tsDeb != self.timeDebTs : raise Exception ("Erreur timeDebTs")
        chaineDateNow=chaineUTCFromTs(tsNow())  # calcul datePréviFutures
        self.timeUTCNow=chaineDateNow
        rep=[]
        for date in self.timeDatePrevi:
            if date>=chaineDateNow : rep.append(date)
        self.timeDatePreviFutures=rep
        self.timeNbEchFutures=len(self.timeDatePreviFutures)
    def niveau(self,numNiv):  #  renvoi la valeur du "numNiv" -ième niveau 
        if numNiv<0 or numNiv> len(self.__dict__[self.niv]):
            raise Exception ("Numéro de niveau non valide: %s" % numNiv)
        return self.__dict__[self.niv][numNiv]
    def getCoverage(self,latiSud,latiNord,longiOuest,longiEst,chaineDatePrevi,niv=None): # Envoi d'une requête "getCoverage" du service WCS
        if self.niv and not (niv in self.__dict__[self.niv]): raise Exception ("getCoverage: Le niveau= "+str(niv)+" n'existe pas" )
        """ https://geoservices.meteofrance.fr/api/__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__
         /MF-NWP-HIGHRES-AROME-0025-FRANCE-WCS?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage
         &format=image/tiff&coverageId=GEOPOTENTIAL__ISOBARIC_SURFACE___2017-08-29T06.00.00Z
         &subset=lat(50.0,51.0)&subset=long(3.0,4.0)&subset=pressure(100)&subset=time(2017-08-29T15:00:00Z)"""
        
        path="https://geoservices.meteofrance.fr/api/__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__/MF-NWP-HIGHRES-AROME-";
        path=path+self.resol+"-FRANCE-WCS?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&format=image/tiff&coverageId=";
        path=path+self.coverageId
        latitude  = "&subset=lat("+str(latiSud)+","+str(latiNord)+")"
        longitude = "&subset=long("+str(longiOuest)+","+str(longiEst)+")";
        path=path+latitude+longitude
        if niv: path=path+"&subset="+self.niv+"("+str(niv)+")"  # ajout du niveau, if any
        path=path+"&subset=time("+chaineDatePrevi+")"
        self.chaineDatePreviGot=chaineDatePrevi
        self.nivGot=niv
        self.filename="WCSgetCoverage.tiff"
        print ("   ")
        print ("getCoverage path: "+path)
        status=-1
        isGeotiff=False
        nb_getCoverage=1
        while status != 200 or not isGeotiff:
            if not(status==-1): time.sleep(0.5)    # sauf la première fois, wait in seconds pour ne pas surcharger le serveur
            r=requests.get(path)  # envoi d'une requête "getCoverage" du WCS
            status=r.status_code
            print (nb_getCoverage,"getCoverage code: "+str(r.status_code))
            print ("longueur retournée: "+ str(len(r.content)))
            print ("deux premiers octets : "+str(r.content[0:2]))
            debut=r.content[0:2]  # lecture des deux premiers octets du buffer retourné
            if debut==b'II' or debut == b'MM':  # on vérifie que le buffer retourné est bien un Geotiff
                isGeotiff=True
            else :
                isGeotiff=False
            print (isGeotiff)
            nb_getCoverage=nb_getCoverage+1
        with open(self.filename,"wb") as fichier:
            fichier.write(r.content)
        self.geotiff=WCSGeotiff(path,self.filename)  # décodage du Geotiff
    def valeur(self,longi,lati):  #  renvoi la valeur du champs sans interpolation
        return self.geotiff.valeur(longi,lati)
    def aIgnorer(self):  # Faut-il le traiter pour l'actualisation des prévisions ?
        if (self.isCumul()) :    # cas des cumuls
            if (self.dureeCumul() == 3600) : return False  # on ne traite que les cumuls sur 1 heure 
            return True;   # tous les autres cumuls seront ignorés
        if "TURBULENT_KINETIC_ENERGY" in self.coverageId :   return True  
        if "GEOMETRIC_HEIGHT__" in self.coverageId :   return True  
        if "SPECIFIC_CLOUD_ICE_WATER" in self.coverageId :   return True  ;
        if "SPECIFIC_RAIN_WATER_CONTENT__ISOBARIC_SURFACE" in self.coverageId :   return True  ; 
        if "SPECIFIC_RAIN_WATER_CONTENT__SPECIFIC_HEIGHT_LEVEL" in self.coverageId :   return True  ;
        if "SPECIFIC_SNOW_WATER_CONTENT__" in self.coverageId :   return True  ;
        if "SHORT_WAVE_RADIATION_FLUX__GROUND_OR_WATER_SURFACE" in self.coverageId :   return True  ;
        if "RELATIVE_HUMIDITY__ISOBARIC_SURFACE___" in self.coverageId :   return True  ;
        if "LOW_CLOUD_COVER__GROUND" in self.coverageId :   return True  ;
        if "HIGH_CLOUD_COVER__GROUND" in self.coverageId :   return True  ;
        if "MEDIUM_CLOUD_COVER__GROUND" in self.coverageId :   return True  ;
        if "CONVECTIVE_CLOUD_COVER__GROUND" in self.coverageId :   return True  ;
        if "PRESSURE__SPECIFIC_HEIGHT_LEVEL_" in self.coverageId :   return True  ;
        if "PRESSURE__GROUND_OR_WATER" in self.coverageId :   return True  ;
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
        if "U_COMPONENT_OF_WIND_GUST__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND" in self.coverageId :   return True  ;
        if "V_COMPONENT_OF_WIND__ISOBARIC_SURFACE" in self.coverageId :   return True  ;
        if "V_COMPONENT_OF_WIND__POTENTIAL_VORTICITY" in self.coverageId :   return True  ;
        if "V_COMPONENT_OF_WIND_GUST__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND" in self.coverageId :   return True  ;
        if "GEOPOTENTIAL__ISOBARIC_SURFACE___" in self.coverageId :   return True  ;
        if "WIND_SPEED__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND" in self.coverageId :   return True  ;
        if "WIND_SPEED__ISOBARIC_SURFACE" in self.coverageId :   return True  ;
        if "DEW_POINT_TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND" in self.coverageId :   return True  ;
        return False
    def affiche(self):
        print (json.dumps(self.__dict__,indent=4,sort_keys=True))
    