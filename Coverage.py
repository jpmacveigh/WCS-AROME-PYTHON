# coding: utf8
'''
Classe Coverage
'''
import sys
import requests
import datetime
import time
import calendar
import gdal
import json
from Client_APIM_MF import Client_APIM_MF  # client MF pour renouveler le token d'acces à l'API WCS de MF (depuis janvier 2022)
from WCSGeotiff import WCSGeotiff
from WCSGeogrib import WCSGeogrib
sys.path.insert(0, '/home/ubuntu/workspace/Utils') # insérer dans sys.path le dossier contenant le/les modules
sys.path.insert(0,'/content/WCS-AROME-PYTHON')
from Utils import chaineUTCFromTs,tsNow
from xml.dom import minidom
from CatalogueWCS import CatalogueWCS
class Coverage :
    def __init__(self, coverageId,resol,modele,domaine):
        domaines=["FRANCE","EUROPE","GLOBE"]       # les domaines possibles
        assert domaine in domaines,domaine          
        resols=["001","0025","01","025"]           # les résolutions possibles
        assert resol in resols,resol              
        models=["HIGHRES-AROME","GLOBAL-ARPEGE"]   # les modèles MF possibles
        assert modele in models,modele
        modele_resol_domaine=f"{modele}-{resol}-{domaine}"
        combinaisons=["HIGHRES-AROME-001-FRANCE","HIGHRES-AROME-0025-FRANCE","GLOBAL-ARPEGE-01-EUROPE","GLOBAL-ARPEGE-025-GLOBE"]
        assert modele_resol_domaine in combinaisons , modele_resol_domaine
        self.coverageId = coverageId  # le label renvoyé par la requête getCapabilities du WCS
        self.resol=resol  # la résolution ("001" ou "0025"), la même que celle fournie à la requête getCapabilities du WCS
        self.descr=""  # description renvoyée par la requette getCapabilities du WCS
        self.code=""
        self.modele=modele
        self.petit_modele=self.modele.split("-")[1].lower()
        self.domaine=domaine
        for k,v in CatalogueWCS.catalogueWCS.items():
            #print (v)
            (nom,desc,type_var,dimension)=v
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
        index=self.coverageId.find("___");
        rep=self.coverageId[0:index];
        return rep
    
    def chaineDate(self):  # retourne la partie de l'Id indiquant la date du run sous un format du type : "2019-01-13T13:00:00Z"
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
    
    def isCumul(self):    # le Coverage concerne-t-il une donnée cumulée ou intégrée sur une durée ?
        index=self.coverageId.find("Z_P")
        if (index<0):
            return False;
        else :
            return True;
    
    def cumul(self):   #  partie du Coverage décrivant la durée du cumul
        if not self.isCumul():
            return ""
        else:
            index=self.coverageId.find("Z_P")
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
        #model="MF-NWP-HIGHRES-AROME-"+self.resol+"-FRANCE-WCS";
        model="MF-NWP-"+self.modele+"-"+self.resol+"-"+self.domaine+"-WCS";
        # forme avant 2022 :
        #https://geoservices.meteofrance.fr/services/MF-NWP-GLOBAL-ARPEGE-01-EUROPE-WCS?SERVICE=WCS&version=2.0.1&REQUEST=DescribeCoverage&coverageID=TEMPERATURE__GROUND_OR_WATER_SURFACE___2021-12-30T12.00.00Z&token=__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__
        #path="https://geoservices.meteofrance.fr/services/"+model+"?SERVICE=WCS&version=2.0.1&REQUEST=DescribeCoverage&coverageID=";
        #path=path+self.coverageId+"&token=__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__"; 
        # nouvelle forme depuis 2022 :
        #"https://public-api.meteofrance.fr/public/arome/1.0/wcs/MF-NWP-HIGHRES-AROME-001-FRANCE-WCS/DescribeCoverage?service=WCS&version=2.0.1"
        #"https://public-api.meteofrance.fr/public/arpege/1.0/wcs/MF-NWP-GLOBAL-ARPEGE-01-EUROPE-WCS/DescribeCoverage?service=WCS&version=2.0.1&coverageID=%22ttttttttooooo%22"
        path =f"https://public-api.meteofrance.fr/public/{self.petit_modele}/1.0/wcs/{model}/DescribeCoverage?service=WCS&version=2.0.1&coverageID={self.coverageId}"
        return path
    
    def describeCoverage(self):  # Envoi et traitement d'une requette describeCoverage pour ce Coverage
        path = self.describeCoveragePath()
        print(path)
        status=-1
        retry=0
        while status != 200 and retry<=10:
            retry=retry+1
            #r=requests.get(path)  # envoi d'une requête "describeCoverage" du WCS
            r=Client_APIM_MF().request("GET",path,verify=False)   # envoi d'une requête "describeCoverage" du WCS
            status=r.status_code
            print("path: ",path," status decribeCoverage : ",str(status))
            if (status != 200): time.sleep(30.)
        if retry>10 :
            print("retry : "+str(retry)+" path: ",path," status decribeCoverage : ",str(status))
            sys.exit(retry)       
        with open("WCSDescribeCoverage.xml","wb") as fichier : # le résultat de la requête est un XML qui l'on écrit dans un fichier
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
        self.timeNbEch=len(self.time)  # nombre d'échéance temporelles dasn le Coverage
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
        if self.niv == None:  return 0
        if numNiv<0 or numNiv> len(self.__dict__[self.niv]):
            raise Exception ("Numéro de niveau non valide: %s" % numNiv)
        return self.__dict__[self.niv][numNiv]
    
    def getCoverage_grib(self,latiSud,latiNord,longiOuest,longiEst,chaineDatePrevi,niv=None): # Envoi d'une requête "getCoverage" du service WCS avec le résultat en format GRIB
        if self.niv and not (niv in self.__dict__[self.niv]): raise Exception ("getCoverage: Le niveau= "+str(niv)+" n'existe pas" )
        # forme du path à partir de 2022 :
        #https://public-api.meteofrance.fr/public/arome/1.0/wcs/MF-NWP-HIGHRES-AROME-001-FRANCE-WCS/GetCoverage?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&format=application/wmo-grib&coverageId=TEMPERATURE__SPECIFIC_HEIGHT_LEVEL_ABOVE_GROUND___2022-03-15T12:00:00Z&subset=time(2022-03-16T14:00:00Z)&subset=lat(48.72635426558551,51.19827809371051)&subset=long(0.8998690061271146,4.865933459252115)&subset=height(2)
        model=model="MF-NWP-"+self.modele+"-"+self.resol+"-"+self.domaine+"-WCS"
        path=f"https://public-api.meteofrance.fr/public/{self.petit_modele}/1.0/wcs/{model}/GetCoverage?service=WCS&version=2.0.1&coverageid={self.coverageId}"
        latitude  = "&subset=lat("+str(latiSud)+","+str(latiNord)+")"
        longitude = "&subset=long("+str(longiOuest)+","+str(longiEst)+")";
        path=path+latitude+longitude
        path=path+"&format=application/wmo-grib"
        if niv: path=path+"&subset="+self.niv+"("+str(niv)+")"  # ajout du niveau, if any
        path=path+"&subset=time("+chaineDatePrevi+")"
        self.chaineDatePreviGot=chaineDatePrevi
        self.nivGot=niv
        self.filename="WCSgetCoverage.grib"
        #print ("getCoverage_grib path: "+path)
        status=-1
        isGrib=False
        while status != 200 or not isGrib:
            if not(status==-1): time.sleep(2.5)    # sauf la première fois, wait in seconds pour ne pas surcharger le serveur
            #r=requests.get(path)  # envoi d'une requête "getCoverage" du WCS
            r=Client_APIM_MF().request("GET",path,verify=False)   # envoi d'une requête "getCoverage" du WCS
            status=r.status_code
            print (path)
            print ("getCoverage_grib code: "+str(r.status_code))
            print ("longueur retournée: "+ str(len(r.content)))
            print ("deux premiers octets : "+str(r.content[0:4]))
            debut=r.content[0:4]  # lecture des deux premiers octets du buffer retourné
            if debut==b'GRIB':  # on vérifie que le buffer retourné est bien un Grib
                isGrib=True
            else :
                isGrib=False
            print ("isGrib : "+str(isGrib))
            time.sleep(1)
        with open(self.filename,"wb") as fichier :  # le résultat de la requête est un geotiff que l'on écrit dans un fichier
          fichier.write(r.content)
        self.geogrib=WCSGeogrib(path,self.filename)  # décodage du Geogrib
    
    def getCoverage_tiff(self,latiSud,latiNord,longiOuest,longiEst,chaineDatePrevi,niv=None): # Envoi d'une requête "getCoverage" du service WCS
        if self.niv and not (niv in self.__dict__[self.niv]): raise Exception ("getCoverage: Le niveau= "+str(niv)+" n'existe pas" )
        
        """ https://geoservices.meteofrance.fr/api/__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__
         /MF-NWP-HIGHRES-AROME-0025-FRANCE-WCS?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage
         &format=image/tiff&coverageId=GEOPOTENTIAL__ISOBARIC_SURFACE___2017-08-29T06.00.00Z
         &subset=lat(50.0,51.0)&subset=long(3.0,4.0)&subset=pressure(100)&subset=time(2017-08-29T15:00:00Z)
        model=model="MF-NWP-"+self.modele+"-"+self.resol+"-"+self.domaine+"-WCS"
        path="https://geoservices.meteofrance.fr/api/__BvvAzSbJXLEdUJ--rRU0E1F8qi6cSxDp5x5AtPfCcuU__/"+model
        path=path+"?SERVICE=WCS&VERSION=2.0.1&REQUEST=GetCoverage&format=image/tiff&coverageId=";
        path=path+self.coverageId
        latitude  = "&subset=lat("+str(latiSud)+","+str(latiNord)+")"
        longitude = "&subset=long("+str(longiOuest)+","+str(longiEst)+")";
        path=path+latitude+longitude
        if niv: path=path+"&subset="+self.niv+"("+str(niv)+")"  # ajout du niveau, if any
        path=path+"&subset=time("+chaineDatePrevi+")"
        """
        
        # forme du path à partir de 2022 :
        #"https://public-api.meteofrance.fr/public/arome/1.0/wcs/MF-NWP-HIGHRES-AROME-0025-FRANCE-WCS/GetCoverage?service=WCS&version=2.0.1&coverageid=%22tototo%22&subset=%22llllll%22&format=image%2Ftiff"
        model=model="MF-NWP-"+self.modele+"-"+self.resol+"-"+self.domaine+"-WCS"
        path=f"https://public-api.meteofrance.fr/public/{self.petit_modele}/1.0/wcs/{model}/GetCoverage?service=WCS&version=2.0.1&coverageid={self.coverageId}"
        latitude  = "&subset=lat("+str(latiSud)+","+str(latiNord)+")"
        longitude = "&subset=long("+str(longiOuest)+","+str(longiEst)+")";
        path=path+latitude+longitude
        if niv: path=path+"&subset="+self.niv+"("+str(niv)+")"  # ajout du niveau, if any
        path=path+"&subset=time("+chaineDatePrevi+")"
        self.chaineDatePreviGot=chaineDatePrevi
        self.nivGot=niv
        self.filename="WCSgetCoverage.tiff"
        #print ("getCoverage path: "+path)
        status=-1
        isGeotiff=False
        while status != 200 or not isGeotiff:
            if not(status==-1): time.sleep(0.5)    # sauf la première fois, wait in seconds pour ne pas surcharger le serveur
            #r=requests.get(path)  # envoi d'une requête "getCoverage" du WCS
            r=Client_APIM_MF().request("GET",path,verify=False)   # envoi d'une requête "getCoverage" du WCS
            status=r.status_code
            print (path)
            print ("getCoverage code: "+str(r.status_code))
            print ("longueur retournée: "+ str(len(r.content)))
            print ("deux premiers octets : "+str(r.content[0:2]))
            debut=r.content[0:2]  # lecture des deux premiers octets du buffer retourné
            if debut==b'II' or debut == b'MM':  # on vérifie que le buffer retourné est bien un Geotiff
                isGeotiff=True
            else :
                isGeotiff=False
            print ("isGeotiff : "+str(isGeotiff))
            time.sleep(1)
        with open(self.filename,"wb") as fichier :  # le résultat de la requête est un geotiff que l'on écrit dans un fichier
          fichier.write(r.content)
        self.geotiff=WCSGeotiff(path,self.filename)  # décodage du Geotiff
    
    def nearest_value_tiff(self,longi,lati):  #  renvoi la valeur du champs sans interpolation
        return self.geotiff.nearest_value(longi,lati)
    
    def nearest_value_grib(self,longi,lati):  #  renvoi la valeur du champs sans interpolation
        return self.geogrib.nearest_value(longi,lati)
    
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
        #if "TEMPERATURE__GROUND_OR_WATER_SURFACE" in self.coverageId :   return True  ;
        if "TEMPERATURE__ISOBARIC_SURFACE" in self.coverageId :   return True  ;
        if "U_COMPONENT_OF_WIND__ISOBARIC_" in self.coverageId :   return True  ;
        if "U_COMPONENT_OF_WIND__POTENTIAL_VORTICITY" in self.coverageId :   return True  ;
        if "V_COMPONENT_OF_WIND__ISOBARIC_SURFACE" in self.coverageId :   return True  ;
        if "V_COMPONENT_OF_WIND__POTENTIAL_VORTICITY" in self.coverageId :   return True  ;
        if "GEOPOTENTIAL__ISOBARIC_SURFACE___" in self.coverageId :   return True  ;
        return False
    
    def affiche(self):
        print (json.dumps(self.__dict__,indent=4,sort_keys=True))