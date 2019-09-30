"use strict";
var Position=require("./Position.js");
module.exports=class PositionSurface extends Position { // une position au niveau de la mer sur tere
  constructor (longi,lati){
      super(longi,lati,0.);
  }
};
