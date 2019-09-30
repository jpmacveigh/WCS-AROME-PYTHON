var GrilleLongLat=require("./GrilleLongLat.js");
var Position=require("./Position.js");
var PositionSurface=require("./PositionSurface.js");
var grille=new GrilleLongLat(3.0,51.0,101,101,0.01,0.01);
grille.affiche();
console.log(grille.getLongiLati(6,36));
console.log(grille.quelleCase(3.06,50.64));
console.log(grille.quelleCase(3.0,51.0));
console.log(grille.quelleCase(4.0,50.0));
var pos=new Position (grille.getLongiLati(6,36).longi,grille.getLongiLati(6,36).lati,0.);
pos.affiche();
console.log(pos.distanceSurSphere(new Position(grille.getLongiLati(6,37).longi,grille.getLongiLati(6,37).lati,0.)));
console.log(pos.distance(new Position(grille.getLongiLati(6,37).longi,grille.getLongiLati(6,37).lati,0.)));
var possurf=new PositionSurface (grille.getLongiLati(6,36).longi,grille.getLongiLati(6,36).lati);
possurf.affiche();
console.log(possurf.distance(new PositionSurface(grille.getLongiLati(6,37).longi,grille.getLongiLati(6,37).lati)));
console.log(possurf.distance(new Position(grille.getLongiLati(6,37).longi,grille.getLongiLati(6,37).lati,1000.)));
console.log(grille.nearest(possurf.longi,possurf.lati));
console.log(grille.nearest(4.,51.));
console.log(grille.nearest(3.067,50.45));
console.log(grille.nearest(3.,51.));
console.log(grille.nearest(4.,50.));
console.log(grille.nearest(3.,50.));
console.log(grille.getLongiLati(grille.nearest(3.233,50.587).iNear,grille.nearest(3.233,50.587).jNear));