"use strict";
var PositSurface=require("./PositionSurface.js");
module.exports=class GrilleLongLat{
    // Grille (long,lat) régulière
    // défine par son point NW (longiNW,latiNW) (degrès Nord positifs, Est positifs)
    // l'indice i des longitudes pris dans [0,nbLongi-1] croit vers l'Est de deltaLongi degrès
    // l'indice j dans latitudes pris [0,nbLati-1] décroit vers le Sud de deltaLati degrès
    constructor (longiNW,latiNW,nbLongi,nbLati,deltaLongi,deltaLati){ // constructeur de la classe
        this.longiNW=longiNW;
        this.latiNW=latiNW;
        this.nbLongi=nbLongi;
        this.nbLati=nbLati;
        this.deltaLongi=deltaLongi;
        this.deltaLati=deltaLati;
        this.longiSE=longiNW+(nbLongi-1)*deltaLongi;
        this.latiSE =latiNW-(nbLati-1)*deltaLati;
        this.ampliLongi=this.longiSE-this.longiNW;
        this.ampliLati=this.latiNW-this.latiSE;
    }
    getLongiLati(i,j){  // renvoie la longitude et la latitude du point (i,j) de la grille
        this.isValideIJ(i,j);
        var longi=this.longiNW+i*this.deltaLongi;
        var lati=this.latiNW-j*this.deltaLati;
        return {longi,lati};
    }
    quelleCase(longi,lati){  // renvoie le point NW(i,j) de la case de la grille dans laquelle se situe la position (longi,lati)
        this.isValideLongiLati(longi,lati);
        if (longi==this.longiSE){
            iNW=this.nbLongi-2;
        }
        else {
            var iNW=Math.trunc((longi-this.longiNW)/this.ampliLongi*this.nbLongi);
        }
        if (lati==this.latiSE){
            jNW=this.nbLati-2;
        }
        else {
            var jNW=Math.trunc((this.latiNW-lati)/this.ampliLati*this.nbLati);
        }
        this.isValideIJ(iNW,jNW);
        return {iNW,jNW};
    }
    nearest(longi,lati){  // recherche du point de la grille le plus proche de la position (longi,lati)
        var pos=new PositSurface(longi,lati);
        var pointNW=this.quelleCase(longi,lati);
        var distMini=Number.MAX_VALUE;
        for (var i=0;i<=1;i++){
            for (var j=0;j<=1;j++){
                var lonlat=this.getLongiLati(pointNW.iNW+i,pointNW.jNW+j);
                var dist=pos.distance(new PositSurface(lonlat.longi,lonlat.lati));
                if (dist<distMini){
                    distMini=dist;
                    var iNear=pointNW.iNW+i;
                    var jNear=pointNW.jNW+j;
                }
            }
        }
        return {iNear,jNear,distMini};
    }
    isValideIJ (i,j){  // le point (i,j) est-il dans la grille ?
      var rep = ((i>=0)&&(i<this.nbLongi)&&(j>=0)&&(j<this.nbLati));
      if (rep) {
      return true;
      }
      else { 
        var error="point( i: "+i+",j: "+j+") pas dans la grille";
        console.log(error);
        throw new Error(error);
      }
    }
    isValideLongiLati (longi,lati){  // le point (i,j) est-il dans la grille ?
      var rep = ((longi>=this.longiNW)&&(longi<=this.longiSE)&&(lati>=this.latiSE)&&(lati<=this.latiNW));
      if (rep) {
      return true;
      }
      else { 
        var error="coordonnées (longi: "+longi+",lati: "+lati+") pas dans la grille";
        console.log(error);
        throw new Error(error);
      }
    }
    affiche(){
        console.log(this);
    }
};
