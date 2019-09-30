<?php session_start(); ?>
<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    #corps_tableau { 
      font-size: 0.7em;
    }
    html, body {
        width: 100%;
        height: 100%;
        margin:  0;
        padding: 0;
    }
  </style>
  <title>Prévisions V2</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>
  <script src="plot_points_previ.js" type="text/javascript"></script>
  <a name="haut"/>
	<p><a href="#bas">bas de la page</a></p>
  <?php
    ini_set("display_errors", 1);
    error_reporting(E_ALL) ;
    /*
    $path_workspace= $_SERVER['DOCUMENT_ROOT'];
    $path_workspace=substr($path_workspace,0,-1);
    echo($path_workspace)."<br>";
    $path=$path_workspace.dirname($_SERVER['PHP_SELF'])."/";
    echo ($path);
    */
    include ("chaineDateAromeToTimestamp.php");
    include ("AfficheTableauAssociatifAvecBouton.php");
    /*
    exec('cat resultPrevi | wc -l',$nblignes);
    echo '<h1>le fichier resultPrevi contient '.$nblignes[0].' lignes</h1>';
    */
    include("MyDB.php");
    echo "<h2>Traitements SQLITE</h2>";
    date_default_timezone_set('UTC');
    echo 'Version PHP courante : ' . phpversion()."<br>".date("r")."<br>";
    $db = new MyDB("Arome.sqlite");
    $result= $db->query('SELECT count(*) FROM prevision');
    $taillePrevision=$result->fetchArray()[0];
    echo '<h1>la table "prevision" de la base "Arome.sqlite" contient '.$taillePrevision.' lignes</h1>';
    $rows=$db->selectArray('SELECT now,nom,val FROM prevision');
    $i=0;
    echo "Première: ".$rows[$i]["now"]." ".$rows[$i]["nom"]." ".$rows[$i]["val"]."<br>";
    $i=sizeof($rows)-1;
    echo "Dernière: ".$rows[$i]["now"]." ".$rows[$i]["nom"]." ".$rows[$i]["val"]."<br>";
    $rows=$db->selectArray("select nom,niv,hauteur,count(*),min(date),max(date)
    from prevision group by nom,niv,hauteur order by nom");
    $_SESSION ["rows"]=$rows;
  ?>  
  <form name="choix-serie" method="post" action="dessine_serie_2.php" target="_blank">
  <?php
    AfficheTableauAssociatifAvecBouton("Liste des noms des variable et de leurs niveaux",$rows);
  ?>
  </form>
  <a name="bas"/>
	<p><a href="#haut">haut de la page</a></p>
</body>
</html>
