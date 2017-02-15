<?php
function devUrl($sys) {
    return sprintf("http://%s.ducksfeet.com/sensor/temp",$sys);
}
date_default_timezone_set('America/Los_Angeles');
if (php_sapi_name() == "cli") {
    for($i = 1; $i < $argc; $i ++) {
        if(strpos($argv[$i],'=') != -1) {
            list($vi,$vv) = explode('=',$argv[$i],2);
            $_GET[$vi] = $vv;
        }
    }
}
header('Content-type: text/json');
if(!isset($_GET['sys'])) {
    $dht = array("status" => "fail", "error" => "device not specified", "mode" => php_sapi_name());
    $sys = null;
}
else {
    $sys = $_GET['sys'];
}
if($sys != null) {
    try {
        $timey = time()+60;
        unset($dht);
        $url = devUrl($sys);
        $dht = @json_decode(file_get_contents($url), true);
        if(!isset($dht)) {
            $dht["sys"] = $sys;
            $dht["url"] = $url;
            throw new Exception("Unable to get data from '${sys}': No response.");
        }
        $timex = (int)$dht["time"];
        if($timex > $timey) {
            throw new Exception("Stale Data");
        }
        $dht["sys"] = $sys;
    } catch(Exception $e) {
        $dht["status"] = "fail";
        $dht["error"] = $e->getMessage();
        if (!isset($dht["status"])) {
            $dht["tf"] = 0;
            $dht["tc"] = 0;
            $dht["h"] = 0;
        }
    }
}
echo json_encode($dht);
?>
