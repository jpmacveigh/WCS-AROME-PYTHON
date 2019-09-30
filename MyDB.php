<?php
class MyDB extends SQLite3 {  // Une BD Sqlite3
      function __construct($bdName){   // constructeur de la classe
          $this->open($bdName);
      }
      function blabla ($chaine){
        echo $chaine."<br>";
      }
      function selectArray ($queryString){
        $result=$this->query($queryString);
        $rows=array();
        while ($row = $result->fetchArray(SQLITE3_ASSOC)) {
          array_push($rows,$row);
        }
        return $rows;
      }
}
?>