<?php
function chaineDateAromeToTimestamp($chaineDate) {
     $formatDeDate="Y-m-d\TH:i:s\Z";
     $date = date_create_from_format($formatDeDate,$chaineDate,new DateTimeZone("UTC"));
     return $date->getTimestamp();
}
?>