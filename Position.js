"use strict";
module.exports=class Position { // une position dans l'espace
  constructor (longi,lati,alti){
      if (alti<0.) throw new Error("position avec altitude négative: ",alti);  // altitude en mètres
      if ((longi<-180.)||(longi>180.)) throw new Error("longitude invalide: ",longi);  // longitude en degrés positifs à l'Est
      if ((lati<-90.)||(lati>90.)) throw new Error("latitude invalide: ",lati);  // latitude en degrés positifs au Nord
      this.longi=longi;
      this.lati=lati;
      this.alti=alti;
  }
  distance(position){  // distance orthodromique à une autre position
      return Math.sqrt(Math.pow(this.distanceSurSphere(position),2)+Math.pow(this.distanceVerticale(position),2));
  }
  distanceVerticale(position){ // distance verticale  une position
      return Math.abs(this.alti-position.alti);
  }
  distanceSurSphere (position) {
        /*
        c  J.P. Mac Veigh le 27/2/88
        c  Calcul de la distance (m) orthodromique entre deux points B (la présente position) et C (la position passée en argument) de la surface
        c  d'une sphère de rayon "rayon"(km) définis par leur latitude et longitude.
        c  On résoud le triangle sphérique formé par les deux points et le pôle
        c  nord et dont on connait deux côtés (les compléments des latitudes
        c  des deux points) et l'angle compris (la différence des longitudes des
        c  deux points).
        c  Référence: Cours d'Astronomie
        c             H. Andoyer
        c             première partie, troisième édition, page 24
        c             Librairie Scientifique J. Hermann, 1923.
        */
        var rayon=6366.2031; // rayon d'une sphère de 40 000 Km de circonférence (la terre)
        var pi=Math.PI;
        var dlong=(this.longi-position.longi)*(pi/180.);
        var rc=(pi/2)-(position.lati*pi/180.);
        var rb=(pi/2)-(this.lati*pi/180.);
        var x=Math.cos(rb)*Math.cos(rc)+Math.sin(rb)*Math.sin(rc)*Math.cos(dlong);
        if (x>1.)x=1.;
        if (x<-1.)x=-1.;
        var ra=Math.acos(x);
        var d=ra*rayon;
        return 1000.*(Math.abs(d));  // retour distance en mètres
   }
   affiche(){
       console.log (this);    
   }
};
