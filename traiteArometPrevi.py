#!/usr/bin/python
import sqlite3
import json
con = sqlite3.connect("Arome.sqlite")
cur = con.cursor()
cur.execute("DELETE from prevision")
con.commit()
fic = open("previArome.txt", "r")
for previ in fic.readlines():
    #print (previ)
    previ=json.loads(previ)
    #print (previ["nom"])
    cur.execute("INSERT INTO prevision (now,nom,abrev,niv,hauteur,unit,run,date,val) VALUES(?,?,?,?,?,?,?,?,?)",[previ["now"],previ["nom"],previ["abrev"],previ["niv"],previ["z"],previ["unit"], previ["run"],previ["date"],previ["val"]])
con.commit()
con.close()
fic.close()