#!/usr/bin/env node
const sqlite3 = require('sqlite3').verbose();
var nomDB="Arome.sqlite";
var db = new sqlite3.Database(nomDB,(err) => {
  if (err) {
    console.error(err.message);
  }
  console.log('Connected to ',nomDB,' database.');
});
//db.run("DROP TABLE prevision");
//db.run("CREATE TABLE prevision (now text,nom text,abrev text,niv text,unit text,run text,date text,val text)");
var byline = require('byline');
process.stdin.resume();
process.stdin.setEncoding('utf8');
var stream = byline.createLineStream(process.stdin);
stream.on('data', function(line) {
  var previ=JSON.parse(line);
  //db.run(`INSERT INTO prevision (previ) VALUES(?)`,line,function(err) {
  db.run(`INSERT INTO prevision (now,nom,abrev,niv,unit,run,date,val)
  VALUES(?,?,?,?,?,?,?,?)`,previ.now,previ.nom,previ.abrev,previ.niv,previ.unit,
  previ.run,previ.date,previ.val,function(err) {
    if (err) {
      return console.log("erreur ecriture",err.message);
    }
    // get the last insert id
    console.log(`A row has been inserted with rowid ${this.lastID}`);
  });
});
stream.on('end', function() {
    // Ended !
    // close the database connection
});
db.close();
