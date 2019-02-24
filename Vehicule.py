#coding: utf8
import time
import json
import requests
import arrow
class Vehicule:  # un véhicule qui se déplace
    def __init__(self,lat,lng,alt):
        if not(-180.<=lng<=180.): raise Exception ("Vehicule : lng doit être dans [-180,+180]")
        if not(-90.<=lat<=90.): raise Exception ("Vehicule : lat doit être dans [-90,+90]")
        if not(alt>=0.): raise Exception ("Vehicule : alt être >= 0.")
        self.lng=lng
        self.lat=lat
        self.alt=lat
    def getTime(self):  # Quelle heure (timestamp) est-il ?
        self.tsUTC=time.time();
        print self.tsUTC;
    def getTimeZone(self):  #  Quel est le décalage horaire de là où je me trouve ?
        self.getTime();
        urlGetTZ="https://maps.googleapis.com/maps/api/timezone/json?location="+str(self.lat)+","+str(self.lng)+"&timestamp="+str(self.tsUTC)+"&key=AIzaSyAJ5k6nijmVsFGQ8EqVs4YiSkdDucJbJ2s"
        status=0
        while status != 200:
            r=requests.get(urlGetTZ)
            status=r.status_code
        print r.content  # le résultat de la requête
        self.timeZone=json.loads(r.content)
        utc = arrow.utcnow()
        print ("heure UTC: "+str(utc)+"  soit TS: "+str(utc.timestamp))
        print ("heure locale Paris: "+str(utc.to("Europe/Paris")))
        print self.timeZone["timeZoneId"]
        print ("heure locale du lieu: "+str(utc.to(self.timeZone["timeZoneId"])))


v=Vehicule (13.6,103.06,20.);
v.getTimeZone()
