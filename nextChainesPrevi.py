# coding: utf8
import calendar
import datetime
import time
def chaineUTCFromTs(tsUTC):  # chaine de date au format '%Y-%m-%dT%H:%M:%SZ' à partir d'un timestamp
    return datetime.datetime.utcfromtimestamp(tsUTC).strftime('%Y-%m-%dT%H:%M:%SZ')
def tsNow():
    return calendar.timegm(time.gmtime())  # now
def nextChainesPrevi():  # renvoi les 48 prochaines heures rondes UTC
    ts= tsNow()  # now
    rep=[]
    #rep.append(chaineUTCFromTs(ts))
    for i in range(0,48):
        ts=ts+3600-(ts % 3600)  #  on ajoute 3600 secondes et on arrondi à l'heure ronde précèdante
        rep.append(chaineUTCFromTs(ts))
    return rep   #  tableau des chaines
    
#print nextChainesPrevi()