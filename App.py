#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import datetime
import sqlite3
from getWCSCapabilities import profilVertical
from flask import jsonify,render_template,make_response
from flask import Flask
app = Flask(__name__)
@app.route('/profil_vertical/long=<float:longi>,lat=<float:lati>,param=<code>')
# exemple de requête : http://54.229.138.69/profil_vertical/long=3.06,lat=50.6,param=T(h)
#  où 54.229.138.69 est l'IP publique de l'instance EC2 allumée)
def profif(longi,lati,code="T(h)"):
    #return "Hello les mecs il est : "+ str(datetime.datetime.utcnow())
    #code="T(h)"
    print (code)
    tab= profilVertical ("0025",code,longi,lati)
    return jsonify(tab)

@app.route('/prevision/long=<float:longi>,lat=<float:lati>,param=<code>,niveau=<float:niveau>')
def prevision(longi,lati,code="t(h)"):
    return None


@app.route("/getTrajectoire")
def getTrajectoire():
    conn=sqlite3.connect('traject.sqlite')
    c=conn.cursor()
    res={}
    res["points"]=[]
    for row in c.execute("SELECT * FROM trajectoire"):
       res["points"].append({"ts":row[0],"lat":row[1],"lng":row[2],"hauteur":row[3],"ville":row[4]}) 
    response=make_response(jsonify(res))
    response.mimetype="application/json"
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
    
@app.route("/trajectoire")
def trajectoire():
    return render_template ("trajectoire.html")
        

if __name__ == '__main__':
   #app.run(debug=True,host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT',8080)) )
    app.run(debug=True,host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT',80))) 
