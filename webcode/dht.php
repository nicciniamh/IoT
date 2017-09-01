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
    $d = array(	"time" => $t['time'], 
            "temperature" => $t['t'. $units], 
            'units' => $units, //$uname[$units],
            'status' => 'ok',
            'humidity' => $t['h']
    );
}
header('Content-type: text/json');
echo json_encode($d);
?>
