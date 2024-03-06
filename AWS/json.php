<?php
header("Content-Type: application/json");

$x = 100;
$y = 50;

echo json_encode(array(
    "type" => "position package",
    "x" => $x,
    "y" => $y
));
?>
