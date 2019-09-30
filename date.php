<!DOCTYPE html>
<html lang="en">
<head>
   <title>Essai date PHP</title>
   <meta charset="utf-8">
</head>
<body>
    <?php
        echo phpversion()."<br>";
        echo "heure locale du serveur :"."<br>";
        echo date("c :  U")."<br>";
        $ts=date("U");
        echo $ts."<br>";
        echo date("c",$ts)."<br><br>";
        echo "décallage horaire du serveur : ".date("O")."<br>";
        echo "fuseau horaire du serveur : ".date("e")."<br><br>";
        echo "heure UTC :"."<br>";
        echo gmdate("c :  U")."<br>";
        $ts=gmdate("U");
        echo $ts."<br>";
        echo gmdate("c",$ts)."<br><br>";
        echo "heure UTC au format choisi :"."<br>";
        $formatDeDate="Y-m-d\TH:i:s.000\Z";
        echo gmdate($formatDeDate)."<br>";  // format des WCS Arome
        $ts=gmdate("U");
        echo $ts."<br>";
        $chainedate=gmdate($formatDeDate,$ts);
        echo $chainedate."<br>";
        $datecree = date_create_from_format($formatDeDate,$chainedate,new DateTimeZone("UTC"));
        echo $datecree->getTimestamp()."<br>";
        include "chaineDateAromeToTimestamp.php";
        echo "Avec la fonction 'chaineDateAromeToTimestamp' : ".chaineDateAromeToTimestamp($chainedate)."<br>";
        include "timestampToChaineDateArome.php";
        echo "Avec la fonction 'timestampToChaineDateArome' : ".timestampToChaineDateArome($ts)."<br>";
    ?>
</body>
</html>
