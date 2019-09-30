  var path="MF-NWP-HIGHRES-AROME-001-FRANCE-WCS___T__HEIGHT___2017-06-14T03-00-00Z (1).tiff";
  path="tifftempo";
  var nomDeLaVariable=process.argv[2];
  require('./traiteGeotiff').traiteGeotiff(path,nomDeLaVariable);
  /*
  var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
  var xhr = new XMLHttpRequest();
  var url="MF-NWP-HIGHRES-AROME-0025-FRANCE-WCS___T__HEIGHT___2017-05-27T21-00-00Z.tiff"
  xhr.open('GET', url, true);
  xhr.responseType = 'arraybuffer';
  xhr.onload = function(e) {
    var tiff = GeoTIFF.parse(this.response);
    // ...
  }
  xhr.send();
  */
