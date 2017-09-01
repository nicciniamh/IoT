<?php
$sensfile = "/sensor/temp.json";
$units = 'f';
$uname = array('f' => 'farenheit', 'c' => 'celsius');
if(isset($_GET['units'])) {
	$u=strtolower(substr($_GET['units'],0,1));
	if($u == 'f' || $u == 'c')
		$units = $u;
}
$t=@file_get_contents($sensfile);
if (!isset($t)) {
    $d = array("status" => "fail", "error" => "Cannot read data", "dev" => $sensfile);
} else {
    $t = json_decode($t,true);
    $temp = $t['temperature'];
    if ($units == 'c') {
        $temp = intval((($temp - 32) *.556)*100)/100.0;
    }
    $d = array(	"time" => $t['time'], 
            "temperature" => $temp, 
            'units' => $units, //$uname[$units],
            'status' => 'ok',
    );
}
header('Content-type: text/json');
echo json_encode($d);
?>
