<?php session_start() ?>
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
    .trace_courbe {
       width:  85%;
       height: 700px;
       margin: auto;
    }
  </style>
  <title>Série temporelle</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
  <script src="https://cdn.anychart.com/releases/8.1.0/js/anychart-base.min.js" type="text/javascript"></script>
</head>
<body>
  <script src="plot_points_previ.js" type="text/javascript"></script>
  <button type="button" class="btn btn-info" data-toggle="collapse" data-target="#liste_des_valeurs">Afficher la série de données</button>
<?php
  ini_set('display_errors',1);
  error_reporting(E_ALL) ;
  include("MyDB.php");
  include("AfficheTableauAssociatif.php");
  include("chaineDateAromeToTimestamp.php");
  $i=$_POST["valider"];
  echo "la serie a tracer est la numero: ".$i."<br>";
  $rows=$_SESSION ['rows'];
  $db = new MyDB('Arome.sqlite');
  $qstr ='select nom,now,run,date,val from prevision where nom="'.$rows[$i]["nom"].'" and niv="'.$rows[$i]["niv"].'" and hauteur="'.$rows[$i]["hauteur"].'" order by date';
  echo $qstr; 
  $series=$db->selectArray($qstr);  // extraction de la série temporelle
  //var_dump($series);
  AfficheTableauAssociatif('Serie temporelle de : '.$rows[$i]["nom"].' '.$rows[$i]["niv"].' '.$rows[$i]["hauteur"],$series);
  echo '<div id="courbe'.$i.'" class="trace_courbe">';  // emplacement où l'on va tracer 
  echo 'ici sera la courbe N°: '.$i.'</div>';
  echo '<script> 
    var x='.$i.';
    console.log("x: ",x);</script>';
  echo '<script>
    var data=[';
  for ($j=0;$j<sizeof($series);$j++){
    //echo'{x:'.$j.',value:'.$series[$j]["val"].'},';
    echo'{x:'.chaineDateAromeToTimestamp($series[$j]["date"]).',value:'.$series[$j]["val"].'},';
  }
  
  echo '];console.log(data);</script>';
  
?>
<?php  
  echo '<script>
    var transformxAxisLabel= function (ts){
      var jour=["dim","lun","mar","mer","jeu","ven","sam"];
      var d=new Date(ts*1000);
      return jour[d.getUTCDay()]+" "+(d.toISOString());
    };
    plot_points_previ(data,"courbe'.$i.'","'.$rows[$i]["nom"].' '.$rows[$i]["niv"].' '.$rows[$i]["hauteur"].'",transformxAxisLabel);
  </script><br>';
  flush();
?>
</body>
</html>