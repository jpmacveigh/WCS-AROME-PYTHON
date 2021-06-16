#!/usr/bin/python
# coding: utf8
import boto3
import sqlite3
import json
import os
from dateLimiteRetention import dateLimiteRetention
# Lecture du fichier previArome.txt lignes par lignes et écriture dans la base Arome.sqlite
def traiteAromePrevi():
    repcourant=os.getcwd()+"/"
    sqlite_name=repcourant+"Arome.sqlite"
    con = sqlite3.connect(sqlite_name)
    cur = con.cursor()
    #cur.execute("DELETE from prevision")
    con.commit()
    fic = open(repcourant+"previArome.txt", "r")
    for previ in fic.readlines():
        #print (previ)
        previ=json.loads(previ)
        if previ["z"]==None :  # traitement du cas des previsions au niveau du sol
            previ["z"]="0"
            previ["niv"]="height"  
        #print (previ)
        cur.execute("INSERT INTO prevision (now,nom,abrev,niv,hauteur,unit,run,date,val) VALUES(?,?,?,?,?,?,?,?,?)",[previ["now"],previ["nom"],previ["abrev"],previ["niv"],previ["z"],previ["unit"], previ["run"],previ["date"],previ["val"]])
    con.commit()
    dateLimite=dateLimiteRetention(40)  # on efface les données plus vieilles de 40 heures
    #cmd='DELETE FROM prevision WHERE now <= "'+dateLimite+'"'
    #print (cmd)
    #cur.execute(cmd)
    con.commit()
    con.close()
    fic.close()
    s3=boto3.client("s3")
    s3.upload_file(sqlite_name, "elasticbeanstalk-eu-west-1-062282685834", "Arome.sqlite") # upload de la base sqlite vers S3
traiteAromePrevi()    