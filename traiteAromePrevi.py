#!/usr/bin/python
# coding: utf8
import sqlite3
import json
# Lecture du fichier Arome.sqlite et écriture dans la base Arome.sqlite
def traiteAromePrevi():
    con = sqlite3.connect("Arome.sqlite")
    cur = con.cursor()
    #cur.execute("DELETE from prevision")
    con.commit()
    fic = open("previArome.txt", "r")
    for previ in fic.readlines():
        #print (previ)
        previ=json.loads(previ)
        #print (previ)
        cur.execute("INSERT INTO prevision (now,nom,abrev,niv,hauteur,unit,run,date,val) VALUES(?,?,?,?,?,?,?,?,?)",[previ["now"],previ["nom"],previ["abrev"],previ["niv"],previ["z"],previ["unit"], previ["run"],previ["date"],previ["val"]])
    con.commit()
    con.close()
    fic.close()
    