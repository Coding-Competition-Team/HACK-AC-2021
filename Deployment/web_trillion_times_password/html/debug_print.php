<?php
function debug_print($thing){
    ob_start();                    
    var_dump($thing);           
    $contents = ob_get_contents(); 
    ob_end_clean();                
    error_log($contents); 
}
?>