<!DOCTYPE html>
<html lang="en">
<head>
  <style>
    #corps_tableau { font-size: 0.7em;}
  </style>
  <title>Prévisions</title>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
</head>
<body>
  <a name="haut"/>
	<p><a href="#bas">bas de la page</a></p>
  <?php
    exec('cat resultPrevi | wc -l',$nblignes);
    echo '<h1>le fichier resultPrevi contient '.$nblignes[0].' lignes</h1>';
  ?>
  <?php  // lecture de la première ligne du fichier des prévisions
      $fichier = fopen('resultPrevi','r');
      echo $nombre_ligne_fichier;
      $ligne = fgets($fichier);
      fclose($fichier);
      $previ=json_decode($ligne,true);
  ?>
  <div id=nombreLignes></div>
  <div class="container">
    <h2>Prévisions</h2>
    <table class="table table-condensed">
      <thead>
        <tr>
         <th>n</th>    
         <?php
         foreach ($previ as $cle => $valeur){  // ecriture des entêtes des colonnes
          echo "<th>".$cle."</th>";
         }
         ?>
        </tr>
      </thead>
      <tbody id="corps_tableau">
        <?php
          $fichier = fopen('resultPrevi','r');
          $n=0;
          while (($ligne = fgets($fichier))!==false){
            $n=$n+1;
            $previ=json_decode($ligne,true);
            echo "<tr>";
              echo "<td>".$n."</td>";     // le numéro de la prévision dans la première 
              foreach ($previ as $cle => $valeur){  // écriture du contenu de chaque colonne
                echo "<td>".$valeur."</td>";
              }
            echo "</tr>";
          }
          fclose($fichier);
        ?>
      </tbody>
    </table>
  </div>
  <a name="bas"/>
	<p><a href="#haut">haut de la page</a></p>
</body>
</html>
