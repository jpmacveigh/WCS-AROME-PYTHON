#!/usr/bin/python
import sqlite3
import json
con = sqlite3.connect("Arome.sqlite")
cur = con.cursor()
cur.execute("DELETE from prevision")
con.commit()
resultPrevi = open("resultPrevi", "r")
for line in resultPrevi.readlines():
    previ=json.dumps(line)
    cur.execute("INSERT INTO prevision (now,nom,abrev,niv,unit,run,date,val) VALUES(?,?,?,?,?,?,?,?)",[previ["now"],previ["nom"],previ["abrev"],previ["niv"],previ["unit"], previ["run"],previ["date"],previ["val"]])
con.commit()
con.close()
resultPrevi.close()