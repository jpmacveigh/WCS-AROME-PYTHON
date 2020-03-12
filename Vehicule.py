#coding: utf8
import json
import sqlite3
import requests
import arrow
import math
import sys
import datetime
import random
#from getWCSCapabilities import profilVertical
#from getWCSCapabilities import mostRecentId
#from getWCSCapabilities import prevision
from AxeVertical import AxeVertical
from VentHorizontal import VentHorizontal
from Utils import getHeureLocale
sys.path.insert(0,'/home/ubuntu/node_jpmv/Utils') # insérer dans sys.path le dossier contenant le/les modules
from Utils import *
sys.path.insert(0,'/home/ubuntu/environment/python_grib') # insérer dans sys.path le dossier contenant le/les modules
from util_eccodes import *
class Vehicule:  # un véhicule qui se déplace
    def __init__(self,lat,lng,alt):  # constructeur
        if not(-180.<=lng<=180.): raise Exception ("Vehicule : lng doit être dans [-180,+180]")
        if not(-90.<=lat<=90.): raise Exception ("Vehicule : lat doit être dans [-90,+90]")
        if not(alt>=0.): raise Exception ("Vehicule : alt être >= 0.")
        self.lng=lng
        self.lat=lat
        self.alt=alt
        self.getTimeZoneParIpgeolocation()   #  la timezone du lieu
        self.getSunRiseSunSet()  #  détermination heures locales de lever et de coucher du soleil du lieu du véhicule
        self.getHauteur()  #  aquisition de la hauteur en fonction de l'heure
        self.getVille()  # recherche du nom de la ville qui est en dessous
        self.initDB()
        print ("hauteurs du véhicule : ",self.alt,self.hauteur)
    def getTime(self):  # Quelle heure UTC est-il ?
        self.heureUTC=arrow.utcnow()
        self.tsUTC=self.heureUTC.timestamp;
        #print ("heure UTC: "+str(self.heureUTC)+"  soit TS: "+str(self.tsUTC))
        #print ("heure locale Paris: "+str(self.heureUTC.to("Europe/Paris")))  # heure de Paris
    def getTimeZone(self):  #  Dans quel fuseau horaire suis-je ?
        self.getTime();
        urlGetTZ="https://maps.googleapis.com/maps/api/timezone/json?location="+str(self.lat)+","+str(self.lng)+"&timestamp="+str(self.tsUTC)+"&key=AIzaSyAJ5k6nijmVsFGQ8EqVs4YiSkdDucJbJ2s"
        status=0
        while status != 200:
            r=requests.get(urlGetTZ)
            status=r.status_code
        #print r.content  # le résultat de la requête
        # tester :  http://api.timezonedb.com/v2.1/get-time-zone?key=TE4GPIYXBN1Y&format=json&by=position&lat=50.6&lng=3.06&time=1552207312
        # tester :  http://api.geonames.org/timezoneJSON?lat=49.11&lng=-27.82&username=demo
        self.timeZone=json.loads(r.content)
        if (self.timeZone["status"]=="ZERO_RESULTS"):  # si Google ne fournit pas le timezone
            #raise Exception ("Vehicule : timeZone inconnu de Google")
            print ("Vehicule : timeZone inconnu de Google")
            #self.heureLocale=getHeureLocale(self.heureUTC,self.lng)
            locale =float(self.heureUTC.timestamp)+(43200.*float(self.lng)/180.);  # décalage horaire géogrphique qui ne dépend que de la longitude du lieu
            self.heureLocale=arrow.get(locale)
            print ("heure UTC           : "+str(self.heureUTC))
            print ("heure locale du lieu: "+str(self.heureLocale))
        else:    
            self.heureLocale=self.heureUTC.to(self.timeZone["timeZoneId"])
    def getTimeZoneParIpgeolocation(self):  #  Dans quel fuseau horaire suis-je ?
        self.getTime();
        # https://api.ipgeolocation.io/timezone?apiKey=87922ec82b4846b0aa6e6ffcf7ccbb78&lat=-27.4748&long=153.017
        urlGetTZ="https://api.ipgeolocation.io/timezone?apiKey=87922ec82b4846b0aa6e6ffcf7ccbb78&lat="+str(self.lat)+"&long="+str(self.lng)
        status=0
        while status != 200:
            r=requests.get(urlGetTZ)
            status=r.status_code
        #print r.content  # le résultat de la requête
        # tester :  http://api.timezonedb.com/v2.1/get-time-zone?key=TE4GPIYXBN1Y&format=json&by=position&lat=50.6&lng=3.06&time=1552207312
        # tester :  http://api.geonames.org/timezoneJSON?lat=49.11&lng=-27.82&username=demo
        self.timeZone=json.loads(r.content)
        self.heureLocale=self.heureUTC.to(self.timeZone["timezone"])        
    def getSunRiseSunSet(self):  # heures locales de lever et de coucher du soleil
        #https://api.sunrise-sunset.org/json?lat=50.6&lng=-34&formatted=0
        url="https://api.sunrise-sunset.org/json?lat="+str(self.lat)+"&lng="+str(self.lng)+"&date=today&formatted=0"
        #print url
        status=0
        while status != 200:
            r=requests.get(url)
            status=r.status_code
        #print r.content  # le résultat de la requête
        self.sunRiseSunSet=json.loads(r.content)
        sunrise=arrow.get(self.sunRiseSunSet["results"]["sunrise"])
        sunriseTs=sunrise.timestamp
        sunset=arrow.get(self.sunRiseSunSet["results"]["sunset"])
        sunsetTs=sunset.timestamp
        self.dayPosition= 100.*(self.tsUTC-sunriseTs)/(sunsetTs-sunriseTs)
        #print self.dayPosition
        self.heureSunriseLocale=sunrise.to(self.timeZone["timezone"])
        if (self.heureSunriseLocale.day!=self.heureLocale.day):
            self.heureSunriseLocale=self.heureSunriseLocale.replace(day=self.heureLocale.day)
        #print sunrise
        self.tsSunriseUTC=self.heureSunriseLocale.timestamp
        #print sunrise.to(self.timeZone["timeZoneId"])
        #print sunset
        self.heureSunsetLocale=sunset.to(self.timeZone["timezone"])
        if (self.heureSunsetLocale.day!=self.heureLocale.day):  # si ce n'est pas le sunset d'aujourd'hui
            self.heureSunsetLocale=self.heureSunsetLocale.replace(day=self.heureLocale.day)   # on le force à aujourd'hui    
        self.tsSunsetUTC=self.heureSunsetLocale.timestamp
        self.dayPosition=(self.tsUTC-self.tsSunriseUTC)/1./self.sunRiseSunSet["results"]["day_length"]*100.  # Où en est-on de la journée dans [0%,100%]
        #print self.dayPosition
        
        if self.dayPosition <0.:
            self.dayPhase="night morning"
        elif 0<=self.dayPosition <50.:
            self.dayPhase="day morning"
        elif 50<=self.dayPosition <=100.:
            self.dayPhase="day afternoon"
        else :
           self.dayPhase="night evening" 
    def getHauteur(self):   # calcul l'altitude du véhicule en fonction de l'heure locale
        hautNuit=10.
        if 0<=self.dayPosition <=100.:
            hautMidi=12000.
            x=(self.dayPosition/100.*2.*math.pi)-(math.pi/2.)
            self.hauteur=((math.sin(x)+1.)*0.5*(hautMidi-hautNuit))+hautNuit
        else:
            self.hauteur=hautNuit
    def moove (self,u,v,dt) : # le déplace pendant dt unités de temps avec les vitesses zonale et méridienne (u,v) en m/unité de temps
        self.lat=self.lat+vLat(v)*dt           # la latitude varie en fonction de v (vitesse méridienne)
        self.lng=self.lng+uLng(u,self.lat)*dt  # la longitude varie en fonction de u (vitesse zonale)
    def getVentActuelRandom(self,dd,ff):
        DELTA_DD=30.  # en degrès
        DELTA_FF=15.  # en m/s
        assert ff > DELTA_FF , (DELTA_FF,ff)
        rand_dd=random.random()-0.5
        direction=(dd+DELTA_DD*rand_dd)%360.
        direction = abs(direction)
        rand_ff=random.random()-0.5
        force=ff+DELTA_FF*rand_ff
        vent=VentHorizontal_DDFF(direction,force)
        return (vent.u,vent.v)    
    def getVentActuelArome (self):   #  Aquisition du vent Arome 0025 actuel à la hauteur du véhicule
        lesDeuxDates=lesChainesDateEntourantes()
        IdU=mostRecentId("0025","U(h)")    #  composante zonale du vent (positive vers l'Est)
        IdU.describeCoverage()
        #print IdU.height
        lesDeuxHauteurs=AxeVertical(IdU.height).encadrement(self.hauteur)
        #print (lesDeuxDates,self.hauteur,lesDeuxHauteurs)
        uBasBefore=prevision (IdU,self.lng,self.lat,lesDeuxDates[0],lesDeuxHauteurs[0])
        uBasAfter =prevision (IdU,self.lng,self.lat,lesDeuxDates[1],lesDeuxHauteurs[0])
        uBas=self.interpole(uBasBefore,uBasAfter,lesDeuxDates[2])  #  interpolation temporelle de uBas
        #print uBasBefore,uBasAfter,uBas
        uHautBefore=prevision (IdU,self.lng,self.lat,lesDeuxDates[0],lesDeuxHauteurs[1])
        uHautAfter =prevision (IdU,self.lng,self.lat,lesDeuxDates[1],lesDeuxHauteurs[1])
        uHaut=self.interpole(uHautBefore,uHautAfter,lesDeuxDates[2])  #  interpolation temporelle de uHaut
        #print uHautBefore,uHautAfter,uHaut
        u=self.interpole (uBas,uHaut,lesDeuxHauteurs[2])  # interpolation verticale de u
        #print uBas,uHaut,u
        IdV=mostRecentId("0025","V(h)")   #  composante méridienne du vent (positive vers le Nord)
        IdV.describeCoverage()
        vBasBefore=prevision (IdV,self.lng,self.lat,lesDeuxDates[0],lesDeuxHauteurs[0])
        vBasAfter =prevision (IdV,self.lng,self.lat,lesDeuxDates[1],lesDeuxHauteurs[0])
        vBas=self.interpole(vBasBefore,vBasAfter,lesDeuxDates[2])  #  interpolation temporelle de vBas
        #print vBasBefore,vBasAfter,vBas
        vHautBefore=prevision (IdV,self.lng,self.lat,lesDeuxDates[0],lesDeuxHauteurs[1])
        vHautAfter =prevision (IdV,self.lng,self.lat,lesDeuxDates[1],lesDeuxHauteurs[1])
        vHaut=self.interpole(vHautBefore,vHautAfter,lesDeuxDates[2])   #  interpolation temporelle de vHaut
        #print vHautBefore,vHautAfter,vHaut
        v=self.interpole(vBas,vHaut,lesDeuxHauteurs[2])  # interpolation verticale de v
        #print vBas,vHaut,v
        print (u,v)
        print (VentHorizontal(u,v).toStringKmh())
        return (u,v)
    def getVentActuelArpege(self):
        print ("Calcul du vent Arpège avec : ",self.lng,self.lat,self.hauteur)
        return (get_now_vent_arpege_world (self.lng,self.lat,self.hauteur))
    def interpole (self,xinf,xsup,alpha):   # interpolation temporelle ou verticale
        rep = ((100.-alpha)*xinf + alpha*xsup)/100.
        return rep
    def getVentActuel_10m_Darksky(self):
        ''' renvoi le vent actuel, (u,v) en m/s,à 10m par requête à l'API globale Darksky '''
        url="https://13ssr86jdc.execute-api.eu-west-1.amazonaws.com/lati_longi/darksky?longi="
        url=url+str(self.lng)
        url=url+"&lati="+str(self.lat)
        print (url)
        status=0
        while status != 200:
            r=requests.get(url)
            status=r.status_code
            print (status)
        self.vent10mDarksky=json.loads(r.content)
        print(self.vent10mDarksky["currently"])
        dd=self.vent10mDarksky["currently"]["windBearing"]
        ff_kmh=self.vent10mDarksky["currently"]["windSpeed"]
        vent_10m=VentHorizontal_DDFF(dd,ff_kmh/3.6)  # on transforme la vitesse en m/s
        u=vent_10m.u
        v=vent_10m.v
        #print (u,v)
        #print (VentHorizontal(u,v).toStringKmh())
        return (u,v)
        
    def getVentActuelMeteomatics(self):  #  Vent là où je metrouve actuellemente ?
        url="https://domicile_macveigh:MHSglNtCk5y78@api.meteomatics.com/now/wind_speed_u_"+str(int(round(self.hauteur,0)))+"m:ms,wind_speed_v_"+str(int(round(self.hauteur,0)))+"m:ms/"+str(self.lat)+","+str(self.lng)+"/json"
        print (url)
        status=0
        while status != 200:
            r=requests.get(url)
            status=r.status_code
            print (status)
        self.ventMeteomatics=json.loads(r.content)
        u= self.ventMeteomatics["data"][0]["coordinates"][0]["dates"][0]["value"]
        v= self.ventMeteomatics["data"][1]["coordinates"][0]["dates"][0]["value"]
        #print (u,v)
        #print (VentHorizontal(u,v).toStringKmh())
        return (u,v)
    def getVille(self):   # détermination de la ville au dessus de laquelle est le véhicule
        path="https://nominatim.openstreetmap.org/reverse?format=json&lat="+str(self.lat)+"&lon="+str(self.lng)+"&zoom=18&addressdetails=1"
        #print path
        status=0
        while status != 200:
            r=requests.get(path)
            status=r.status_code
        print (r.content)  # le résultat de la requête
        self.localisation=json.loads(r.content)
        if ("error" in self.localisation): 
            self.ville="ville inconnue"
        else :
            self.ville=self.localisation["display_name"]
        return self.ville
    def initDB(self):
        self.conn = sqlite3.connect('traject.sqlite')
        c = self.conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS trajectoire (ts num,lat real,lng real,haut real,lieu text)")
    def savePosition(self):  #  sauvegarde la postion actuelle
        sql="INSERT INTO trajectoire VALUES ("
        sql=sql+str(self.tsUTC)
        sql=sql+","+str(self.lat)+","+str(self.lng)+","+str(self.hauteur)+","
        sql=sql+'"'+self.ville+'")'
        #print sql
        c=self.conn.cursor()
        #c.execute("INSERT INTO trajectoire VALUES (150.,50.6,3.06,22.0,'Lille')")
        c.execute(sql)
        self.conn.commit()
    def listPositions(self):  #  liste toutes les positions archivées dans la base de données sqlite
        c=self.conn.cursor()
        for row in c.execute("SELECT * FROM trajectoire"):
            print (row)
    def affiche(self):
        for k in sorted(self.__dict__.keys()):
            print (k+":  "+str(self.__dict__[k]))
            #print (k)
"""
v=Vehicule(-21.566896, 165.498048,200)
v.affiche()
(u,v)=v.getVentActuelRandom(270.,16.)
print (u,v)
vent=VentHorizontal(u,v)
vent.affiche_tout()
"""
v=Vehicule(50.6,3.06,10.)
v.getVentActuel_10m_Darksky()
