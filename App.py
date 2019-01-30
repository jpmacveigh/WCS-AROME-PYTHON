#! /usr/bin/python
# -*- coding:utf-8 -*-
import os
import datetime
from getWCSCapabilities import profilVertical
from flask import jsonify
from flask import Flask
app = Flask(__name__)
@app.route('/profil_vertical/long=<float:longi>,lat=<float:lati>,param=<code>')
def profif(longi,lati,code="T(h)"):
    #return "Hello les mecs il est : "+ str(datetime.datetime.utcnow())
    #code="T(h)"
    #print code
    tab= profilVertical ("0025",code,longi,lati)
    return jsonify(tab)

if __name__ == '__main__':
    app.run(debug=True,host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)) )

