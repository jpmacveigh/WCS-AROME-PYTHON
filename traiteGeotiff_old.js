exports.traiteGeotiff=function(path,nomDeLaVariable){
  var fs = require("fs");
  var fichierDesPrevisions="resultPrevi";
  fs.readFile(path, function(err,geotiff) {
    if (err) throw err;
    //console.log("lecture OK geotiff de Météo-France : ", path);
    var dataArray = geotiff.buffer.slice();
    //console.log("slice OK");
    var GeoTIFF = require("geotiff");
    this.tiff = GeoTIFF.parse(dataArray);
    //console.log("parse OK");
    //console.log(tiff);
    //console.log("geotifView :",this.tiff.geotiffView);
    //console.log ("nombre images dans le tiff : ",this.tiff.getImageCount()); 
    this.image = this.tiff.getImage(); // or use .getImage(n) where n is between 0 and tiff.getImageCount() 
    //console.log("largeur : ",this.image.getWidth(), "   hauteur : ",this.image.getHeight(), "   pas : ",this.image.getSamplesPerPixel());
    console.log("************************* getFileDirectory *********************************");
    //console.log(this.image.getFileDirectory());
    console.log("***************************************************************************");
    var gdalMetadata = this.image.getFileDirectory().GDAL_METADATA;
    console.log ("***********************  GDAL_METADATA  ***********************")
    //console.log(gdalMetadata);
    console.log ("*****************************************************************")
    var DOMParser = require('xmldom').DOMParser;
    var parser = new DOMParser();
    var xmlDoc = parser.parseFromString(gdalMetadata,"text/xml");
    console.log ("*********************   xlmDoc ******************");
    //console.log ("xlmDoc",xmlDoc);
    console.log ("*************************************************");
    var variable=xmlDoc.getElementsByTagName("Item")[0].childNodes[0].nodeValue;
    console.log("variable : ",variable);
    variable=nomDeLaVariable;
    var abbrev=xmlDoc.getElementsByTagName("Item")[1].childNodes[0].nodeValue;
    console.log("abbréviation : ",abbrev);
    var echeance_sec=parseInt(xmlDoc.getElementsByTagName("Item")[2].childNodes[0].nodeValue); 
    console.log("échéance (sec) : ",echeance_sec);
    var short_name=xmlDoc.getElementsByTagName("Item")[4].childNodes[0].nodeValue;
    var unit=xmlDoc.getElementsByTagName("Item")[5].childNodes[0].nodeValue;
    console.log ("unit : ",unit);
    var dateDuRun=xmlDoc.getElementsByTagName("Item")[3].childNodes[0].nodeValue;
    //console.log("date du run : ",dateDuRun);
    var timeInMili =parseInt(xmlDoc.getElementsByTagName("Item")[3].childNodes[0].nodeValue.substring(0,10),10)*1000;
    //console.log (timeInMili);
    dateDuRun=new Date(timeInMili);
    console.log("date du run : ",new Date(timeInMili));
    var datePrevision=xmlDoc.getElementsByTagName("Item")[6].childNodes[0].nodeValue;
    //console.log("date prévision : ",datePrevision);
    timeInMili =parseInt(xmlDoc.getElementsByTagName("Item")[6].childNodes[0].nodeValue.substring(0,10),10)*1000;
    //console.log (timeInMili);
    datePrevision=new Date(timeInMili);
    console.log("date prévision : ",new Date(timeInMili));
    var description=xmlDoc.getElementsByTagName("Item")[7].childNodes[0].nodeValue;
    console.log("description : ",description);
    var rangCrochet=description.indexOf("]");
    var niveau=description.substring(0,rangCrochet+1);
    console.log ("niveau : ",niveau);
    console.log("ModelTiepoint : ",this.image.getFileDirectory().ModelTiepoint);
    console.log("ModelTiepoint[4] : ",this.image.getFileDirectory().ModelTiepoint[4]);
    console.log("************************** getGeoKey ***************************************");
    //console.log(this.image.getGeoKeys());
    console.log("**********************************************************************");
    // definition de la grilleLongLat couverte par le coverage
    var longimin=this.image.getFileDirectory().ModelTiepoint[3];         // longitude minimale (bord Ouest)
    var latimax=this.image.getFileDirectory().ModelTiepoint[4];          // latitude maximale  (bord Nord)
    //console.log ("longimin : ",longimin,"   latimax : ",latimax);
    var deltalongi=this.image.getFileDirectory().ModelPixelScale[0];     // incrément de longitude
    var deltalati=this.image.getFileDirectory().ModelPixelScale[1];      // décrément de latitude
    //console.log ("deltalongi : ",deltalongi,"   deltalati : ",deltalati);
    var nblongi=this.image.getWidth();        // nb de pixels sur la largeur (longitudes)
    var nblati=this.image.getHeight();        // nb de pixels sur la hauteur (latitudes)
    this.grille=new (require("./GrilleLongLat.js"))(longimin,latimax,nblongi,nblati,deltalongi,deltalati);
    this.grille.affiche();
    console.log(this.grille.getLongiLati(6,36));
    var rasters = this.image.readRasters();
    if (rasters[0].length == (this.image.getWidth()*this.image.getHeight())){
      //console.log ("longueur du raster : ",rasters[0].length,"  OK");
    }
    console.log("première valeur du raster rasters[0][0]: ",rasters[0][0]);
    console.log("dernière valeur du raster rasters[0][rasters[0].length-1] : ",rasters[0][rasters[0].length-1]);
    console.log("incrément de longitude : ",this.image.getFileDirectory().ModelPixelScale[0]);     // incrément de longitude
    console.log("décrément de latitude  : ",this.image.getFileDirectory().ModelPixelScale[1]);      // décrément de latitude
    console.log("premier point : ",getPoint(0,0));
    console.log("dernier point : ",getPoint(this.image.getWidth()-1,this.image.getHeight()-1));
    
    
    var valeurPrevue=" "+getPoint(6,36)["val"];
    var prevu2chiffres=parseFloat(valeurPrevue).toFixed(2);
    console.log("point défini  : ",getPoint(6,36));  // point Lille (3.06,50.64) dans vigentte 0.01 degrès couvrant Longi(3,4) et Lati(50,51)    //Affiche(image);
    var chaine=variable+" "+abbrev+"  "+description+" "+dateDuRun+" "+datePrevision+" "+valeurPrevue;
    //var DateUTCString=new Date().toUTCString();
    var DateUTCString=new Date().toISOString();
    var previ=
    {
      "now": DateUTCString,
      //"nom":short_name,
      "nom":variable,
      "abrev":abbrev,
      //"descr":description,
      "niv":niveau,
      "unit":unit,
      "run":dateDuRun,
      "date":datePrevision,
      "val":prevu2chiffres
    };
    chaine=JSON.stringify(previ);
    console.log (chaine);
    require("fs").appendFileSync("resultPrevi", chaine+"\n", "UTF-8");
    
    function getLongiLati(i,j){
      return this.grille.getLongiLati(i,j);
      /*
      isValide(i,j);
      var longimin=this.image.getFileDirectory().ModelTiepoint[3];         // longitude minimale (bord Ouest)
      var latimax=this.image.getFileDirectory().ModelTiepoint[4];          // latitude maximale  (bord Nord)
      //console.log ("longimin : ",longimin,"   latimax : ",latimax);
      var deltalongi=this.image.getFileDirectory().ModelPixelScale[0];     // incrément de longitude
      var deltalati=this.image.getFileDirectory().ModelPixelScale[1];      // décrément de latitude
      //console.log ("deltalongi : ",deltalongi,"   deltalati : ",deltalati);
      var longi=longimin+i*deltalongi;
      var lati=latimax-j*deltalati;
      return {longi,lati};
      */
      
    }
    
    function getValue(i,j){
      isValide(i,j);
      var nblongi=this.image.getWidth();        // nb de pixels sur la largeur (longitudes)
      //var nblati=image.getHeight();           // nb de pixels sur la hauteur (latitudes)
      var rasters = this.image.readRasters();
      return (rasters[0][j*nblongi + i]);     // le raster est supposé être une suite de "nblati" lignes de longitudes de "nblongi" de largeur
    }
    function getPoint(i,j){
      var val = getValue(i,j);
      var longi = getLongiLati(i,j)["longi"];
      var lati = getLongiLati(i,j)["lati"]
      return {longi,lati,val};
    }
    
    function Affiche (){
      for (var i=0;i<this.image.getWidth();i++){
        for (var j=0;j<this.image.getHeight();j++){
          console.log(i,j,getPoint(i,j));
        }
      }
    }
    
    function isValide (i,j){
      return this.grille.isValideIJ(i,j);
      /*
      var rep = ((i>=0)&&(i<this.image.getWidth())&&(j>=0)&&(j<this.image.getHeight()));
      if (rep) {
        return;
      }
      else { 
        console.log("(",i,",",j,") non valide");
        throw new Error("(",i,",",j,") non valide");
      }*/
    }
  });
}
