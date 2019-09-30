<?php
function timestampToChaineDateArome($timestamp){
    $formatDeDate="Y-m-d\TH:i:s.000\Z";
    return gmdate($formatDeDate,$timestamp);
}
?>