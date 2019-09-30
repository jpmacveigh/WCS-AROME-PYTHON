
<?php
ini_set("display_errors", 1);
error_reporting(E_ALL) ;
echo date("r")."<br>";
$chaineDate="2019-08-28T03:00:00Z";
echo $chaineDate;
var_dump($chaineDate);
//include ("/home/ubuntu/environment/node_jpmv/Essais-java/chaineDateAromeToTimestamp.php");
include ("chaineDateAromeToTimestamp.php");
var_dump($chaineDate);
$ts =  chaineDateAromeToTimestamp ($chaineDate);
var_dump($ts);
phpinfo();
?>
